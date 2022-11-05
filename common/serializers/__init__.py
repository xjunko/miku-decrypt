from .deserialize import BinaryDeserialize


def deserialize(data: bytes) -> int | dict | list | str | float | bool:
    return BinaryDeserialize(data).process()
