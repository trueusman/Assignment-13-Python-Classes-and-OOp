"""Task 03: Recursively find every path whose value equals target."""

def find_paths(data, target):
    paths = []

    def equal(a, b):
        # Avoid Python's True == 1 and False == 0 behavior.
        if isinstance(a, bool) != isinstance(b, bool):
            return False
        return type(a) is type(b) or (
            isinstance(a, (int, float)) and not isinstance(a, bool)
            and isinstance(b, (int, float)) and not isinstance(b, bool)
        ) if a == b else False

    def walk(value, path):
        if equal(value, target):
            paths.append(path or "$")

        if isinstance(value, dict):
            for key, child in value.items():
                child_path = f"{path}.{key}" if path else str(key)
                walk(child, child_path)
        elif isinstance(value, list):
            for index, child in enumerate(value):
                walk(child, f"{path}[{index}]")

    walk(data, "")
    return paths


if __name__ == "__main__":
    sample = {"a": [{"x": 5}, 5], "b": {"y": 5}}
    print(find_paths(sample, 5))
