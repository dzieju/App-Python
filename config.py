"""Configuration manager module for the launcher application."""

import json
import os
from pathlib import Path


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
        """Save current configuration to the JSON file."""
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.config_path, "w", encoding="utf-8") as f:
            json.dump(self._config, f, indent=2, ensure_ascii=False)

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
