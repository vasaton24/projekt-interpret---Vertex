"""Graphical User Interface module for Vertex IDE."""

import tkinter as tk
from tkinter import scrolledtext, filedialog, messagebox
import json
import os
from typing import Callable, Dict, Any

class VertexGUI:
    """Class handling the layout and behavior of the main Tkinter window."""
    
    def __init__(self, root: tk.Tk, run_callback: Callable[[], None], reset_callback: Callable[[], None]) -> None:
        """Initialize GUI components.
        
        Args:
            root (tk.Tk): The main Tkinter root window.
            run_callback (Callable): Function to execute when the Run button is pressed.
            reset_callback (Callable): Function to execute when environment reset is requested.
        """
        self.root: tk.Tk = root
        self.root.title("Vertex IDE Pro")
        self.default_code: str = (
            "x = 10 ;\ny = 20 ;\nz = x + y * 20 ;\nprint z ;\n\nprint 10 + 20 + 30 ;\n\n"
            "for (i = 0; i < 3; i = i + 1) {\n    print i ;\n}"
        )
        self.config: Dict[str, Any] = self.load_config()
        self.root.geometry(self.config.get("window_geometry", "850x650+100+100"))
        self.root.configure(bg="#1e1e1e")
        self.reset_callback = reset_callback
        
        # Reserve rows: 0=banner, 1=editor label, 2=editor, 3=run button, 4=output label, 5=output, 6=status
        self.root.grid_rowconfigure(2, weight=3)
        self.root.grid_rowconfigure(5, weight=2)
        self.root.grid_columnconfigure(0, weight=1)

        self.create_menu()

        # Top banner (styled like CSS header)
        self.banner_frame = tk.Frame(root, bg="#0e639c", height=44)
        self.banner_frame.grid(row=0, column=0, sticky="ew")
        self.banner_frame.grid_propagate(False)
        self.banner_label = tk.Label(self.banner_frame, text="Vertex IDE Pro", fg="#ffffff", bg="#0e639c", font=("Segoe UI", 12, "bold"))
        self.banner_label.pack(side="left", padx=15, pady=8)

        lbl_editor = tk.Label(root, text="KÓD EDITOR", fg="#ffffff", bg="#1e1e1e", font=("Consolas", 10, "bold"))
        lbl_editor.grid(row=1, column=0, sticky="w", padx=15, pady=(12, 5))
        
        self.editor = scrolledtext.ScrolledText(
            root, 
            bg="#2d2d2d", 
            fg="#d4d4d4", 
            insertbackground="white",
            font=("Consolas", self.config.get("font_size", 11)),
            wrap="none"
        )
        self.editor.grid(row=2, column=0, sticky="nsew", padx=15, pady=5)
        
        self.editor.insert(tk.END, self.config.get("last_code", self.default_code))

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
        self.run_btn.grid(row=3, column=0, pady=15)
        self.root.bind("<F5>", lambda e: run_callback())
        self.root.bind("<Control-s>", lambda e: self.save_code_as())

        lbl_output = tk.Label(root, text="VÝSTUP", fg="#ffffff", bg="#1e1e1e", font=("Consolas", 10, "bold"))
        lbl_output.grid(row=4, column=0, sticky="w", padx=15, pady=(10, 5))

        self.output = scrolledtext.ScrolledText(
            root, 
            bg="#1e1e1e", 
            fg="#a3dda3", 
            insertbackground="white",
            font=("Consolas", self.config.get("font_size", 11)),
            relief="sunken",
            wrap="none"
        )
        self.output.grid(row=5, column=0, sticky="nsew", padx=15, pady=(5, 5))

        self.status_var = tk.StringVar(value="Ready")
        self.status_label = tk.Label(root, textvariable=self.status_var, fg="#d4d4d4", bg="#1e1e1e", font=("Segoe UI", 9))
        self.status_label.grid(row=6, column=0, sticky="ew", padx=15, pady=(0, 10))

        self.apply_theme()

    def create_menu(self) -> None:
        menu_bar = tk.Menu(self.root)

        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Otevřít kód...", command=self.open_file)
        file_menu.add_command(label="Uložit kód jako...", command=self.save_code_as)
        file_menu.add_separator()
        file_menu.add_command(label="Uložit nastavení", command=self.save_config)
        file_menu.add_command(label="Resetovat nastavení", command=self.reset_settings)
        file_menu.add_separator()
        file_menu.add_command(label="Ukončit", command=self.root.quit)
        menu_bar.add_cascade(label="Soubor", menu=file_menu)

        edit_menu = tk.Menu(menu_bar, tearoff=0)
        edit_menu.add_command(label="Vyčistit výstup", command=self.clear_output)
        edit_menu.add_command(label="Resetovat prostředí", command=self.reset_callback)
        menu_bar.add_cascade(label="Upravit", menu=edit_menu)

        settings_menu = tk.Menu(menu_bar, tearoff=0)
        settings_menu.add_command(label="Nastavení", command=self.open_settings_dialog)
        menu_bar.add_cascade(label="Nastavení", menu=settings_menu)

        help_menu = tk.Menu(menu_bar, tearoff=0)
        help_menu.add_command(label="O aplikaci", command=self.show_about)
        menu_bar.add_cascade(label="Nápověda", menu=help_menu)

        self.root.config(menu=menu_bar)

    def default_config(self) -> Dict[str, Any]:
        return {
            "theme": "dark",
            "font_size": 11,
            "window_geometry": "850x650+100+100",
            "last_code": self.default_code,
        }

    def load_config(self) -> Dict[str, Any]:
        """Load configuration settings from config.json if it exists.
        
        Returns:
            Dict[str, Any]: A dictionary containing configuration data.
        """
        if os.path.exists("config.json"):
            try:
                with open("config.json", "r", encoding="utf-8") as f:
                    config = json.load(f)
                    return {**self.default_config(), **config}
            except (json.JSONDecodeError, OSError):
                return self.default_config()
        return self.default_config()

    def save_config(self, show_message: bool = True) -> None:
        """Save the current settings and editor contents to config.json."""
        self.config["font_size"] = self.config.get("font_size", 11)
        self.config["theme"] = self.config.get("theme", "dark")
        self.config["window_geometry"] = self.root.geometry()
        self.config["last_code"] = self.editor.get("1.0", tk.END).rstrip() + "\n"
        try:
            with open("config.json", "w", encoding="utf-8") as f:
                json.dump(self.config, f, indent=4, ensure_ascii=False)
            self.update_status("Nastavení uloženo.")
            if show_message:
                try:
                    messagebox.showinfo("Uloženo", "Nastavení bylo uloženo.")
                except Exception:
                    # Pokud není možné zobrazit dialog, stačí status
                    pass
        except OSError:
            messagebox.showerror("Chyba", "Nelze uložit konfiguraci do config.json.")

    def open_file(self) -> None:
        path = filedialog.askopenfilename(
            title="Otevřít kód",
            filetypes=[("Vertex soubory", "*.vtx"), ("Všechny soubory", "*")],
        )
        if path:
            try:
                with open(path, "r", encoding="utf-8") as f:
                    code = f.read()
                self.editor.delete("1.0", tk.END)
                self.editor.insert(tk.END, code)
                self.update_status(f"Načteno {os.path.basename(path)}")
            except OSError:
                messagebox.showerror("Chyba", "Nelze načíst soubor.")

    def save_code_as(self) -> None:
        path = filedialog.asksaveasfilename(
            title="Uložit kód jako",
            defaultextension=".vtx",
            filetypes=[("Vertex soubory", "*.vtx"), ("Všechny soubory", "*")],
        )
        if path:
            try:
                with open(path, "w", encoding="utf-8") as f:
                    f.write(self.editor.get("1.0", tk.END).rstrip() + "\n")
                self.update_status(f"Uloženo {os.path.basename(path)}")
                try:
                    messagebox.showinfo("Uloženo", f"Soubor uložen: {os.path.basename(path)}")
                except Exception:
                    pass
            except OSError:
                messagebox.showerror("Chyba", "Nelze uložit soubor.")

    def clear_output(self) -> None:
        self.output.delete("1.0", tk.END)
        self.update_status("Výstup vyčištěn.")

    def reset_settings(self) -> None:
        if messagebox.askyesno("Resetovat nastavení", "Opravdu chcete obnovit výchozí nastavení?"):
            self.config = self.default_config()
            self.editor.configure(font=("Consolas", self.config["font_size"]))
            self.output.configure(font=("Consolas", self.config["font_size"]))
            self.editor.delete("1.0", tk.END)
            self.editor.insert(tk.END, self.config["last_code"])
            self.apply_theme()
            self.update_status("Nastavení obnoveno na výchozí hodnoty.")

    def open_settings_dialog(self) -> None:
        dialog = tk.Toplevel(self.root)
        dialog.title("Nastavení Vertex IDE")
        dialog.configure(bg="#1e1e1e")
        dialog.resizable(False, False)
        dialog.transient(self.root)
        dialog.grab_set()
        dialog.focus_force()

        tk.Label(dialog, text="Téma:", fg="#ffffff", bg="#1e1e1e", font=("Segoe UI", 10, "bold")).grid(row=0, column=0, sticky="w", padx=15, pady=(15, 5))

        theme_var = tk.StringVar(value=self.config.get("theme", "dark"))
        # Set dialog colors according to currently selected theme so options are visible
        if theme_var.get() == "light":
            dlg_bg = "#f3f3f3"
            dlg_text = "#202020"
            selectcol = "#d4d4d4"
        else:
            dlg_bg = "#1e1e1e"
            dlg_text = "#d4d4d4"
            selectcol = "#3c3c3c"

        dialog.configure(bg=dlg_bg)
        tk.Radiobutton(dialog, text="Tmavé", variable=theme_var, value="dark", fg=dlg_text, bg=dlg_bg, selectcolor=selectcol).grid(row=1, column=0, sticky="w", padx=20)
        tk.Radiobutton(dialog, text="Světlé", variable=theme_var, value="light", fg=dlg_text, bg=dlg_bg, selectcolor=selectcol).grid(row=2, column=0, sticky="w", padx=20)

        tk.Label(dialog, text="Velikost písma:", fg="#ffffff", bg="#1e1e1e", font=("Segoe UI", 10, "bold")).grid(row=3, column=0, sticky="w", padx=15, pady=(10, 5))
        font_size_var = tk.IntVar(value=self.config.get("font_size", 11))
        tk.Spinbox(dialog, from_=8, to=20, textvariable=font_size_var, width=5).grid(row=4, column=0, sticky="w", padx=20)

        # Ukázkový text, aby uživatel viděl změnu písma
        sample_label = tk.Label(dialog, text="Ukázkový text: 123 ABC xyz", fg=dlg_text, bg=dlg_bg)
        sample_label.grid(row=4, column=1, sticky="w", padx=10)
        sample_label.configure(font=("Consolas", font_size_var.get()))

        def apply_changes() -> None:
            self.config["theme"] = theme_var.get()
            self.config["font_size"] = font_size_var.get()
            self.editor.configure(font=("Consolas", self.config["font_size"]))
            self.output.configure(font=("Consolas", self.config["font_size"]))
            self.apply_theme()
            # Update sample label font immediately so user sees change
            sample_label.configure(font=("Consolas", self.config["font_size"]))
            self.update_status("Nastavení upraveno.")
            # Save configuration (this will show single informational alert)
            try:
                self.save_config()
            except Exception:
                pass
            # Do NOT destroy the dialog; let the user close it when ready

        tk.Button(dialog, text="Uložit", command=apply_changes, bg="#0e639c", fg="white", relief="flat", padx=10, pady=5).grid(row=5, column=0, sticky="e", padx=15, pady=15)

    def apply_theme(self) -> None:
        theme = self.config.get("theme", "dark")
        if theme == "light":
            bg = "#f3f3f3"
            text = "#202020"
            editor_bg = "#ffffff"
            output_bg = "#f7f7f7"
        else:
            bg = "#1e1e1e"
            text = "#d4d4d4"
            editor_bg = "#2d2d2d"
            output_bg = "#1e1e1e"

        self.root.configure(bg=bg)
        for widget in [self.status_label]:
            widget.configure(bg=bg, fg=text)
        self.editor.configure(bg=editor_bg, fg=text, insertbackground=text)
        self.output.configure(bg=output_bg, fg="#a3dda3", insertbackground=text)

    def update_status(self, message: str) -> None:
        self.status_var.set(message)

    def show_about(self) -> None:
        messagebox.showinfo(
            "O aplikaci",
            "Vertex IDE Pro\n\nRozhraní pro jednoduchý interpret jazyka Vertex\n• uložené nastavení\n• reset prostředí\n• ukládání a načítání kódu",
        )
