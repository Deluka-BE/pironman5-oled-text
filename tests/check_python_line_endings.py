"""Reject CRLF in tracked Python blobs; .gitattributes requires LF."""

import subprocess
import sys


def git(*args):
    return subprocess.check_output(["git", *args])


def main():
    paths = git("ls-files", "-z", "--", "*.py").split(b"\0")
    bad = []
    for raw_path in filter(None, paths):
        path = raw_path.decode("utf-8", "surrogateescape")
        if b"\r\n" in git("show", f":{path}"):
            bad.append(path)
    if bad:
        print("Tracked Python blobs contain CRLF (expected LF):", file=sys.stderr)
        for path in bad:
            print(f"  {path}", file=sys.stderr)
        return 1
    print("Tracked Python blobs use LF line endings.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
