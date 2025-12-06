"""Configuration manager module for the launcher application."""

import json
import os
import tempfile
from pathlib import Path
from typing import List, Optional


def get_app_dir() -> Path:
    """Get the application directory (where app.py resides).

    Returns:
        Path to the application directory.
    """
    return Path(__file__).parent.resolve()


class ConfigManager:
    """Manages application configuration stored in a JSON file."""

    def __init__(self, config_path: str = "data/config.json"):
        """Initialize the ConfigManager.

        Args:
            config_path: Path to the configuration JSON file.
        """
        self.config_path = Path(config_path)
        self._config = {}
        self._ensure_config_exists()
        self.load()

    def _ensure_config_exists(self) -> None:
        """Ensure the configuration file exists, creating it if missing."""
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.config_path.exists():
            self._config = self._get_default_config()
            self.save()

    def _get_default_config(self) -> dict:
        """Return the default configuration.

        Returns:
            Dictionary containing default configuration values.
        """
        return {
            "scripts": {
                "zlecenia": "scripts/zlecenia_main.py",
                "faktury": "scripts/faktury_main.py"
            },
            "entries": [
                {
                    "name": "Zlecenia",
                    "script_path": "scripts/zlecenia_main.py",
                    "working_dir": "",
                    "interpreter": "",
                    "args": ""
                },
                {
                    "name": "Faktury",
                    "script_path": "scripts/faktury_main.py",
                    "working_dir": "",
                    "interpreter": "",
                    "args": ""
                }
            ],
            "python_executable": "python",
            "log_max_lines": 1000
        }

    def load(self) -> dict:
        """Load configuration from the JSON file.

        Returns:
            Dictionary containing the loaded configuration.
        """
        try:
            with open(self.config_path, "r", encoding="utf-8") as f:
                self._config = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            self._config = self._get_default_config()
            self.save()
        return self._config

    def save(self) -> None:
        """Save current configuration to the JSON file atomically."""
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Write to a temporary file first, then rename for atomic save
        temp_fd, temp_path = tempfile.mkstemp(
            dir=self.config_path.parent,
            prefix=".config_",
            suffix=".tmp"
        )
        
        try:
            # Set secure permissions (read/write for owner only)
            os.chmod(temp_path, 0o600)
            
            with os.fdopen(temp_fd, "w", encoding="utf-8") as f:
                json.dump(self._config, f, indent=2, ensure_ascii=False)
            
            # Atomic rename (on most systems)
            os.replace(temp_path, self.config_path)
        except (IOError, OSError, json.JSONEncodeError) as e:
            # Clean up temp file if save failed
            try:
                os.remove(temp_path)
            except OSError:
                pass
            raise

    def get(self, key: str, default=None):
        """Get a configuration value.

        Args:
            key: The configuration key to retrieve.
            default: Default value if key is not found.

        Returns:
            The configuration value or default.
        """
        return self._config.get(key, default)

    def set(self, key: str, value) -> None:
        """Set a configuration value.

        Args:
            key: The configuration key to set.
            value: The value to set.
        """
        self._config[key] = value

    @property
    def scripts(self) -> dict:
        """Get the scripts configuration.

        Returns:
            Dictionary mapping script names to their paths.
        """
        return self._config.get("scripts", {})

    @property
    def python_executable(self) -> str:
        """Get the Python executable path.

        Returns:
            Path to the Python executable.
        """
        return self._config.get("python_executable", "python")

    @property
    def entries(self) -> List[dict]:
        """Get the list of menu entries.

        Returns:
            List of entry dictionaries.
        """
        return self._config.get("entries", [])

    def add_entry(self, name: str = None, script_path: str = None, working_dir: str = "",
                  interpreter: str = "", args: str = "", save_relative: bool = True,
                  show_console: bool = False, enabled: bool = True, 
                  cwd_flag: bool = False, **kwargs) -> None:
        """Add a new menu entry and save configuration.

        Args:
            name: Display name for the entry.
            script_path: Path to the script file.
            working_dir: Working directory for the script (optional).
            interpreter: Python interpreter path (optional).
            args: Command line arguments (optional).
            save_relative: Whether paths are stored relative to app folder.
            show_console: Whether to show console window when running.
            enabled: Whether the entry is enabled.
            cwd_flag: Whether working directory is set.
            **kwargs: Additional fields to include in the entry.
        """
        if "entries" not in self._config:
            self._config["entries"] = []

        entry = {
            "name": name,
            "script_path": script_path,
            "working_dir": working_dir,
            "interpreter": interpreter,
            "args": args,
            "save_relative": save_relative,
            "show_console": show_console,
            "enabled": enabled,
            "cwd_flag": cwd_flag
        }
        # Add any additional fields from kwargs
        entry.update(kwargs)
        self._config["entries"].append(entry)
        self.save()

    def update_entry(self, index: int, name: str = None, script_path: str = None,
                     working_dir: str = "", interpreter: str = "",
                     args: str = "", save_relative: bool = True,
                     show_console: bool = False, enabled: bool = True,
                     cwd_flag: bool = False, **kwargs) -> bool:
        """Update an existing menu entry and save configuration.

        Args:
            index: Index of the entry to update.
            name: Display name for the entry.
            script_path: Path to the script file.
            working_dir: Working directory for the script (optional).
            interpreter: Python interpreter path (optional).
            args: Command line arguments (optional).
            save_relative: Whether paths are stored relative to app folder.
            show_console: Whether to show console window when running.
            enabled: Whether the entry is enabled.
            cwd_flag: Whether working directory is set.
            **kwargs: Additional fields to include in the entry.

        Returns:
            True if entry was updated, False if index is invalid.
        """
        if "entries" not in self._config:
            return False

        entries = self._config["entries"]
        if 0 <= index < len(entries):
            # Preserve existing id if present
            existing_id = entries[index].get("id")
            
            entry = {
                "name": name,
                "script_path": script_path,
                "working_dir": working_dir,
                "interpreter": interpreter,
                "args": args,
                "save_relative": save_relative,
                "show_console": show_console,
                "enabled": enabled,
                "cwd_flag": cwd_flag
            }
            
            # Preserve id if it existed
            if existing_id is not None:
                entry["id"] = existing_id
            elif "id" in kwargs:
                entry["id"] = kwargs["id"]
                
            # Add any additional fields from kwargs (except id which was handled)
            for key, value in kwargs.items():
                if key != "id":
                    entry[key] = value
                    
            entries[index] = entry
            self.save()
            return True
        return False

    def remove_entry(self, index: int) -> bool:
        """Remove a menu entry and save configuration.

        Args:
            index: Index of the entry to remove.

        Returns:
            True if entry was removed, False if index is invalid.
        """
        if "entries" not in self._config:
            return False

        entries = self._config["entries"]
        if 0 <= index < len(entries):
            entries.pop(index)
            self.save()
            return True
        return False
