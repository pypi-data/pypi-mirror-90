from ctypes import (CDLL, Structure, POINTER, c_char, c_int, c_long, c_short,
                    c_char_p, c_void_p)
import pathlib
from typing import Any

from .wrapper import *


def analyze(filename: str) -> Any:
    so_file = pathlib.Path(__file__).parent / "pdf.so"
    funcs = CDLL(so_file)
    funcs.pdf_summary.restype  = c_void_p

    pointer = funcs.pdf_summary(bytes(filename, encoding='utf-8'))

    summary = pdf_t.from_address(pointer)
    return summary
