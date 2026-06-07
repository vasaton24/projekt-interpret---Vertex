"""Lexikální analyzátor pro zdrojový kód jazyka Vertex."""

import re
from typing import List
from .exceptions import VertexSyntaxError

class Token:
    """Token s typem, hodnotou a pozicí ve zdroji."""

    def __init__(self, type: str, value: str, line: int = 1, column: int = 1) -> None:
        self.type: str = type
        self.value: str = value
        self.line: int = line
        self.column: int = column

class Lexer:
    """Převádí vstupní text na posloupnost tokenů."""

    def __init__(self, text: str) -> None:
        self.text: str = text
        self.tokens: List[Token] = []

    def tokenize(self) -> List[Token]:
        """Projde vstupní text a vytvoří seznam tokenů.
        
        Vrací:
            List[Token]: Seznam tokenů reprezentujících zdrojový kód.
        """
        token_specification = [
            ("NUMBER",   r"\d+"),
            ("PRINT",    r"\bprint\b"),
            ("IF",       r"\bif\b"),
            ("ELSE",     r"\belse\b"),
            ("WHILE",    r"\bwhile\b"),
            ("FOR",      r"\bfor\b"),
            ("AND",      r"\band\b"),
            ("OR",       r"\bor\b"),
            ("NOT",      r"\bnot\b"),
            ("ID",       r"[a-zA-Z_][a-zA-Z0-9_]*"),
            ("STRING",   r'"(?:\\.|[^"\\])*"'),
            ("EQ",       r"=="),
            ("NE",       r"!="),
            ("LE",       r"<="),
            ("GE",       r">="),
            ("ASSIGN",   r"="),
            ("PLUS",     r"\+"),
            ("MINUS",    r"-"),
            ("TIMES",    r"\*"),
            ("COMMENT",  r"//.*|/\*[\s\S]*?\*/|#.*"),
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
        def update_position(line: int, column: int, text: str) -> tuple[int, int]:
            if "\n" in text:
                line += text.count("\n")
                column = len(text) - text.rfind("\n")
            else:
                column += len(text)
            return line, column

        tok_regex: str = "|".join(f"(?P<{pair[0]}>{pair[1]})" for pair in token_specification)
        line = 1
        column = 1
        for mo in re.finditer(tok_regex, self.text):
            kind: str = mo.lastgroup if mo.lastgroup else "MISMATCH"
            lexeme: str = mo.group()
            if kind == "SKIP" or kind == "COMMENT":
                line, column = update_position(line, column, lexeme)
                continue
            elif kind == "STRING":
                raw_string = lexeme[1:-1]
                value = bytes(raw_string, "utf-8").decode("unicode_escape")
                self.tokens.append(Token(kind, value, line, column))
            elif kind == "MISMATCH":
                raise VertexSyntaxError(f"Neočekávaný znak: {lexeme}", line, column)
            else:
                self.tokens.append(Token(kind, lexeme, line, column))
            line, column = update_position(line, column, lexeme)
        return self.tokens