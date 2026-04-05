from .exceptions import VertexRuntimeError, VertexSyntaxError

class Environment:
    def __init__(self):
        self.variables = {}

    def set(self, name, value):
        self.variables[name] = value

    def get(self, name):
        if name in self.variables:
            return self.variables[name]
        raise VertexRuntimeError(f"Undefined variable '{name}'")

class Interpreter:
    def __init__(self, env, output_widget):
        self.env = env
        self.output_widget = output_widget

    def execute(self, tokens):
        i = 0
        while i < len(tokens):
            t = tokens[i]
            
            if t.type == "PRINT":
                val = self.env.get(tokens[i+1].value) if tokens[i+1].type == "ID" else int(tokens[i+1].value)
                self.output_widget.insert("end", f"> {val}\n")
                i += 3
            elif t.type == "ID" and i + 1 < len(tokens) and tokens[i+1].type == "ASSIGN":
                name = t.value
                end = i
                while end < len(tokens) and tokens[end].type != "SEMI":
                    end += 1
                
                expr_tokens = tokens[i+2 : end]
                val = self.evaluate_expression(expr_tokens)
                self.env.set(name, val)
                i = end + 1
            else:
                i += 1

    def evaluate_expression(self, tokens):
        if not tokens:
            return 0
        res = self.get_value(tokens[0])
        idx = 1
        while idx < len(tokens):
            op = tokens[idx].value
            next_val = self.get_value(tokens[idx+1])
            if op == "+":
                res += next_val
            elif op == "-":
                res -= next_val
            elif op == "*":
                res *= next_val
            elif op == "/":
                if next_val == 0:
                    raise VertexRuntimeError("Division by zero!")
                res //= next_val
            idx += 2
        return res

    def get_value(self, token):
        if token.type == "NUMBER":
            return int(token.value)
        if token.type == "ID":
            return self.env.get(token.value)
        raise VertexSyntaxError(f"Unexpected token: {token.value}")
