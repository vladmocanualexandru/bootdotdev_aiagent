import os
import subprocess

schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Execute the indicated python file, relative to the working directory.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path of the Python/*.py file that should be executed, relative to the working directory (default is the working directory itself)",
                },
                "args": {
                    "type": "list of strings",
                    "description": "List of parameters that are to be sent to the Python file upon execution.",
                },
            },
        },
    },
}

def run_python_file(working_dir: str, file_path: str, args: list[str] | None = None) -> str:
    try:
        working_dir_abs = os.path.abspath(working_dir)
        target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))

        if os.path.commonpath([working_dir_abs, target_file]) != working_dir_abs:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(target_file):
            return f'Error: "{file_path}" does not exist or is not a regular file'

        if not file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'

        command = ["python", target_file]

        if args:
            command.extend(args)

        run_result = subprocess.run(command, cwd=working_dir, text=True, timeout=30, capture_output=True, check=False)

        report = [f'Successfully executed "{file_path}"']

        if run_result.returncode != 0:
            report.append(f"Process exited with code {run_result.returncode}")

        if run_result.stdout == '' and run_result.stderr == '':
            report.append(f"No output produced")
        else:
            report.append(f"STDOUT: {run_result.stdout}")
            report.append(f"STDERR: {run_result.stderr}")

        return "\n".join(report)

    except Exception as e:
        return f"Error: executing Python file: {e}"
