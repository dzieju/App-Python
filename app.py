"""Main launcher application using Tkinter (standard library)."""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from config import ConfigManager
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

        self._create_widgets()
        self._start_update_loop()

        # Handle window close
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)

    def _create_widgets(self) -> None:
        """Create all GUI widgets."""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Title label
        title_label = ttk.Label(
            main_frame,
            text="Launcher Application",
            font=("Helvetica", 16, "bold")
        )
        title_label.pack(pady=(0, 10))

        # Separator
        ttk.Separator(main_frame, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=5)

        # Button frame
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=10)

        # Style configuration for buttons
        style = ttk.Style()
        style.configure("Green.TButton", foreground="dark green")
        style.configure("Blue.TButton", foreground="dark blue")
        style.configure("Red.TButton", foreground="dark red")

        # Buttons
        self.btn_zlecenia = ttk.Button(
            button_frame,
            text="Zlecenia",
            command=self._on_zlecenia,
            width=15,
            style="Green.TButton"
        )
        self.btn_zlecenia.pack(side=tk.LEFT, padx=5)

        self.btn_faktury = ttk.Button(
            button_frame,
            text="Faktury",
            command=self._on_faktury,
            width=15,
            style="Blue.TButton"
        )
        self.btn_faktury.pack(side=tk.LEFT, padx=5)

        self.btn_stop = ttk.Button(
            button_frame,
            text="Zatrzymaj",
            command=self._on_stop,
            width=15,
            style="Red.TButton",
            state=tk.DISABLED
        )
        self.btn_stop.pack(side=tk.LEFT, padx=5)

        self.btn_config = ttk.Button(
            button_frame,
            text="Konfiguracja",
            command=self._on_config,
            width=15
        )
        self.btn_config.pack(side=tk.RIGHT, padx=5)

        # Separator
        ttk.Separator(main_frame, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=5)

        # Log label
        log_label = ttk.Label(
            main_frame,
            text="Output Log:",
            font=("Helvetica", 10, "bold")
        )
        log_label.pack(anchor=tk.W)

        # Log text area with scrollbar
        self.log_text = scrolledtext.ScrolledText(
            main_frame,
            height=15,
            font=("Courier New", 9),
            state=tk.DISABLED,
            wrap=tk.WORD
        )
        self.log_text.pack(fill=tk.BOTH, expand=True, pady=5)

        # Bottom frame
        bottom_frame = ttk.Frame(main_frame)
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

    def _start_update_loop(self) -> None:
        """Start the update loop to check process output."""
        self._update()
        self.root.after(100, self._start_update_loop)

    def _update(self) -> None:
        """Update the log with process output and check process status."""
        # Update log with process output
        if self.runner.is_running:
            output = self.runner.get_output()
            if output:
                self.log_content += output
                # Limit log size
                lines = self.log_content.split("\n")
                max_lines = self.config.get("log_max_lines", 1000)
                if len(lines) > max_lines:
                    self.log_content = "\n".join(lines[-max_lines:])
                self._update_log_display()

        # Check if process finished
        if self.current_script and not self.runner.is_running:
            self.status_label.config(text=f"Status: {self.current_script} zakończone")
            self.btn_zlecenia.config(state=tk.NORMAL)
            self.btn_faktury.config(state=tk.NORMAL)
            self.btn_stop.config(state=tk.DISABLED)
            self.current_script = None

    def _update_log_display(self) -> None:
        """Update the log text widget with current content."""
        self.log_text.config(state=tk.NORMAL)
        self.log_text.delete(1.0, tk.END)
        self.log_text.insert(tk.END, self.log_content)
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)

    def _on_zlecenia(self) -> None:
        """Handle Zlecenia button click."""
        script_path = self.config.scripts.get("zlecenia")
        if script_path and self.runner.start(script_path):
            self.current_script = "Zlecenia"
            self.status_label.config(text="Status: Uruchomiono Zlecenia...")
            self.btn_zlecenia.config(state=tk.DISABLED)
            self.btn_faktury.config(state=tk.DISABLED)
            self.btn_stop.config(state=tk.NORMAL)
            self.log_content += f"\n{LOG_SEPARATOR}\nUruchamianie Zlecenia...\n{LOG_SEPARATOR}\n"
            self._update_log_display()

    def _on_faktury(self) -> None:
        """Handle Faktury button click."""
        script_path = self.config.scripts.get("faktury")
        if script_path and self.runner.start(script_path):
            self.current_script = "Faktury"
            self.status_label.config(text="Status: Uruchomiono Faktury...")
            self.btn_zlecenia.config(state=tk.DISABLED)
            self.btn_faktury.config(state=tk.DISABLED)
            self.btn_stop.config(state=tk.NORMAL)
            self.log_content += f"\n{LOG_SEPARATOR}\nUruchamianie Faktury...\n{LOG_SEPARATOR}\n"
            self._update_log_display()

    def _on_stop(self) -> None:
        """Handle Stop button click."""
        if self.runner.is_running:
            self.runner.stop()
            self.log_content += f"\n[ZATRZYMANO] {self.current_script} zostało zatrzymane przez użytkownika.\n"
            self._update_log_display()
            self.status_label.config(text="Status: Zatrzymano")
            self.btn_zlecenia.config(state=tk.NORMAL)
            self.btn_faktury.config(state=tk.NORMAL)
            self.btn_stop.config(state=tk.DISABLED)
            self.current_script = None

    def _on_clear(self) -> None:
        """Handle Clear Log button click."""
        self.log_content = ""
        self._update_log_display()

    def _on_config(self) -> None:
        """Handle Configuration button click."""
        ConfigWindow(self.root, self.config)

    def _on_close(self) -> None:
        """Handle window close event."""
        self.runner.stop()
        self.root.destroy()


class ConfigWindow:
    """Configuration window dialog."""

    def __init__(self, parent: tk.Tk, config: ConfigManager):
        """Initialize the configuration window.

        Args:
            parent: The parent window.
            config: The configuration manager instance.
        """
        self.config = config

        self.window = tk.Toplevel(parent)
        self.window.title("Konfiguracja")
        self.window.geometry("500x300")
        self.window.resizable(False, False)
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

        # Scripts configuration
        scripts_frame = ttk.LabelFrame(main_frame, text="Skrypty", padding="10")
        scripts_frame.pack(fill=tk.X, pady=5)

        ttk.Label(scripts_frame, text="Ścieżka do Zlecenia:").pack(anchor=tk.W)
        self.zlecenia_entry = ttk.Entry(scripts_frame, width=50)
        self.zlecenia_entry.insert(0, self.config.scripts.get("zlecenia", ""))
        self.zlecenia_entry.pack(fill=tk.X, pady=2)

        ttk.Label(scripts_frame, text="Ścieżka do Faktury:").pack(anchor=tk.W)
        self.faktury_entry = ttk.Entry(scripts_frame, width=50)
        self.faktury_entry.insert(0, self.config.scripts.get("faktury", ""))
        self.faktury_entry.pack(fill=tk.X, pady=2)

        # Buttons
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

    def _on_save(self) -> None:
        """Handle Save button click."""
        self.config.set("python_executable", self.py_entry.get())
        scripts = {
            "zlecenia": self.zlecenia_entry.get(),
            "faktury": self.faktury_entry.get()
        }
        self.config.set("scripts", scripts)
        self.config.save()
        messagebox.showinfo("Sukces", "Konfiguracja została zapisana.")
        self.window.destroy()


def main():
    """Main function to run the launcher application."""
    root = tk.Tk()
    LauncherApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
