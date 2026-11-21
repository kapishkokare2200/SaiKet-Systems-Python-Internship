
import re
import string
from collections import Counter


def analyze(text):
    words = re.findall(r"[A-Za-z0-9']+", text.lower())
    return {
        "lines": len(text.splitlines()),
        "words": len(words),
        "characters": len(text),
        "characters_no_spaces": len("".join(text.split())),
        "unique_words": len(set(words)),
        "frequency": Counter(words),
    }


def print_report(stats, top_n=10):
    print("\n" + "=" * 40)
    print("          TEXT ANALYSIS REPORT")
    print("=" * 40)
    print(f"{'Lines':<24}{stats['lines']:>10}")
    print(f"{'Words':<24}{stats['words']:>10}")
    print(f"{'Unique words':<24}{stats['unique_words']:>10}")
    print(f"{'Characters':<24}{stats['characters']:>10}")
    print(f"{'Characters (no spaces)':<24}{stats['characters_no_spaces']:>10}")

    print(f"\nTop {top_n} most common words")
    print("-" * 40)
    print(f"{'Rank':<6}{'Word':<18}{'Count':>6}{'%':>8}")
    total = stats["words"] or 1
    for rank, (word, count) in enumerate(stats["frequency"].most_common(top_n), start=1):
        bar = "#" * min(count, 20)
        print(f"{rank:<6}{word:<18}{count:>6}{count / total * 100:>7.1f}%  {bar}")


def main():
    print("=== WORD COUNT TOOL ===")
    path = input("Text file to analyze: ").strip()
    try:
        with open(path, "r", encoding="utf-8") as f:
            text = f.read()
    except FileNotFoundError:
        print(f"Error: '{path}' not found.")
        return
    except PermissionError:
        print(f"Error: no permission to read '{path}'.")
        return
    except UnicodeDecodeError:
        print("Error: file is not UTF-8 text.")
        return

    if not text.strip():
        print("The file is empty.")
        return
    print_report(analyze(text))


if __name__ == "__main__":
    main()