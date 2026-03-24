class VertexError(Exception):
    """Základní třída pro chyby v jazyce Vertex."""
    pass

class VertexSyntaxError(VertexError):
    """Chyba v zápisu kódu."""
    pass

class VertexRuntimeError(VertexError):
    """Chyba při běhu."""
    pass
