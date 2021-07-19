#!/usr/bin/env python3
import sys
import getopt
import re
from pathlib import Path


def main() -> None:
    optlist, args = getopt.getopt(sys.argv[1:], 'o::')
    options = dict(optlist)

    output_path = options.get("-o")
    data = sys.stdin.read()
    data = re.sub(r"/\*[^!].+?\*/", "", data, flags=re.DOTALL)
    data = re.sub(r"^\s+", "", data, flags=re.MULTILINE)
    data = re.sub(r"\n(?:\n\s*)+", "\n", data)

    if output_path is None:
        print(data)
    else:
        Path(output_path).write_text(data)


if __name__ == "__main__":
    main()
