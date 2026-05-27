"""Main entry point for the Vertex IDE application."""

import tkinter as tk
from vertex.lexer import Lexer
from vertex.interpreter import Interpreter, Environment
from vertex.gui import VertexGUI
from vertex.exceptions import VertexError

class App:
    """Main application class tying together the GUI, Lexer, Parser, and Interpreter."""
    
    def __init__(self) -> None:
        """Initialize the root window, environment, and GUI."""
        self.root: tk.Tk = tk.Tk()
        self.env: Environment = Environment()
        self.gui: VertexGUI = VertexGUI(self.root, self.run_code)

    def run_code(self) -> None:
        """Retrieve code from the editor, tokenize, parse, and execute it."""
        self.gui.output.delete("1.0", tk.END)
        code: str = self.gui.editor.get("1.0", tk.END)
        try:
            lexer: Lexer = Lexer(code)
            tokens = lexer.tokenize()
            interpreter: Interpreter = Interpreter(self.env, self.gui.output)
            interpreter.execute(tokens)
        except VertexError as e:
            self.gui.output.insert("end", f"CHYBA: {e}\n")
        except Exception as e:
            self.gui.output.insert("end", f"SYSTÉMOVÁ CHYBA: {e}\n")

    def start(self) -> None:
        """Start the main event loop of the application."""
        self.root.mainloop()

if __name__ == "__main__":
    App().start()
