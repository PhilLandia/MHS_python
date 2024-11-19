import sys


def nl(file=None):
    try:
        lines = open(file).readlines() if file else sys.stdin.readlines()
        for i, line in enumerate(lines, 1):
            print(f"{i} {line.rstrip()}")
    except FileNotFoundError:
        print(f"Error: File '{file}' not found.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    file = sys.argv[1] if len(sys.argv) > 1 else None
    nl(file)
