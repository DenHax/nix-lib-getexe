#!/usr/bin/env python3
import re
import sys
import os
from pathlib import Path


def process_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    pattern = r"\$\{pkgs\.([^}]+)\}/bin/([^}\s]+)"

    def replacement(match):
        pkg = match.group(1)
        cmd = match.group(2)

        if pkg == cmd:
            return f"${{lib.getExe pkgs.{pkg}}}"
        else:
            return f'${{lib.getExe\' pkgs.{pkg} "{cmd}"}}'

    new_content = re.sub(pattern, replacement, content)

    if new_content != content:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(new_content)
        return True
    return False


def main():
    if len(sys.argv) != 2:
        print("Usage: bin2exe <file_or_directory>")
        sys.exit(1)

    target = Path(sys.argv[1])

    if not target.exists():
        print(f"Error: {target} does not exist")
        sys.exit(1)

    processed_count = 0

    if target.is_file():
        if process_file(target):
            processed_count += 1
    else:
        for root, dirs, files in os.walk(target):
            for file in files:
                if file.endswith(".nix"):
                    filepath = Path(root) / file
                    if process_file(filepath):
                        processed_count += 1

    print(f"Processed {processed_count} file(s)")


if __name__ == "__main__":
    main()
