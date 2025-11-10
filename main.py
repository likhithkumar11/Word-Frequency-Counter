import re
from collections import Counter

DEFAULT_TOP_N = 10
DEFAULT_MIN_LEN = 1  # set to 3 later if you want to ignore very short words
DEFAULT_STOPWORDS = {"the", "and", "is", "in"}  # small demo list; you can expand it

CLEAN_REGEX = re.compile(r"[^a-z0-9]+")

def clean_and_tokenize(text: str):
    text = text.lower()
    text = CLEAN_REGEX.sub(" ", text)
    tokens = text.split()
    return tokens

def filter_tokens(tokens, min_len=DEFAULT_MIN_LEN, use_stopwords=False, stopwords=DEFAULT_STOPWORDS):
    if use_stopwords:
        return [t for t in tokens if len(t) >= min_len and t not in stopwords]
    else:
        return [t for t in tokens if len(t) >= min_len]

def count_frequencies(tokens):
    return Counter(tokens)

def display_by_frequency(counter: Counter, top_n: int):
    print("\n=== Top Words (by frequency) ===")
    for word, freq in counter.most_common(top_n):
        print(f"{word:20} {freq}")

def display_alphabetical(counter: Counter):
    print("\n=== All Words (alphabetical) ===")
    for word in sorted(counter):
        print(f"{word:20} {counter[word]}")

def prompt_yes_no(message: str) -> bool:
    while True:
        ans = input(f"{message} [y/n]: ").strip().lower()
        if ans in {"y", "yes"}:
            return True
        if ans in {"n", "no"}:
            return False
        print("Please enter y or n.")

def get_positive_int_or_default(prompt: str, default_val: int) -> int:
    raw = input(f"{prompt} (press Enter for {default_val}): ").strip()
    if raw == "":
        return default_val
    try:
        n = int(raw)
        if n <= 0:
            print("Please enter a positive integer; using default.")
            return default_val
        return n
    except ValueError:
        print("Invalid integer; using default.")
        return default_val

def main():
    print("WORD FREQUENCY COUNTER")
    print("----------------------")

    # 1) Ask for file path with retry loop
    while True:
        path = input("Enter path to a text file (e.g., sample.txt): ").strip()
        try:
            with open(path, "r", encoding="utf-8") as f:
                text = f.read()
            break
        except FileNotFoundError:
            print("Error: File not found.")
        except OSError as e:
            print(f"Error opening file: {e}")
        if not prompt_yes_no("Try again?"):
            print("Exiting.")
            return

    # Handle empty file
    if not text.strip():
        print("The file is empty after reading. Nothing to analyze.")
        return

    # 2) Clean + tokenize
    tokens = clean_and_tokenize(text)

    # Optional filters
    use_custom_n = prompt_yes_no("Would you like to choose how many top words to display?")
    top_n = get_positive_int_or_default("Enter N", DEFAULT_TOP_N) if use_custom_n else DEFAULT_TOP_N

    ignore_short = prompt_yes_no("Ignore very short words (e.g., length < 3)?")
    min_len = 3 if ignore_short else DEFAULT_MIN_LEN

    use_stop = prompt_yes_no("Use a small stop-word list (the, and, is, in)?")

    tokens = filter_tokens(tokens, min_len=min_len, use_stopwords=use_stop)

    # 3) Count
    counter = count_frequencies(tokens)

    total_words = sum(counter.values())
    unique_words = len(counter)

    # Guard for empty after filtering
    if total_words == 0:
        print("After filtering, there are no words to count.")
        return

    # Validate top_n vs unique words
    if top_n > unique_words:
        print(f"Note: N ({top_n}) > unique words ({unique_words}). Showing all unique words instead.")
        top_n = unique_words

    # 4) Display summary
    print("\n=== Summary ===")
    print(f"Total words (after cleaning/filters): {total_words}")
    print(f"Total unique words: {unique_words}")

    # 5) Display sorted by frequency (descending)
    display_by_frequency(counter, top_n)

    # Optional: alphabetical view
    if prompt_yes_no("Also display alphabetical listing?"):
        display_alphabetical(counter)

    # Optional: save results
    if prompt_yes_no("Save full word frequencies to an output file?"):
        out_path = input("Enter output filename (e.g., output.txt): ").strip() or "output.txt"
        try:
            with open(out_path, "w", encoding="utf-8") as out:
                out.write("word,count\n")
                for w, c in counter.most_common():
                    out.write(f"{w},{c}\n")
            print(f"Saved results to {out_path}")
        except OSError as e:
            print(f"Could not save the file: {e}")

if __name__ == "__main__":
    main()
