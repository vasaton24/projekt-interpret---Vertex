from vertex.lexer import Lexer
from vertex.interpreter import Interpreter, Environment  
from vertex.gui import VertexGUI
from vertex.exceptions import VertexError
import tkinter as tk

class App:
    def __init__(self):
        self.root = tk.Tk()
        self.env = Environment()
        self.gui = VertexGUI(self.root, self.run_code)

    def run_code(self):
        self.gui.output.delete("1.0", tk.END)
        code = self.gui.editor.get("1.0", tk.END)
        try:
            lexer = Lexer(code)
            tokens = lexer.tokenize()
            interpreter = Interpreter(self.env, self.gui.output)
            interpreter.execute(tokens)
        except VertexError as e:
            self.gui.output.insert("end", f"SYNTAX ERROR: {e}\n")
        except Exception as e:
            self.gui.output.insert("end", f"SYSTEM ERROR: {e}\n")

    def start(self):
        self.root.mainloop()

if __name__ == "__main__":
    App().start()
