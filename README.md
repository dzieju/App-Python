# App Python

Menu do uruchamiania aplikacji PY - Launcher for running Python scripts using Tkinter (standard library).

## Description

This application provides a graphical user interface (GUI) for launching and managing Python scripts. It uses **Tkinter**, which is part of Python's standard library, so no external dependencies are required.

The launcher supports running two main scripts:

- **Zlecenia** (Orders) - Script for processing order batches
- **Faktury** (Invoices) - Script for processing invoice batches

## Features

- Simple and intuitive GUI built with **Tkinter** (standard library)
- Real-time output logging from running scripts
- Start/Stop control for running processes
- Configuration window for easy settings management
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

### Manual Test Steps

1. Run `python app.py` to start the launcher
2. Click the **Zlecenia** button to start the Zlecenia script
3. Observe the log output in the text area
4. Click the **Zatrzymaj** (Stop) button to stop the running process
5. Click **Faktury** to test the other script
6. Click **Wyczyść log** (Clear Log) to clear the output log
7. Click **Konfiguracja** to open the configuration window

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
  "python_executable": "python",
  "log_max_lines": 1000
}
```

You can also modify the configuration through the GUI by clicking the **Konfiguracja** button.

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
