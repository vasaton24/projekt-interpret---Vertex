"""Graphical User Interface module for Vertex IDE."""

import tkinter as tk
from tkinter import scrolledtext
import json
import os
from typing import Callable, Dict, Any

class VertexGUI:
    """Class handling the layout and behavior of the main Tkinter window."""
    
    def __init__(self, root: tk.Tk, run_callback: Callable[[], None]) -> None:
        """Initialize GUI components.
        
        Args:
            root (tk.Tk): The main Tkinter root window.
            run_callback (Callable): Function to execute when the Run button is pressed.
        """
        self.root: tk.Tk = root
        self.root.title("Vertex IDE Pro")
        self.root.geometry("850x650")
        self.root.configure(bg="#1e1e1e")
        
        self.root.grid_rowconfigure(1, weight=3)
        self.root.grid_rowconfigure(3, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        self.config: Dict[str, Any] = self.load_config()

        lbl_editor = tk.Label(root, text="KÓD EDITOR", fg="#ffffff", bg="#1e1e1e", font=("Consolas", 10, "bold"))
        lbl_editor.grid(row=0, column=0, sticky="w", padx=15, pady=(15, 5))
        
        self.editor = scrolledtext.ScrolledText(
            root, 
            bg="#2d2d2d", 
            fg="#d4d4d4", 
            insertbackground="white",
            font=("Consolas", 11)
        )
        self.editor.grid(row=1, column=0, sticky="nsew", padx=15, pady=5)
        
        default_code = "x = 10 ;\ny = 20 ;\nz = x + y * 20 ;\nprint z ;\n\nprint 10 + 20 + 30 ;\n\nfor (i = 0; i < 3; i = i + 1) {\n    print i ;\n}"
        self.editor.insert(tk.END, default_code)

        self.run_btn = tk.Button(
            root, 
            text="SPUSTIT KÓD (F5)", 
            command=run_callback, 
            bg="#0e639c", 
            fg="white",
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            padx=10,
            pady=5
        )
        self.run_btn.grid(row=2, column=0, pady=15)
        self.root.bind("<F5>", lambda e: run_callback())

        lbl_output = tk.Label(root, text="VÝSTUP", fg="#ffffff", bg="#1e1e1e", font=("Consolas", 10, "bold"))
        lbl_output.grid(row=3, column=0, sticky="w", padx=15, pady=(10, 5))

        self.output = scrolledtext.ScrolledText(
            root, 
            bg="#1e1e1e", 
            fg="#a3dda3", 
            insertbackground="white",
            font=("Consolas", 11),
            relief="sunken"
        )
        self.output.grid(row=4, column=0, sticky="nsew", padx=15, pady=(5, 15))

    def load_config(self) -> Dict[str, Any]:
        """Load configuration settings from config.json if it exists.
        
        Returns:
            Dict[str, Any]: A dictionary containing configuration data.
        """
        if os.path.exists("config.json"):
            with open("config.json", "r") as f:
                return json.load(f)
        return {}