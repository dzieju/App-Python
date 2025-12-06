"""Main launcher application using Tkinter (standard library)."""

import os
from pathlib import Path
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog
from config import ConfigManager, get_app_dir
from runner import ProcessRunner

# Constants
LOG_SEPARATOR = "=" * 50


class LauncherApp:
    """Main launcher application class using Tkinter."""

    def __init__(self, root: tk.Tk):
        """Initialize the launcher application.

        Args:
            root: The Tkinter root window.
        """
        self.root = root
        self.root.title("Python Script Launcher")
        self.root.geometry("700x500")
        self.root.minsize(600, 400)

        self.config = ConfigManager()
        self.runner = ProcessRunner(python_executable=self.config.python_executable)

        self.current_script = None
        self.log_content = ""
        self.entry_buttons = []

        self._create_widgets()
        self._start_update_loop()

        # Handle window close
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)

    def _create_widgets(self) -> None:
        """Create all GUI widgets."""
        # Main frame
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Title label
        title_label = ttk.Label(
            self.main_frame,
            text="Launcher Application",
            font=("Helvetica", 16, "bold")
        )
        title_label.pack(pady=(0, 10))

        # Separator
        ttk.Separator(self.main_frame, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=5)

        # Button frame for dynamic entry buttons
        self.button_frame = ttk.Frame(self.main_frame)
        self.button_frame.pack(fill=tk.X, pady=10)

        # Style configuration for buttons
        style = ttk.Style()
        style.configure("Green.TButton", foreground="dark green")
        style.configure("Blue.TButton", foreground="dark blue")
        style.configure("Red.TButton", foreground="dark red")

        # Create entry buttons dynamically
        self._refresh_entry_buttons()

        # Control buttons frame (Stop + Config)
        control_frame = ttk.Frame(self.main_frame)
        control_frame.pack(fill=tk.X, pady=5)

        self.btn_stop = ttk.Button(
            control_frame,
            text="Zatrzymaj",
            command=self._on_stop,
            width=15,
            style="Red.TButton",
            state=tk.DISABLED
        )
        self.btn_stop.pack(side=tk.LEFT, padx=5)

        self.btn_config = ttk.Button(
            control_frame,
            text="Konfiguracja",
            command=self._on_config,
            width=15
        )
        self.btn_config.pack(side=tk.RIGHT, padx=5)

        # Separator
        ttk.Separator(self.main_frame, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=5)

        # Log label
        log_label = ttk.Label(
            self.main_frame,
            text="Output Log:",
            font=("Helvetica", 10, "bold")
        )
        log_label.pack(anchor=tk.W)

        # Log text area with scrollbar
        self.log_text = scrolledtext.ScrolledText(
            self.main_frame,
            height=15,
            font=("Courier New", 9),
            state=tk.DISABLED,
            wrap=tk.WORD
        )
        self.log_text.pack(fill=tk.BOTH, expand=True, pady=5)

        # Bottom frame
        bottom_frame = ttk.Frame(self.main_frame)
        bottom_frame.pack(fill=tk.X, pady=5)

        # Clear log button
        self.btn_clear = ttk.Button(
            bottom_frame,
            text="Wyczyść log",
            command=self._on_clear
        )
        self.btn_clear.pack(side=tk.LEFT)

        # Status label
        self.status_label = ttk.Label(
            bottom_frame,
            text="Status: Gotowy",
            font=("Helvetica", 10)
        )
        self.status_label.pack(side=tk.RIGHT)

    def _refresh_entry_buttons(self) -> None:
        """Refresh the dynamic entry buttons from config entries."""
        # Clear existing buttons
        for btn in self.entry_buttons:
            btn.destroy()
        self.entry_buttons.clear()

        # Create buttons from entries
        entries = self.config.entries
        styles = ["Green.TButton", "Blue.TButton"]

        for i, entry in enumerate(entries):
            style = styles[i % len(styles)]
            btn = ttk.Button(
                self.button_frame,
                text=entry.get("name", f"Entry {i+1}"),
                command=lambda idx=i: self._on_entry_click(idx),
                width=15,
                style=style
            )
            btn.pack(side=tk.LEFT, padx=5)
            self.entry_buttons.append(btn)

    def _on_entry_click(self, index: int) -> None:
        """Handle entry button click.

        Args:
            index: Index of the entry in the config.
        """
        entries = self.config.entries
        if index >= len(entries):
            return

        entry = entries[index]
        script_path = entry.get("script_path", "")
        working_dir = entry.get("working_dir", "")
        args = entry.get("args", "")
        name = entry.get("name", f"Entry {index+1}")

        # Resolve relative paths
        app_dir = get_app_dir()
        if script_path and not os.path.isabs(script_path):
            script_path = str(app_dir / script_path)
        if working_dir and not os.path.isabs(working_dir):
            working_dir = str(app_dir / working_dir)

        if script_path and self.runner.start(script_path, cwd=working_dir if working_dir else None, args=args):
            self.current_script = name
            self.status_label.config(text=f"Status: Uruchomiono {name}...")
            self._set_buttons_state(tk.DISABLED)
            self.btn_stop.config(state=tk.NORMAL)
            self._append_to_log(f"\n{LOG_SEPARATOR}\nUruchamianie {name}...\n{LOG_SEPARATOR}\n")

    def _set_buttons_state(self, state) -> None:
        """Set state for all entry buttons.

        Args:
            state: The button state (tk.NORMAL or tk.DISABLED).
        """
        for btn in self.entry_buttons:
            btn.config(state=state)

    def _start_update_loop(self) -> None:
        """Start the update loop to check process output."""
        self._update()

    def _update(self) -> None:
        """Update the log with process output and check process status."""
        # Update log with process output
        if self.runner.is_running:
            output = self.runner.get_output()
            if output:
                self._append_to_log(output)

        # Check if process finished
        if self.current_script and not self.runner.is_running:
            self.status_label.config(text=f"Status: {self.current_script} zakończone")
            self._set_buttons_state(tk.NORMAL)
            self.btn_stop.config(state=tk.DISABLED)
            self.current_script = None

        # Schedule next update using after() directly
        self.root.after(100, self._update)

    def _append_to_log(self, text: str) -> None:
        """Append text to the log widget efficiently.

        Args:
            text: The text to append to the log.
        """
        self.log_content += text
        # Limit log size
        lines = self.log_content.split("\n")
        max_lines = self.config.get("log_max_lines", 1000)
        if len(lines) > max_lines:
            self.log_content = "\n".join(lines[-max_lines:])
            # Full refresh needed when truncating
            self._update_log_display()
        else:
            # Efficient append - only add new content
            self.log_text.config(state=tk.NORMAL)
            self.log_text.insert(tk.END, text)
            self.log_text.see(tk.END)
            self.log_text.config(state=tk.DISABLED)

    def _update_log_display(self) -> None:
        """Update the log text widget with full content refresh."""
        self.log_text.config(state=tk.NORMAL)
        self.log_text.delete(1.0, tk.END)
        self.log_text.insert(tk.END, self.log_content)
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)

    def _on_stop(self) -> None:
        """Handle Stop button click."""
        if self.runner.is_running:
            self.runner.stop()
            self._append_to_log(f"\n[ZATRZYMANO] {self.current_script} zostało zatrzymane przez użytkownika.\n")
            self.status_label.config(text="Status: Zatrzymano")
            self._set_buttons_state(tk.NORMAL)
            self.btn_stop.config(state=tk.DISABLED)
            self.current_script = None

    def _on_clear(self) -> None:
        """Handle Clear Log button click."""
        self.log_content = ""
        self._update_log_display()

    def _on_config(self) -> None:
        """Handle Configuration button click."""
        ConfigWindow(self.root, self.config, self._refresh_entry_buttons)

    def _on_close(self) -> None:
        """Handle window close event."""
        self.runner.stop()
        self.root.destroy()


