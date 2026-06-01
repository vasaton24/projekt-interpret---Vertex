"""Custom exceptions used across the Vertex interpreter."""

class VertexError(Exception):
    """Base class for all custom Vertex errors."""
    pass

class VertexSyntaxError(VertexError):
    """Raised when the Lexer or Parser encounters invalid syntax."""

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
    """Raised when an error occurs during the execution of the AST."""

    def __init__(self, message: str, line: int | None = None, column: int | None = None) -> None:
        self.message: str = message
        self.line: int | None = line
        self.column: int | None = column
        super().__init__(message)

    def __str__(self) -> str:
        if self.line is not None and self.column is not None:
            return f"{self.message} na řádku {self.line}, sloupec {self.column}"
        return self.message