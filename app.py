"""Main launcher application using PySimpleGUI."""

import PySimpleGUI as sg
from config import ConfigManager
from runner import ProcessRunner

# Constants
LOG_SEPARATOR = "=" * 50


def create_layout():
    """Create the main window layout.

    Returns:
        List of layout elements for PySimpleGUI.
    """
    button_size = (15, 2)

    layout = [
        [sg.Text("Launcher Application", font=("Helvetica", 16), justification="center", expand_x=True)],
        [sg.HorizontalSeparator()],
        [
            sg.Button("Zlecenia", key="-ZLECENIA-", size=button_size, button_color=("white", "green")),
            sg.Button("Faktury", key="-FAKTURY-", size=button_size, button_color=("white", "blue")),
            sg.Button("Stop", key="-STOP-", size=button_size, button_color=("white", "red"), disabled=True),
        ],
        [sg.HorizontalSeparator()],
        [sg.Text("Output Log:", font=("Helvetica", 10, "bold"))],
        [sg.Multiline(
            size=(80, 20),
            key="-LOG-",
            autoscroll=True,
            disabled=True,
            font=("Courier New", 9)
        )],
        [
            sg.Button("Clear Log", key="-CLEAR-"),
            sg.Push(),
            sg.Text("Status: Ready", key="-STATUS-", font=("Helvetica", 10))
        ],
    ]

    return layout


def main():
    """Main function to run the launcher application."""
    sg.theme("DarkBlue3")

    config = ConfigManager()
    runner = ProcessRunner(python_executable=config.python_executable)

    window = sg.Window(
        "Python Script Launcher",
        create_layout(),
        finalize=True,
        resizable=True
    )

    current_script = None
    log_content = ""

    while True:
        event, values = window.read(timeout=100)

        if event == sg.WIN_CLOSED:
            break

        # Update log with process output
        if runner.is_running:
            output = runner.get_output()
            if output:
                log_content += output
                # Limit log size
                lines = log_content.split("\n")
                max_lines = config.get("log_max_lines", 1000)
                if len(lines) > max_lines:
                    log_content = "\n".join(lines[-max_lines:])
                window["-LOG-"].update(log_content)

        # Check if process finished
        if current_script and not runner.is_running:
            window["-STATUS-"].update(f"Status: {current_script} finished")
            window["-ZLECENIA-"].update(disabled=False)
            window["-FAKTURY-"].update(disabled=False)
            window["-STOP-"].update(disabled=True)
            current_script = None

        if event == "-ZLECENIA-":
            script_path = config.scripts.get("zlecenia")
            if script_path and runner.start(script_path):
                current_script = "Zlecenia"
                window["-STATUS-"].update("Status: Running Zlecenia...")
                window["-ZLECENIA-"].update(disabled=True)
                window["-FAKTURY-"].update(disabled=True)
                window["-STOP-"].update(disabled=False)
                log_content += f"\n{LOG_SEPARATOR}\nStarting Zlecenia...\n{LOG_SEPARATOR}\n"
                window["-LOG-"].update(log_content)

        elif event == "-FAKTURY-":
            script_path = config.scripts.get("faktury")
            if script_path and runner.start(script_path):
                current_script = "Faktury"
                window["-STATUS-"].update("Status: Running Faktury...")
                window["-ZLECENIA-"].update(disabled=True)
                window["-FAKTURY-"].update(disabled=True)
                window["-STOP-"].update(disabled=False)
                log_content += f"\n{LOG_SEPARATOR}\nStarting Faktury...\n{LOG_SEPARATOR}\n"
                window["-LOG-"].update(log_content)

        elif event == "-STOP-":
            if runner.is_running:
                runner.stop()
                log_content += f"\n[STOPPED] {current_script} was stopped by user.\n"
                window["-LOG-"].update(log_content)
                window["-STATUS-"].update("Status: Stopped")
                window["-ZLECENIA-"].update(disabled=False)
                window["-FAKTURY-"].update(disabled=False)
                window["-STOP-"].update(disabled=True)
                current_script = None

        elif event == "-CLEAR-":
            log_content = ""
            window["-LOG-"].update("")

    runner.stop()
    window.close()


if __name__ == "__main__":
    main()
