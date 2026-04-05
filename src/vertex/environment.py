from .exceptions import VertexRuntimeError

class Environment:
    def __init__(self):
        self.variables = {}

    def set(self, name, value):
        """Uloží novou proměnnou nebo přepíše stávající."""
        self.variables[name] = value

    def get(self, name):
        """Vytáhne hodnotu proměnné. Pokud neexistuje, nahlásí chybu."""
        if name in self.variables:
            return self.variables[name]
        
        raise VertexRuntimeError(f"Použití nedefinované proměnné '{name}'")