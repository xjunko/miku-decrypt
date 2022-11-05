"""
    decrypt.py - common world decryptor
"""
__maintainer__ = "FireRedz"
__source__ = "TearlessHen"

import sys

# Constants
READ: bytes = b"\x10\x00\x00\x00"
SKIP: bytes = b"\x20\x00\x00\x00"


def main(args: list[str]) -> int:
    if len(args) < 2:
        print("No file path given, exiting.")
        return 1

    # Pray to god that the file exists and decrypt it.
    with open(args[1], "br+") as file:
        data: bytes = file.read()

        if data[:4] == SKIP:
            data = data[4:]
        elif data[:4] == READ:
            data = data[4:]
            header: bytes = bytes(
                a ^ b for a, b in zip(data[:128], (b"\xff" * 5 + b"\x00" * 3) * 16)
            )
            data = header + data[128:]

        file.seek(0)
        file.write(data)
        file.truncate()

    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
