"""Task 02: Longest substring without repeated characters."""

def longest_unique_window(text):
    last_seen = {}
    left = 0
    best_start = 0
    best_length = 0

    for right, char in enumerate(text):
        if char in last_seen and last_seen[char] >= left:
            left = last_seen[char] + 1
        last_seen[char] = right

        current_length = right - left + 1
        if current_length > best_length:  # strict > keeps earliest on ties
            best_start = left
            best_length = current_length

    return text[best_start:best_start + best_length], best_start, best_length


if __name__ == "__main__":
    for value in ("abcabcbb", "", "pwwkew", "a b!a"):
        print(repr(value), "->", longest_unique_window(value))
