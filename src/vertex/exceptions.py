"""Vlastní výjimky používané v interpretu Vertex."""

class VertexError(Exception):
    """Základní třída pro vlastní chyby Vertex."""
    pass

class VertexSyntaxError(VertexError):
    """Vyvolá se při chybné syntaxi v lexeru nebo parseru."""

    def __init__(self, message: str, line: int | None = None, column: int | None = None) -> None:
        self.message: str = message
        self.line: int | None = line
        self.column: int | None = column
        super().__init__(message)

    def __str__(self) -> str:
        if self.line is not None and self.column is not None:
            return f"{self.message} na řádku {self.line}, sloupec {self.column}"
        return self.message

class VertexRuntimeError(VertexError):
    """Vyvolá se při chybě během vykonávání AST."""

    def __init__(self, message: str, line: int | None = None, column: int | None = None) -> None:
        self.message: str = message
        self.line: int | None = line
        self.column: int | None = column
        super().__init__(message)

    def __str__(self) -> str:
        if self.line is not None and self.column is not None:
            return f"{self.message} na řádku {self.line}, sloupec {self.column}"
        return self.message