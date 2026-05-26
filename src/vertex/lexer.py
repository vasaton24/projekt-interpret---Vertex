import re
from typing import List
from .exceptions import VertexSyntaxError

class Token:
    def __init__(self, type: str, value: str) -> None:
        self.type: str = type
        self.value: str = value

class Lexer:
    def __init__(self, text: str) -> None:
        self.text: str = text
        self.tokens: List[Token] = []

    def tokenize(self) -> List[Token]:
        token_specification = [
            ("NUMBER",   r"\d+"),
            ("PRINT",    r"\bprint\b"),
            ("IF",       r"\bif\b"),
            ("ELSE",     r"\belse\b"),
            ("WHILE",    r"\bwhile\b"),
            ("FOR",      r"\bfor\b"),
            ("ID",       r"[a-zA-Z_][a-zA-Z0-9_]*"),
            ("EQ",       r"=="),
            ("NE",       r"!="),
            ("LE",       r"<="),
            ("GE",       r">="),
            ("ASSIGN",   r"="),
            ("PLUS",     r"\+"),
            ("MINUS",    r"-"),
            ("TIMES",    r"\*"),
            ("DIVIDE",   r"/"),
            ("LT",       r"<"),
            ("GT",       r">"),
            ("SEMI",     r";"),
            ("LPAREN",   r"\("),
            ("RPAREN",   r"\)"),
            ("LBRACE",   r"\{"),
            ("RBRACE",   r"\}"),
            ("LBRACKET", r"\["),
            ("RBRACKET", r"\]"),
            ("COMMA",    r","),
            ("SKIP",     r"[ \t\n\r]+"),
            ("MISMATCH", r"."),
        ]
        tok_regex: str = "|".join(f"(?P<{pair[0]}>{pair[1]})" for pair in token_specification)
        for mo in re.finditer(tok_regex, self.text):
            kind: str = mo.lastgroup if mo.lastgroup else "MISMATCH"
            value: str = mo.group()
            if kind == "SKIP":
                continue
            elif kind == "MISMATCH":
                raise VertexSyntaxError(f"Neočekávaný znak: {value}")
            else:
                self.tokens.append(Token(kind, value))
        return self.tokens
