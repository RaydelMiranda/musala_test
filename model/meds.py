from dataclasses import dataclass


@dataclass
class Medication:
    name: str
    weight: int
    code: str
    # Image will be represented (for simplicity) as a b64 encoded string.
    image: bytes
