import sys


def print_err(*args, **kwargs):
    exit_code = kwargs.get("exit_code")
    if exit_code is not None:
        del kwargs["exit_code"]
    kwargs["file"] = sys.stderr
    print(*args, **kwargs)
    if exit_code is not None:
        exit(exit_code)
