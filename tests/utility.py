import random
from string import ascii_lowercase


def make_random_string(length: int = 10) -> str:
    return "".join(random.choices(ascii_lowercase, k=length))
