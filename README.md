# App Python

Menu do uruchamiania aplikacji PY - A PySimpleGUI-based launcher for running Python scripts.

## Description

This application provides a graphical user interface (GUI) for launching and managing Python scripts. It currently supports running two main scripts:

- **Zlecenia** (Orders) - Script for processing order batches
- **Faktury** (Invoices) - Script for processing invoice batches

## Features

- Simple and intuitive GUI built with PySimpleGUI
- Real-time output logging from running scripts
- Start/Stop control for running processes
- Configuration management via JSON file
- Automatic config file creation if missing

## Requirements

- Python 3.x
- PySimpleGUI

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/dzieju/App-Python.git
   cd App-Python
   ```

2. Install dependencies:
   ```bash
   pip install PySimpleGUI
   ```

## Usage

Run the launcher application:

```bash
python app.py
```

### Manual Test Steps

1. Run `python app.py` to start the launcher
2. Click the **Zlecenia** button to start the Zlecenia script
3. Observe the log output in the text area
4. Click the **Stop** button to stop the running process
5. Click **Faktury** to test the other script
6. Click **Clear Log** to clear the output log

## Project Structure

```
App-Python/
├── app.py              # Main launcher application (PySimpleGUI)
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

## License

This project is provided as-is for demonstration purposes.
