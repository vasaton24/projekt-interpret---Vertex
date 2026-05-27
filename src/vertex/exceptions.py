"""Custom exceptions used across the Vertex interpreter."""

class VertexError(Exception):
    """Base class for all custom Vertex errors."""
    pass

class VertexSyntaxError(VertexError):
    """Raised when the Lexer or Parser encounters invalid syntax."""
    pass

class VertexRuntimeError(VertexError):
    """Raised when an error occurs during the execution of the AST."""
    pass