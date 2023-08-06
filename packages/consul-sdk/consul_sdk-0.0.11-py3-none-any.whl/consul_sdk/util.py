from typing import List


def chunk(it: List, size: int):
    return [it[i : (i + size)] for i in range(0, len(it), size)]
