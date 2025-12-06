# App Python

Menu do uruchamiania aplikacji PY - Launcher for running Python scripts using Tkinter (standard library).

## Description

This application provides a graphical user interface (GUI) for launching and managing Python scripts. It uses **Tkinter**, which is part of Python's standard library, so no external dependencies are required.

The launcher supports running multiple scripts configured through the GUI:

- **Zlecenia** (Orders) - Script for processing order batches
- **Faktury** (Invoices) - Script for processing invoice batches
- **Custom entries** - Add your own scripts through the GUI

## Features

- Simple and intuitive GUI built with **Tkinter** (standard library)
- **Add new menu entries** through the GUI with file/folder browser dialogs
- **Edit and delete existing entries** from the configuration window
- **Persistent configuration saving** - changes to entries are automatically saved to `data/config.json`
- **File chooser dialog** for selecting Python scripts (*.py)
- **Folder chooser dialog** for selecting working directory
- **Relative path support** - paths can be stored relative to the application folder
- Real-time output logging from running scripts
- Start/Stop control for running processes
- Configuration management via JSON file (`data/config.json`)
- Automatic config file creation if missing

## Requirements

- Python 3.x (Tkinter is included in standard Python installation)

No external dependencies required! The application uses only Python's standard library.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/dzieju/App-Python.git
   cd App-Python
   ```

2. No additional dependencies to install - Tkinter is included with Python.

## Usage

Run the launcher application:

```bash
python app.py
```

### Adding a New Entry via GUI

1. Click the **Konfiguracja** (Configuration) button
2. Click **Dodaj wpis** (Add Entry)
3. Enter the entry name
4. Click **Wybierz...** next to "Ścieżka do skryptu" to browse for a Python script
5. Optionally click **Wybierz...** next to "Katalog roboczy" to set a working directory
6. Optionally fill in interpreter and arguments
7. Check/uncheck "Zapisz ścieżkę względnie do folderu aplikacji" to store relative/absolute paths
8. Click **OK** to add the entry
9. Click **Zapisz** (Save) to save all changes

### Editing/Deleting Entries

1. Click the **Konfiguracja** button
2. Select an entry from the list
3. Click **Edytuj** (Edit) to modify or **Usuń** (Delete) to remove
4. Click **Zapisz** to save changes

### Manual Test Steps

1. Run `python app.py` to start the launcher
2. Click the **Zlecenia** button to start the Zlecenia script
3. Observe the log output in the text area
4. Click the **Zatrzymaj** (Stop) button to stop the running process
5. Click **Faktury** to test the other script
6. Click **Wyczyść log** (Clear Log) to clear the output log
7. Click **Konfiguracja** to open the configuration window
8. Click **Dodaj wpis** → Select `scripts/zlecenia_main.py` via file dialog → Confirm
9. Return to main window and click the new button to run the script

## Project Structure

```
App-Python/
├── app.py              # Main launcher application (Tkinter)
├── runner.py           # Process runner module
├── config.py           # Configuration manager module
├── scripts/
│   ├── zlecenia_main.py    # Zlecenia (Orders) script
│   └── faktury_main.py     # Faktury (Invoices) script
├── data/
│   └── config.json     # Application configuration
└── README.md           # This file
```

## Configuration

The application uses `data/config.json` for configuration. If this file is missing, it will be automatically created with default values:

```json
{
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
```

### Entry Fields

- **name**: Display name for the button
- **script_path**: Path to the Python script (absolute or relative to app folder)
- **working_dir**: Working directory for script execution (optional, defaults to script's directory)
- **interpreter**: Custom Python interpreter path (optional)
- **args**: Command line arguments to pass to the script (optional)

You can modify the configuration through the GUI by clicking the **Konfiguracja** button.

## Building Executable with PyInstaller

To create a standalone executable:

1. Install PyInstaller:
   ```bash
   pip install pyinstaller
   ```

2. Build the executable:
   ```bash
   pyinstaller --onefile --windowed --name="Launcher" app.py
   ```

3. The executable will be created in the `dist/` folder.

**Note:** Make sure to copy the `scripts/` and `data/` folders next to the executable for it to work correctly.

## License

This project is provided as-is for demonstration purposes.
