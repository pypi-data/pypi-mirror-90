import sys
from .print_err import print_err


def main():
    print_err(sys.argv[1])
    if len(sys.argv) > 2:
        exit_code = int(sys.argv[2])
        exit(exit_code)


if __name__ == "__main__":
    main()
