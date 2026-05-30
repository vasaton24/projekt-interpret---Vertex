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
        self.gui: VertexGUI = VertexGUI(self.root, self.run_code, self.reset_environment)
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

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

    def reset_environment(self) -> None:
        """Reset the interpreter environment to a clean state."""
        self.env = Environment()
        self.gui.update_status("Prostředí bylo resetováno.")

    def on_close(self) -> None:
        """Save configuration before closing the application."""
        try:
            self.gui.save_config()
        finally:
            self.root.destroy()

    def start(self) -> None:
        """Start the main event loop of the application."""
        self.root.mainloop()

def main() -> None:
    """Launch the Vertex IDE application."""
    App().start()

if __name__ == "__main__":
    main()
