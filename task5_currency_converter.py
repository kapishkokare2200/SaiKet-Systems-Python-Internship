
import os
import sys
import requests

COMMON = ["USD", "EUR", "GBP", "INR", "JPY", "AUD", "CAD", "AED"]


def get_rates():
    app_id = os.environ.get("OXR_APP_ID")
    if app_id:
        url = f"https://openexchangerates.org/api/latest.json?app_id={app_id}"
        key = "rates"
    else:
        url = "https://open.er-api.com/v6/latest/USD"
        key = "rates"
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return response.json()[key]


def convert(amount, from_cur, to_cur, rates):
    """Convert via USD: amount / rate(from) * rate(to)."""
    return amount / rates[from_cur] * rates[to_cur]


def ask_currency(prompt, rates):
    while True:
        code = input(prompt).strip().upper()
        if code in rates:
            return code
        print(f"'{code}' is not a supported currency code. Try e.g. {', '.join(COMMON[:5])}.")


def ask_amount():
    while True:
        raw = input("Amount: ").strip().replace(",", "")
        try:
            value = float(raw)
            if value <= 0:
                print("Amount must be greater than zero.")
                continue
            return value
        except ValueError:
            print("Please enter a valid number.")


def main():
    print("=== CURRENCY CONVERTER ===")
    try:
        rates = get_rates()
    except requests.exceptions.RequestException as e:
        sys.exit(f"Could not fetch exchange rates: {e}")

    print("Common codes:", ", ".join(COMMON))
    while True:
        from_cur = ask_currency("From currency: ", rates)
        to_cur = ask_currency("To currency:   ", rates)
        amount = ask_amount()
        result = convert(amount, from_cur, to_cur, rates)
        print(f"\n{amount:,.2f} {from_cur} = {result:,.2f} {to_cur}")
        print(f"(1 {from_cur} = {convert(1, from_cur, to_cur, rates):.4f} {to_cur})\n")
        if input("Convert another? (y/n): ").strip().lower() != "y":
            print("Goodbye!")
            break


if __name__ == "__main__":
    main()