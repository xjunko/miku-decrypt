"""
    encrypt.py - common world encryptor
"""
__maintainer__ = "FireRedz"
__source__ = "TearlessHen"

import sys

# Constants
ENCRYPT: bytes = b"\x55\x6E\x69\x74"
SKIP: bytes = b"\x20\x00\x00\x00"


def main(args: list[str]) -> int:
    if len(args) < 3:
        print("Not enough arguments, exiting. [Requires `in`, `out`]")
        return 1

    # Pray to god that the file exists and decrypt it.
    with open(args[1], "br+") as file:
        with open(args[2], "bw+") as out:
            data: bytes = file.read()

            if data[:4] == SKIP:
                data = data[4:]
            elif data[:4] == ENCRYPT:
                xor = b"\x10\x00\x00\x00"
                header = bytes(
                    a ^ b for a, b in zip(data[:128], (b"\xff" * 5 + b"\x00" * 3) * 16)
                )
                data = xor + header + data[128:]

            out.seek(0)
            out.write(data)
            out.truncate()

    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
