
import shutil


def read_file(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def write_file(path, text):
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)


def find_and_replace(path, old, new, case_sensitive=True, backup=True):
    text = read_file(path)

    if case_sensitive:
        count = text.count(old)
        updated = text.replace(old, new)
    else:
        import re
        pattern = re.compile(re.escape(old), re.IGNORECASE)
        updated, count = pattern.subn(new, text)

    if count == 0:
        return 0
    if backup:
        shutil.copyfile(path, path + ".bak")
    write_file(path, updated)
    return count


def main():
    print("=== FIND & REPLACE TOOL ===")
    path = input("File name (e.g. sample.txt): ").strip()
    try:
        text = read_file(path)
        print(f"\n--- Current content ({len(text)} characters) ---\n{text}\n")

        old = input("Word/phrase to find: ")
        if not old:
            print("Nothing to find. Exiting.")
            return
        new = input("Replace with: ")
        case = input("Case sensitive? (y/n): ").strip().lower() == "y"

        count = find_and_replace(path, old, new, case_sensitive=case)
        if count:
            print(f"\nReplaced {count} occurrence(s). Saved to {path} (backup: {path}.bak)")
        else:
            print(f"\n'{old}' was not found. File left unchanged.")

    except FileNotFoundError:
        print(f"Error: '{path}' does not exist. Check the name and try again.")
    except PermissionError:
        print(f"Error: no permission to read/write '{path}'.")
    except IsADirectoryError:
        print(f"Error: '{path}' is a folder, not a file.")
    except UnicodeDecodeError:
        print(f"Error: '{path}' is not a readable UTF-8 text file.")
    except OSError as e:
        print(f"Unexpected file error: {e}")


if __name__ == "__main__":
    main()