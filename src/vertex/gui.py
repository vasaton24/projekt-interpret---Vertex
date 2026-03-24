import tkinter as tk
from tkinter import scrolledtext
import json
import os

class VertexGUI:
    def __init__(self, root, run_callback):
        self.root = root
        self.root.title("Vertex IDE Pro")
        self.root.geometry("800x600")

        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_rowconfigure(3, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        config = self.load_config()

        tk.Label(root, text="Editor:").grid(row=0, column=0, sticky="w", padx=10)
        self.editor = scrolledtext.ScrolledText(root, bg=config.get("editor_bg", "white"))
        self.editor.grid(row=1, column=0, sticky="nsew", padx=10)

        self.run_btn = tk.Button(root, text="RUN (F5)", command=run_callback, bg="green", fg="white")
        self.run_btn.grid(row=2, column=0, pady=10)
        self.root.bind("<F5>", lambda e: run_callback())

        tk.Label(root, text="Output:").grid(row=3, column=0, sticky="w", padx=10)
        self.output = scrolledtext.ScrolledText(root, bg="black", fg="lightgreen")
        self.output.grid(row=4, column=0, sticky="nsew", padx=10)

    def load_config(self):
        if os.path.exists("config.json"):
            with open("config.json", "r") as f:
                return json.load(f)
        return {}
