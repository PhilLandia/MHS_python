import sys

def tail_file(file, lines=10, show_filename=False):
    try:
        with open(file, 'r') as f:
            content = f.readlines()[-lines:]
            if show_filename:
                print(f"==> {file} <==")
            print(''.join(content), end='')
    except FileNotFoundError:
        print(f"Error: File '{file}' not found.", file=sys.stderr)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)

def tail_stdin(lines=17):
    content = sys.stdin.readlines()[-lines:]
    print(''.join(content), end='')

if __name__ == "__main__":
    files = sys.argv[1:]
    if files:
        for i, file in enumerate(files):
            show_filename = len(files) > 1
            tail_file(file, show_filename=show_filename)
            if i < len(files) - 1:
                print()
    else:
        tail_stdin()