class ConfigWindow:
    """Configuration window dialog."""

    def __init__(self, parent: tk.Tk, config: ConfigManager, on_refresh_callback=None):
        """Initialize the configuration window.

        Args:
            parent: The parent window.
            config: The configuration manager instance.
            on_refresh_callback: Callback to refresh main window buttons.
        """
        self.config = config
        self.on_refresh_callback = on_refresh_callback

        self.window = tk.Toplevel(parent)
        self.window.title("Konfiguracja")
        self.window.geometry("550x450")
        self.window.resizable(True, True)
        self.window.transient(parent)
        self.window.grab_set()

        self._create_widgets()

    def _create_widgets(self) -> None:
        """Create configuration window widgets."""
        main_frame = ttk.Frame(self.window, padding="15")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Title
        title_label = ttk.Label(
            main_frame,
            text="Ustawienia aplikacji",
            font=("Helvetica", 14, "bold")
        )
        title_label.pack(pady=(0, 15))

        # Python executable
        py_frame = ttk.LabelFrame(main_frame, text="Python", padding="10")
        py_frame.pack(fill=tk.X, pady=5)

        ttk.Label(py_frame, text="Ścieżka do Python:").pack(anchor=tk.W)
        self.py_entry = ttk.Entry(py_frame, width=50)
        self.py_entry.insert(0, self.config.python_executable)
        self.py_entry.pack(fill=tk.X, pady=2)

        # Entries list frame
        entries_frame = ttk.LabelFrame(main_frame, text="Wpisy menu", padding="10")
        entries_frame.pack(fill=tk.BOTH, expand=True, pady=5)

        # Listbox with scrollbar
        list_frame = ttk.Frame(entries_frame)
        list_frame.pack(fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.entries_listbox = tk.Listbox(list_frame, yscrollcommand=scrollbar.set, height=8)
        self.entries_listbox.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.entries_listbox.yview)

        self._refresh_entries_list()

        # Entry buttons
        entry_btn_frame = ttk.Frame(entries_frame)
        entry_btn_frame.pack(fill=tk.X, pady=5)

        ttk.Button(
            entry_btn_frame,
            text="Dodaj wpis",
            command=self._on_add_entry
        ).pack(side=tk.LEFT, padx=2)

        ttk.Button(
            entry_btn_frame,
            text="Edytuj",
            command=self._on_edit_entry
        ).pack(side=tk.LEFT, padx=2)

        ttk.Button(
            entry_btn_frame,
            text="Usuń",
            command=self._on_remove_entry
        ).pack(side=tk.LEFT, padx=2)

        # Bottom buttons
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=tk.X, pady=15)

        ttk.Button(
            btn_frame,
            text="Zapisz",
            command=self._on_save
        ).pack(side=tk.RIGHT, padx=5)

        ttk.Button(
            btn_frame,
            text="Anuluj",
            command=self.window.destroy
        ).pack(side=tk.RIGHT, padx=5)

    def _refresh_entries_list(self) -> None:
        """Refresh the entries listbox."""
        self.entries_listbox.delete(0, tk.END)
        for entry in self.config.entries:
            name = entry.get("name", "Unnamed")
            script = entry.get("script_path", "")
            self.entries_listbox.insert(tk.END, f"{name} - {script}")

    def _on_add_entry(self) -> None:
        """Handle Add Entry button click."""
        dialog = EntryDialog(self.window, self.config)
        self.window.wait_window(dialog.window)
        if dialog.result:
            self.config.add_entry(**dialog.result)
            self.config.save()
            self._refresh_entries_list()
            if self.on_refresh_callback:
                self.on_refresh_callback()

    def _on_edit_entry(self) -> None:
        """Handle Edit Entry button click."""
        selection = self.entries_listbox.curselection()
        if not selection:
            messagebox.showwarning("Ostrzeżenie", "Wybierz wpis do edycji.")
            return

        index = selection[0]
        entries = self.config.entries
        if index >= len(entries):
            return

        entry = entries[index]
        dialog = EntryDialog(self.window, self.config, entry)
        self.window.wait_window(dialog.window)
        if dialog.result:
            self.config.update_entry(index, **dialog.result)
            self.config.save()
            self._refresh_entries_list()
            if self.on_refresh_callback:
                self.on_refresh_callback()

    def _on_remove_entry(self) -> None:
        """Handle Remove Entry button click."""
        selection = self.entries_listbox.curselection()
        if not selection:
            messagebox.showwarning("Ostrzeżenie", "Wybierz wpis do usunięcia.")
            return

        index = selection[0]
        if messagebox.askyesno("Potwierdzenie", "Czy na pewno chcesz usunąć ten wpis?"):
            self.config.remove_entry(index)
            self.config.save()
            self._refresh_entries_list()
            if self.on_refresh_callback:
                self.on_refresh_callback()

    def _on_save(self) -> None:
        """Handle Save button click."""
        py_path = self.py_entry.get().strip()

        # Validate that fields are not empty
        if not py_path:
            messagebox.showwarning("Ostrzeżenie", "Ścieżka do Python nie może być pusta.")
            return

        self.config.set("python_executable", py_path)
        self.config.save()
        messagebox.showinfo("Sukces", "Konfiguracja została zapisana.")
        if self.on_refresh_callback:
            self.on_refresh_callback()
        self.window.destroy()


