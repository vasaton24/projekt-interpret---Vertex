import tkinter as tk
from tkinter import scrolledtext

class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

class Lexer:
    def __init__(self, text):
        self.text = text
        self.tokens = []

    def tokenize(self):
        clean_text = self.text.replace(";", " ; ").replace("=", " = ").replace("+", " + ")
        words = clean_text.split()
        
        for word in words:
            if word == "var":
                self.tokens.append(Token("VAR", word))
            elif word == "print":
                self.tokens.append(Token("PRINT", word))
            elif word == "=":
                self.tokens.append(Token("ASSIGN", word))
            elif word == ";":
                self.tokens.append(Token("SEMI", word))
            elif word.isdigit():
                self.tokens.append(Token("NUMBER", word))
            else:
                self.tokens.append(Token("ID", word))
        return self.tokens

class Environment:
    def __init__(self):
        self.variables = {}

    def set(self, name, value):
        self.variables[name] = value

    def get(self, name):
        if name in self.variables:
            return self.variables[name]
        return 0

class Interpreter:
    def __init__(self, output_widget):
        self.env = Environment()
        self.output_widget = output_widget

    def execute(self, tokens):
        i = 0
        while i < len(tokens):
            token = tokens[i]
            
            if token.type == "VAR":
                var_name = tokens[i + 1].value
                var_value = self.evaluate(tokens[i + 3])
                self.env.set(var_name, var_value)
                i = i + 5
                
            elif token.type == "PRINT":
                val = self.evaluate(tokens[i + 1])
                self.output_widget.insert(tk.END, f"> {val}\n")
                i = i + 3
                
            elif token.type == "ID" and i + 1 < len(tokens) and tokens[i+1].type == "ASSIGN":
                var_name = token.value
                var_value = self.evaluate(tokens[i + 2])
                self.env.set(var_name, var_value)
                i = i + 4
            else:
                i = i + 1

    def evaluate(self, token):
        if token.type == "NUMBER":
            return int(token.value)
        if token.type == "ID":
            return self.env.get(token.value)
        return 0

class VertexGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Vertex IDE")
        self.root.geometry("600x500")

        self.label_edit = tk.Label(root, text="Editor:")
        self.label_edit.pack()

        self.editor = scrolledtext.ScrolledText(root, height=10, width=70)
        self.editor.pack(pady=5)
        self.editor.insert(tk.END, "var x = 10 ;\nprint x ;\nx = 25 ;\nprint x ;")

        self.run_btn = tk.Button(root, text="RUN", command=self.run_code, bg="green", fg="white")
        self.run_btn.pack(pady=10)

        self.label_out = tk.Label(root, text="Output:")
        self.label_out.pack()

        self.output = scrolledtext.ScrolledText(root, height=10, width=70, bg="black", fg="lightgreen")
        self.output.pack(pady=5)

    def run_code(self):
        self.output.delete("1.0", tk.END)
        code = self.editor.get("1.0", tk.END)
        try:
            l = Lexer(code)
            tokens = l.tokenize()
            interp = Interpreter(self.output)
            interp.execute(tokens)
        except Exception as e:
            self.output.insert(tk.END, f"Error: {e}")

def main():
    root = tk.Tk()
    app = VertexGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
