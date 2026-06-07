"""Grafické uživatelské rozhraní Vertex IDE: úvodní stránka a editor."""

import tkinter as tk
from tkinter import scrolledtext, filedialog, messagebox
import json
import os
from typing import Callable, Dict, Any

class VertexGUI:
    """Class handling the layout and behavior of the main Tkinter window."""
    
    def __init__(self, root: tk.Tk, run_callback: Callable[[], None], reset_callback: Callable[[], None]) -> None:
        """Inicializuje GUI, úvodní obrazovku a hlavní editor.

        Parametry:
            root: hlavní okno tkinter
            run_callback: callback pro spuštění kódu
            reset_callback: callback pro reset prostředí
        """
        self.root: tk.Tk = root
        self.root.title("Vertex IDE Pro - Nový soubor")
        self.default_code: str = (
            "x = 10 ;\ny = 20 ;\nz = x + y * 20 ;\nprint z ;\n\nprint 10 + 20 + 30 ;\n\n"
            "for (i = 0; i < 3; i = i + 1) {\n    print i ;\n}"
        )
        self.config: Dict[str, Any] = self.load_config()
        self.root.geometry(self.config.get("window_geometry", "850x650+100+100"))
        self.root.configure(bg="#1e1e1e")
        self.reset_callback = reset_callback
        self.run_callback = run_callback

        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        self.create_menu()
        self.create_intro_screen()
        self.create_main_screen()
        self.show_intro_screen()
        self.apply_theme()

    def create_intro_screen(self) -> None:
        self.intro_frame = tk.Frame(self.root, bg="#1e1e1e")
        self.intro_frame.grid(row=0, column=0, sticky="nsew")

        title = tk.Label(
            self.intro_frame,
            text="Vítejte v Vertex IDE Pro",
            fg="#ffffff",
            bg="#1e1e1e",
            font=("Segoe UI", 18, "bold")
        )
        title.pack(pady=(80, 10))

        subtitle = tk.Label(
            self.intro_frame,
            text="Rychlý interpret jazyka Vertex. Klikněte na tlačítko pro otevření editoru.",
            fg="#d4d4d4",
            bg="#1e1e1e",
            font=("Segoe UI", 11)
        )
        subtitle.pack(pady=(0, 30), padx=40)

        start_btn = tk.Button(
            self.intro_frame,
            text="Otevřít Vertex editor",
            command=self.show_main_screen,
            bg="#0e639c",
            fg="white",
            font=("Segoe UI", 12, "bold"),
            relief="flat",
            padx=20,
            pady=10
        )
        start_btn.pack()

        hint = tk.Label(
            self.intro_frame,
            text="Můžete také použít klávesu F5 pro spuštění kódu, až budete v editoru.",
            fg="#a3a3a3",
            bg="#1e1e1e",
            font=("Segoe UI", 9)
        )
        hint.pack(pady=(20, 0))

    def create_main_screen(self) -> None:
        self.main_frame = tk.Frame(self.root, bg="#1e1e1e")
        self.main_frame.grid(row=0, column=0, sticky="nsew")

        self.banner_frame = tk.Frame(self.main_frame, bg="#0e639c", height=44)
        self.banner_frame.grid(row=0, column=0, sticky="ew")
        self.banner_frame.grid_propagate(False)
        self.banner_label = tk.Label(self.banner_frame, text="Vertex IDE Pro", fg="#ffffff", bg="#0e639c", font=("Segoe UI", 12, "bold"))
        self.banner_label.pack(side="left", padx=15, pady=8)

        self.main_frame.grid_rowconfigure(2, weight=3)
        self.main_frame.grid_rowconfigure(5, weight=2)
        self.main_frame.grid_columnconfigure(0, weight=1)

        lbl_editor = tk.Label(self.main_frame, text="KÓD EDITOR", fg="#ffffff", bg="#1e1e1e", font=("Consolas", 10, "bold"))
        lbl_editor.grid(row=1, column=0, sticky="w", padx=15, pady=(12, 5))
        
        self.editor = scrolledtext.ScrolledText(
            self.main_frame, 
            bg="#2d2d2d", 
            fg="#d4d4d4", 
            insertbackground="white",
            font=("Consolas", self.config.get("font_size", 11)),
            wrap="none"
        )
        self.editor.grid(row=2, column=0, sticky="nsew", padx=15, pady=5)
        self.editor.insert(tk.END, self.config.get("last_code", self.default_code))

        self.run_btn = tk.Button(
            self.main_frame, 
            text="SPUSTIT KÓD (F5)", 
            command=self.run_callback, 
            bg="#0e639c", 
            fg="white",
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            padx=10,
            pady=5
        )
        self.run_btn.grid(row=3, column=0, pady=15)
        self.root.bind("<F5>", lambda e: self.run_callback())
        self.root.bind("<Control-s>", lambda e: self.save_code_as())

        lbl_output = tk.Label(self.main_frame, text="VÝSTUP", fg="#ffffff", bg="#1e1e1e", font=("Consolas", 10, "bold"))
        lbl_output.grid(row=4, column=0, sticky="w", padx=15, pady=(10, 5))

        self.output = scrolledtext.ScrolledText(
            self.main_frame, 
            bg="#1e1e1e", 
            fg="#a3dda3", 
            insertbackground="white",
            font=("Consolas", self.config.get("font_size", 11)),
            relief="sunken",
            wrap="none"
        )
        self.output.grid(row=5, column=0, sticky="nsew", padx=15, pady=(5, 5))

        self.status_var = tk.StringVar(value="Ready")
        self.status_label = tk.Label(self.main_frame, textvariable=self.status_var, fg="#d4d4d4", bg="#1e1e1e", font=("Segoe UI", 9))
        self.status_label.grid(row=6, column=0, sticky="ew", padx=15, pady=(0, 10))

    def show_intro_screen(self) -> None:
        try:
            self.root.config(menu="")
        except Exception:
            pass
        self.main_frame.grid_remove()
        self.intro_frame.grid()
        self.update_status("Vítejte. Klikněte na tlačítko pro otevření editoru.")

    def show_main_screen(self) -> None:
        try:
            self.root.config(menu=self.menu_bar)
        except Exception:
            pass
        self.intro_frame.grid_remove()
        self.main_frame.grid()
        self.update_status("Editor je připraven. Použijte F5 pro spuštění.")

    def create_menu(self) -> None:
        self.menu_bar = tk.Menu(self.root)

        file_menu = tk.Menu(self.menu_bar, tearoff=0)
        file_menu.add_command(label="Otevřít kód...", command=self.open_file)
        file_menu.add_command(label="Uložit kód jako...", command=self.save_code_as)
        file_menu.add_command(label="Exportovat výstup...", command=self.export_output)
        file_menu.add_separator()
        file_menu.add_command(label="Uložit nastavení", command=self.save_config)
        file_menu.add_command(label="Resetovat nastavení", command=self.reset_settings)
        file_menu.add_separator()
        file_menu.add_command(label="Ukončit", command=self.root.quit)
        self.menu_bar.add_cascade(label="Soubor", menu=file_menu)

        edit_menu = tk.Menu(self.menu_bar, tearoff=0)
        edit_menu.add_command(label="Vyčistit výstup", command=self.clear_output)
        edit_menu.add_command(label="Resetovat prostředí", command=self.reset_callback)
        self.menu_bar.add_cascade(label="Upravit", menu=edit_menu)

        settings_menu = tk.Menu(self.menu_bar, tearoff=0)
        settings_menu.add_command(label="Nastavení", command=self.open_settings_dialog)
        self.menu_bar.add_cascade(label="Nastavení", menu=settings_menu)

        help_menu = tk.Menu(self.menu_bar, tearoff=0)
        help_menu.add_command(label="O aplikaci", command=self.show_about)
        self.menu_bar.add_cascade(label="Nápověda", menu=help_menu)

    def default_config(self) -> Dict[str, Any]:
        return {
            "theme": "dark",
            "font_size": 11,
            "window_geometry": "850x650+100+100",
            "last_code": self.default_code,
        }

    def load_config(self) -> Dict[str, Any]:
        """Načte konfiguraci z config.json nebo použije výchozí hodnoty."""
        if os.path.exists("config.json"):
            try:
                with open("config.json", "r", encoding="utf-8") as f:
                    config = json.load(f)
                    return {**self.default_config(), **config}
            except (json.JSONDecodeError, OSError):
                return self.default_config()
        return self.default_config()

    def save_config(self, show_message: bool = True) -> None:
        """Uloží konfiguraci do config.json."""
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
                self.root.title(f"Vertex IDE Pro - {os.path.basename(path)}")
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
                self.root.title(f"Vertex IDE Pro - {os.path.basename(path)}")
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
        if theme_var.get() == "light":
            dlg_bg = "#f3f3f3"
            dlg_text = "#202020"
            selectcol = "#d4d4d4"
        else:
            dlg_bg = "#1e1e1e"
            dlg_text = "#d4d4d4"
            selectcol = "#3c3c3c"

        dialog.configure(bg=dlg_bg)
        rb_dark = tk.Radiobutton(dialog, text="Tmavé", variable=theme_var, value="dark", fg=dlg_text, bg=dlg_bg, selectcolor=selectcol)
        rb_dark.grid(row=1, column=0, sticky="w", padx=20)
        rb_light = tk.Radiobutton(dialog, text="Světlé", variable=theme_var, value="light", fg=dlg_text, bg=dlg_bg, selectcolor=selectcol)
        rb_light.grid(row=2, column=0, sticky="w", padx=20)

        tk.Label(dialog, text="Velikost písma:", fg="#ffffff", bg="#1e1e1e", font=("Segoe UI", 10, "bold")).grid(row=3, column=0, sticky="w", padx=15, pady=(10, 5))
        font_size_var = tk.IntVar(value=self.config.get("font_size", 11))
        tk.Spinbox(dialog, from_=8, to=20, textvariable=font_size_var, width=5).grid(row=4, column=0, sticky="w", padx=20)

        sample_label = tk.Label(dialog, text="Ukázkový text: 123 ABC xyz", fg=dlg_text, bg=dlg_bg)
        sample_label.grid(row=4, column=1, sticky="w", padx=10)
        sample_label.configure(font=("Consolas", font_size_var.get()))

        def on_theme_change(*_args) -> None:
            if theme_var.get() == "light":
                new_bg = "#f3f3f3"
                new_text = "#202020"
                new_select = "#d4d4d4"
            else:
                new_bg = "#1e1e1e"
                new_text = "#d4d4d4"
                new_select = "#3c3c3c"
            try:
                dialog.configure(bg=new_bg)
                rb_dark.configure(bg=new_bg, fg=new_text, selectcolor=new_select)
                rb_light.configure(bg=new_bg, fg=new_text, selectcolor=new_select)
                sample_label.configure(bg=new_bg, fg=new_text)
            except Exception:
                pass

        theme_var.trace("w", on_theme_change)

        def apply_changes() -> None:
            self.config["theme"] = theme_var.get()
            self.config["font_size"] = font_size_var.get()
            self.editor.configure(font=("Consolas", self.config["font_size"]))
            self.output.configure(font=("Consolas", self.config["font_size"]))
            self.apply_theme()
            sample_label.configure(font=("Consolas", self.config["font_size"]))
            self.update_status("Nastavení upraveno.")
            try:
                self.save_config()
            except Exception:
                pass

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
        output_fg = "#a3dda3" if theme != "light" else "#064e04"
        self.output.configure(bg=output_bg, fg=output_fg, insertbackground=text)

    def clear_error_highlight(self) -> None:
        try:
            self.editor.tag_remove("vertex_error", "1.0", tk.END)
        except Exception:
            pass

    def highlight_error(self, line: int | None) -> None:
        if line is None:
            return
        self.clear_error_highlight()
        if self.config.get("theme", "dark") == "light":
            err_bg = "#ffcccc"
            err_fg = "#800000"
        else:
            err_bg = "#6b0000"
            err_fg = "#ffffff"
        self.editor.tag_configure("vertex_error", background=err_bg, foreground=err_fg)
        start = f"{line}.0"
        end = f"{line}.end"
        try:
            self.editor.tag_add("vertex_error", start, end)
            self.editor.see(start)
        except Exception:
            pass

    def export_output(self) -> None:
        path = filedialog.asksaveasfilename(
            title="Exportovat výstup",
            defaultextension=".txt",
            filetypes=[("Textové soubory", "*.txt"), ("Všechny soubory", "*")],
        )
        if path:
            try:
                with open(path, "w", encoding="utf-8") as f:
                    f.write(self.output.get("1.0", tk.END))
                self.update_status(f"Výstup exportován: {os.path.basename(path)}")
                try:
                    messagebox.showinfo("Exportováno", "Výstup byl uložen.")
                except Exception:
                    pass
            except OSError:
                messagebox.showerror("Chyba", "Nelze exportovat výstup.")

    def update_status(self, message: str) -> None:
        self.status_var.set(message)

    def show_about(self) -> None:
        messagebox.showinfo(
            "O aplikaci",
            "Vertex IDE Pro\n\nRozhraní pro jednoduchý interpret jazyka Vertex\n• uložené nastavení\n• reset prostředí\n• ukládání a načítání kódu",
        )
