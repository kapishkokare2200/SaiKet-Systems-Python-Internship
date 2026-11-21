
import random

LEVELS = {
    "1": ("Easy", 1, 50, 10),
    "2": ("Medium", 1, 100, 7),
    "3": ("Hard", 1, 500, 9),
}


def choose_level():
    print("Choose a difficulty:")
    for key, (name, low, high, tries) in LEVELS.items():
        print(f"  {key}. {name}: number between {low} and {high}, {tries} attempts")
    while True:
        choice = input("Your choice (1-3):- ").strip()
        if choice in LEVELS:
            return LEVELS[choice]
        print("Please enter 1, 2 or 3")


def play_round():
    name, low, high, max_attempts = choose_level()
    secret = random.randint(low, high)
    attempts = 0
    print(f"\nI'm thinking of a number between {low} and {high}. You have {max_attempts} attempts.")

    while attempts < max_attempts:
        raw = input(f"Attempt {attempts + 1}/{max_attempts} - your guess:- ").strip()
        if not raw.lstrip("-").isdigit():
            print("That's not a whole number(This didn't use up an attempt.)")
            continue
        guess = int(raw)
        if guess < low or guess > high:
            print(f"Stay within {low} and {high}. (This didn't use up an attempt)")
            continue

        attempts += 1
        if guess < secret:
            print("Too low! Try a higher number")
        elif guess > secret:
            print("Too high! Try a lower number")
        else:
            print(f"\nCorrect! You guessed {secret} in {attempts} attempt(s)")
            return attempts
    print(f"\nOut of attempts. The number was {secret}.")
    return None


def main():
    print("=== GUESS THE NUMBER ===")
    best = None
    while True:
        result = play_round()
        if result is not None and (best is None or result < best):
            best = result
        if best is not None:
            print(f"Your best score this session: {best} attempt(s).")
        if input("\nPlay again? (y/n): ").strip().lower() != "y":
            print("Thanks for playing!")
            break
        print()


if __name__ == "__main__":
    main()