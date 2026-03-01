import re
import sys

class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

class Lexer:
    def __init__(self, text):
        self.text = text
        self.tokens = []
        self.rules = [
            ('VAR', r'var'),
            ('PRINT', r'print'),
            ('ID', r'[a-zA-Z_][a-zA-Z0-9_]*'),
            ('NUMBER', r'\d+'),
            ('ASSIGN', r'='),
            ('PLUS', r'\+'),
            ('MINUS', r'-'),
            ('SEMI', r';'),
            ('SPACE', r'\s+'),
        ]

    def tokenize(self):
        pos = 0
        while pos < len(self.text):
            match = None
            for name, pattern in self.rules:
                regex = re.compile(pattern)
                match = regex.match(self.text, pos)
                if match:
                    if name != 'SPACE':
                        self.tokens.append(Token(name, match.group()))
                    pos = match.end()
                    break
            if not match:
                raise SyntaxError(f"Unknown character at position {pos}")
        return self.tokens

class Environment:
    def __init__(self):
        self.variables = {}

    def set(self, name, value):
        self.variables[name] = value

    def get(self, name):
        if name in self.variables:
            return self.variables[name]
        raise NameError(f"Variable '{name}' is not defined")

class Interpreter:
    def __init__(self):
        self.env = Environment()

    def execute(self, tokens):
        i = 0
        while i < len(tokens):
            token = tokens[i]

            if token.type == 'VAR':
                name = tokens[i + 1].value
                i += 3 
                val = self.evaluate_expression(tokens[i])
                self.env.set(name, val)
                i += 2 
            
            elif token.type == 'PRINT':
                val = self.evaluate_expression(tokens[i + 1])
                print(f"> {val}")
                i += 3
            
            elif token.type == 'ID' and i + 1 < len(tokens) and tokens[i+1].type == 'ASSIGN':
                name = token.value
                i += 2
                val = self.evaluate_expression(tokens[i])
                self.env.set(name, val)
                i += 2
            else:
                i += 1

    def evaluate_expression(self, token):
        if token.type == 'NUMBER':
            return int(token.value)
        if token.type == 'ID':
            return self.env.get(token.value)
        return 0

def start_repl():
    interpreter = Interpreter()
    print("--- Vertex Language Interface ---")
    print("Type 'exit' to quit.")
    while True:
        try:
            user_input = input("vertex> ")
            if user_input.lower() == 'exit':
                break
            if not user_input.strip():
                continue
            
            l = Lexer(user_input)
            tokens = l.tokenize()
            interpreter.execute(tokens)
        except Exception as e:
            print(f"Runtime Error: {e}")

if __name__ == "__main__":
    start_repl()
