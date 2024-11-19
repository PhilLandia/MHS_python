import sys

def calculate_statistics(content):
    lines = len(content.splitlines())
    words = len(content.split())
    bytes_count = len(content.encode('utf-8'))
    return lines, words, bytes_count
def wc_file(file):
    try:
        with open(file, 'r', encoding='utf-8') as f:
            content = f.read()
        return calculate_statistics(content), file
    except FileNotFoundError:
        print(f"Error: File '{file}' not found.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

def wc_stdin():
    content = sys.stdin.read()
    return calculate_statistics(content)

def print_statistics(stats, file_name=None):
    lines, words, bytes_count = stats
    if file_name:
        print(f"{lines} {words} {bytes_count} {file_name}")
    else:
        print(f"{lines} {words} {bytes_count}")

if __name__ == "__main__":
    files = sys.argv[1:]
    total_stats = (0, 0, 0)

    if files:
        for file in files:
            stats, file_name = wc_file(file)
            print_statistics(stats, file_name)
            total_stats = tuple(x + y for x, y in zip(total_stats, stats))

        if len(files) > 1:
            print_statistics(total_stats, "total")
    else:
        stats = wc_stdin()
        print_statistics(stats)