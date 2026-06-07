"""Hlavní vstupní bod aplikace Vertex IDE."""

import tkinter as tk
from vertex.lexer import Lexer
from vertex.interpreter import Interpreter, Environment
from vertex.gui import VertexGUI
from vertex.exceptions import VertexError, VertexSyntaxError

class App:
    """Hlavní třída aplikace spojující GUI, lexer, parser a interpret."""
    
    def __init__(self) -> None:
        """Inicializuje hlavní okno, prostředí a rozhraní GUI."""
        self.root: tk.Tk = tk.Tk()
        self.env: Environment = Environment()
        self.gui: VertexGUI = VertexGUI(self.root, self.run_code, self.reset_environment)
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def run_code(self) -> None:
        """Získá kód z editoru, provede tokenizaci a vykonání."""
        self.gui.output.delete("1.0", tk.END)
        self.gui.clear_error_highlight()
        code: str = self.gui.editor.get("1.0", tk.END)
        try:
            lexer: Lexer = Lexer(code)
            tokens = lexer.tokenize()
            interpreter: Interpreter = Interpreter(self.env, self.gui.output)
            interpreter.execute(tokens)
            self.gui.clear_error_highlight()
        except VertexError as e:
            if isinstance(e, VertexSyntaxError):
                self.gui.output.insert("end", f"CHYBA: {e}\n")
                self.gui.highlight_error(e.line)
            else:
                self.gui.output.insert("end", f"CHYBA: {e}\n")
        except Exception as e:
            self.gui.output.insert("end", f"SYSTÉMOVÁ CHYBA: {e}\n")

    def reset_environment(self) -> None:
        """Obnoví prostředí interpretu do výchozího stavu."""
        self.env = Environment()
        self.gui.update_status("Prostředí bylo resetováno.")

    def on_close(self) -> None:
        """Uloží konfiguraci při ukončení aplikace."""
        try:
            self.gui.save_config()
        finally:
            self.root.destroy()

    def start(self) -> None:
        """Spustí hlavní událostní smyčku aplikace."""
        self.root.mainloop()

def main() -> None:
    """Spustí aplikaci Vertex IDE."""
    App().start()

if __name__ == "__main__":
    main()
