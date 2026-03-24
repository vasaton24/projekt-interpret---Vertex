class Token:
    def __init__(self, type, value, line=1):
        self.type = type
        self.value = value
        self.line = line

class Lexer:
    def __init__(self, text):
        self.text = text
        self.tokens = []

    def tokenize(self):
        for op in [";", "=", "+", "-", "*", "/"]:
            self.text = self.text.replace(op, f" {op} ")
        
        words = self.text.split()
        for word in words:
            if word == "var": self.tokens.append(Token("VAR", word))
            elif word == "print": self.tokens.append(Token("PRINT", word))
            elif word == "=": self.tokens.append(Token("ASSIGN", word))
            elif word == ";": self.tokens.append(Token("SEMI", word))
            elif word in ["+", "-", "*", "/"]: self.tokens.append(Token("OP", word))
            elif word.isdigit(): self.tokens.append(Token("NUMBER", word))
            else: self.tokens.append(Token("ID", word))
        return self.tokens
