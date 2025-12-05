"""Process runner module for executing Python scripts."""

import subprocess
import threading
import queue
from pathlib import Path
from typing import Optional


class ProcessRunner:
    """Runs Python scripts as subprocesses with output streaming."""

    def __init__(self, python_executable: str = "python"):
        """Initialize the ProcessRunner.

        Args:
            python_executable: Path to the Python executable.
        """
        self.python_executable = python_executable
        self._process: Optional[subprocess.Popen] = None
        self._output_queue: queue.Queue = queue.Queue()
        self._reader_thread: Optional[threading.Thread] = None
        self._running = False
        self._lock = threading.Lock()

    @property
    def is_running(self) -> bool:
        """Check if a process is currently running.

        Returns:
            True if a process is running, False otherwise.
        """
        with self._lock:
            process = self._process
        if process is None:
            return False
        return process.poll() is None

    def start(self, script_path: str, cwd: str = None, args: str = "") -> bool:
        """Start a Python script as a subprocess.

        Args:
            script_path: Path to the Python script to run.
            cwd: Working directory for the process (optional).
            args: Command line arguments (optional).

        Returns:
            True if the script was started successfully, False otherwise.
        """
        if self.is_running:
            return False

        script = Path(script_path)
        if not script.exists():
            self._output_queue.put(f"Error: Script not found: {script_path}\n")
            return False

        # Determine working directory
        working_dir = cwd if cwd else str(script.parent)

        # Build command with optional arguments
        cmd = [self.python_executable, str(script)]
        if args:
            cmd.extend(args.split())

        try:
            self._process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
                cwd=working_dir
            )
            self._running = True
            self._start_reader_thread()
            return True
        except Exception as e:
            self._output_queue.put(f"Error starting script: {e}\n")
            return False

    def _start_reader_thread(self) -> None:
        """Start a background thread to read process output."""
        def read_output():
            with self._lock:
                process = self._process
            if process and process.stdout:
                for line in process.stdout:
                    self._output_queue.put(line)
                process.stdout.close()
            with self._lock:
                self._running = False

        self._reader_thread = threading.Thread(target=read_output, daemon=True)
        self._reader_thread.start()

    def stop(self) -> None:
        """Stop the running process."""
        with self._lock:
            process = self._process
            if process is not None:
                try:
                    process.terminate()
                    process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    process.kill()
                    process.wait()
                finally:
                    self._process = None
                    self._running = False

    def get_output(self) -> str:
        """Get all available output from the process.

        Returns:
            String containing all available output lines.
        """
        output_lines = []
        while True:
            try:
                line = self._output_queue.get_nowait()
                output_lines.append(line)
            except queue.Empty:
                break
        return "".join(output_lines)

    def __del__(self):
        """Cleanup when the runner is destroyed."""
        self.stop()
