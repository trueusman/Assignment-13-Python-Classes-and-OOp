"""Task 09: Stream ERROR log entries and summarize them by date."""

from collections import Counter
from datetime import datetime

def read_errors(path, malformed_counter=None):
    malformed = 0
    with open(path, "r", encoding="utf-8") as file:
        for line_number, raw_line in enumerate(file, start=1):
            parts = [part.strip() for part in raw_line.split("|", 2)]
            if len(parts) != 3:
                malformed += 1
                continue
            timestamp, level, message = parts
            try:
                parsed = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                malformed += 1
                continue
            if not level or not message:
                malformed += 1
                continue
            if level == "ERROR":
                yield line_number, timestamp, message

    if malformed_counter is not None:
        malformed_counter["count"] = malformed

def summarize_errors(path):
    malformed = {"count": 0}
    counts = Counter()
    for _, timestamp, _ in read_errors(path, malformed):
        counts[timestamp[:10]] += 1
    return dict(counts), malformed["count"]


if __name__ == "__main__":
    sample_path = "sample.log"
    with open(sample_path, "w", encoding="utf-8") as file:
        file.write("2026-11-07 10:30:00 | ERROR | Connection lost\\n")
        file.write("2026-11-07 10:31:00 | INFO | Service started\\n")
        file.write("not a valid log line\\n")
    print(list(read_errors(sample_path)))
    print(summarize_errors(sample_path))
