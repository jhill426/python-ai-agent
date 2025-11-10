from pathlib import Path
import subprocess
import sys
from typing import List


def run_python_file(working_directory: str, file_path: str, args: List[str] = []):
    """
    Execute a Python file within a permitted working directory.
    """
    try:
        workdir = Path(working_directory).resolve()
        target = (
            (workdir / file_path).resolve()
            if not Path(file_path).is_absolute()
            else Path(file_path).resolve()
        )

        try:
            target.relative_to(workdir)
        except ValueError:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        if not target.exists() or not target.is_file():
            return f'Error: File "{file_path}" not found.'
        if target.suffix != ".py":
            return f'Error: "{file_path}" is not a Python file.'

        cmd = [sys.executable, str(target), *[str(a) for a in (args or [])]]

        completed = subprocess.run(
            cmd, cwd=str(workdir), capture_output=True, text=True, timeout=30
        )

        stdout = completed.stdout or ""
        stderr = completed.stderr or ""

        if not stdout and not stderr:
            return "No output produced."

        parts = []
        parts.append(
            "STDOUT:"
            + ("" if stdout.startswith("\n") or not stdout else "\n")
            + stdout.rstrip("\n")
        )
        parts.append(
            "STDERR:"
            + ("" if stderr.startswith("\n") or not stderr else "\n")
            + stderr.rstrip("\n")
        )
        if completed.returncode != 0:
            parts.append(f"Process exited with code {completed.returncode}")

        return "\n".join(parts)

    except Exception as e:
        return f"Error: executing Python file: {e}"