class EntryDialog:
    """Dialog for adding or editing a menu entry."""

    def __init__(self, parent, config: ConfigManager, entry: dict = None):
        """Initialize the entry dialog.

        Args:
            parent: The parent window.
            config: The configuration manager instance.
            entry: Existing entry to edit (None for new entry).
        """
        self.config = config
        self.result = None
        self.app_dir = get_app_dir()
        self.last_browse_dir = str(self.app_dir)

        self.window = tk.Toplevel(parent)
        self.window.title("Edytuj wpis" if entry else "Dodaj wpis")
        self.window.geometry("500x350")
        self.window.resizable(False, False)
        self.window.transient(parent)
        self.window.grab_set()

        self._create_widgets(entry)

    def _create_widgets(self, entry: dict = None) -> None:
        """Create dialog widgets.

        Args:
            entry: Existing entry data to prefill (None for new entry).
        """
        main_frame = ttk.Frame(self.window, padding="15")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Name field
        ttk.Label(main_frame, text="Nazwa:").pack(anchor=tk.W)
        self.name_entry = ttk.Entry(main_frame, width=50)
        self.name_entry.pack(fill=tk.X, pady=2)
        if entry:
            self.name_entry.insert(0, entry.get("name", ""))

        # Script path field with browse button
        ttk.Label(main_frame, text="Ścieżka do skryptu:").pack(anchor=tk.W, pady=(10, 0))
        script_frame = ttk.Frame(main_frame)
        script_frame.pack(fill=tk.X, pady=2)

        self.script_entry = ttk.Entry(script_frame, width=40)
        self.script_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        if entry:
            self.script_entry.insert(0, entry.get("script_path", ""))

        ttk.Button(
            script_frame,
            text="Wybierz...",
            command=self._browse_script
        ).pack(side=tk.RIGHT, padx=5)

        # Working directory field with browse button
        ttk.Label(main_frame, text="Katalog roboczy (opcjonalnie):").pack(anchor=tk.W, pady=(10, 0))
        cwd_frame = ttk.Frame(main_frame)
        cwd_frame.pack(fill=tk.X, pady=2)

        self.cwd_entry = ttk.Entry(cwd_frame, width=40)
        self.cwd_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        if entry:
            self.cwd_entry.insert(0, entry.get("working_dir", ""))

        ttk.Button(
            cwd_frame,
            text="Wybierz...",
            command=self._browse_cwd
        ).pack(side=tk.RIGHT, padx=5)

        # Interpreter field
        ttk.Label(main_frame, text="Interpreter (opcjonalnie):").pack(anchor=tk.W, pady=(10, 0))
        self.interpreter_entry = ttk.Entry(main_frame, width=50)
        self.interpreter_entry.pack(fill=tk.X, pady=2)
        if entry:
            self.interpreter_entry.insert(0, entry.get("interpreter", ""))

        # Args field
        ttk.Label(main_frame, text="Argumenty (opcjonalnie):").pack(anchor=tk.W, pady=(10, 0))
        self.args_entry = ttk.Entry(main_frame, width=50)
        self.args_entry.pack(fill=tk.X, pady=2)
        if entry:
            self.args_entry.insert(0, entry.get("args", ""))

        # Relative path checkbox
        self.relative_var = tk.BooleanVar(value=True)
        self.relative_check = ttk.Checkbutton(
            main_frame,
            text="Zapisz ścieżkę względnie do folderu aplikacji",
            variable=self.relative_var
        )
        self.relative_check.pack(anchor=tk.W, pady=10)

        # Buttons
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=tk.X, pady=10)

        ttk.Button(
            btn_frame,
            text="OK",
            command=self._on_ok
        ).pack(side=tk.RIGHT, padx=5)

        ttk.Button(
            btn_frame,
            text="Anuluj",
            command=self._on_cancel
        ).pack(side=tk.RIGHT, padx=5)

    def _browse_script(self) -> None:
        """Open file dialog to select a script."""
        initial_dir = self.last_browse_dir
        filepath = filedialog.askopenfilename(
            parent=self.window,
            title="Wybierz skrypt Python",
            initialdir=initial_dir,
            filetypes=[("Python files", "*.py"), ("All files", "*.*")]
        )
        if filepath:
            self.last_browse_dir = os.path.dirname(filepath)
            self.script_entry.delete(0, tk.END)
            self.script_entry.insert(0, filepath)

    def _browse_cwd(self) -> None:
        """Open folder dialog to select working directory."""
        initial_dir = self.last_browse_dir
        dirpath = filedialog.askdirectory(
            parent=self.window,
            title="Wybierz katalog roboczy",
            initialdir=initial_dir
        )
        if dirpath:
            self.last_browse_dir = dirpath
            self.cwd_entry.delete(0, tk.END)
            self.cwd_entry.insert(0, dirpath)

    def _on_ok(self) -> None:
        """Handle OK button click."""
        name = self.name_entry.get().strip()
        script_path = self.script_entry.get().strip()
        working_dir = self.cwd_entry.get().strip()
        interpreter = self.interpreter_entry.get().strip()
        args = self.args_entry.get().strip()

        if not name:
            messagebox.showwarning("Ostrzeżenie", "Nazwa nie może być pusta.")
            return

        if not script_path:
            messagebox.showwarning("Ostrzeżenie", "Ścieżka do skryptu nie może być pusta.")
            return

        # Convert to relative path if checkbox is checked
        if self.relative_var.get():
            script_path = self._make_relative(script_path)
            if working_dir:
                working_dir = self._make_relative(working_dir)

        self.result = {
            "name": name,
            "script_path": script_path,
            "working_dir": working_dir,
            "interpreter": interpreter,
            "args": args
        }
        self.window.destroy()

    def _make_relative(self, path: str) -> str:
        """Convert an absolute path to relative if possible.

        Args:
            path: The path to convert.

        Returns:
            Relative path if under app_dir, otherwise the original path.
        """
        try:
            p = Path(path).resolve()
            rel = p.relative_to(self.app_dir)
            return str(rel).replace("\\", "/")
        except ValueError:
            # Path is not under app_dir, return as-is
            return path

    def _on_cancel(self) -> None:
        """Handle Cancel button click."""
        self.window.destroy()


def main():
    """Main function to run the launcher application."""
    root = tk.Tk()
    LauncherApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
