from enum import Enum, auto
from dataclasses import dataclass
from typing import Union


class TokenType(Enum):
    # punctuation
    LPAREN = auto()
    RPAREN = auto()
    SEMI = auto()

    # special forms
    DEFINE = auto()
    IF = auto()
    LAMBDA = auto()
    DEFUN = auto()
    LIST = auto()

    # types
    TRUE = auto()
    NIL = auto()
    INTEGER = auto()
    FLOAT = auto()
    STRING = auto()

    # math operators
    PLUS = auto()
    MULTIPLY = auto()
    MINUS = auto()
    DIVIDE = auto()

    # comparison operators
    EQUALS = auto()
    GREATER = auto()
    LESS = auto()
    GEQ = auto()
    LEQ = auto()

    # other symbols
    IDENT = auto()

    EOF = auto()



@dataclass
class Token:
    type: TokenType
    pos: int
    literal: Union[int, float, str, None]

    def __repr__(self):
        return f'Token({self.type}, {self.pos}, {self.literal})'



