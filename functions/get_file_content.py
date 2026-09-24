import os
from config import MAX_FILE_READ_CHARS


def get_file_content(working_dir: str, file_path: str) -> str:

    try:
        working_dir_abs = os.path.abspath(working_dir)
        target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))

        if os.path.commonpath([working_dir_abs, target_file]) != working_dir_abs:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(target_file):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        file_content = None
        with open(target_file, "r") as f:
            file_content = f.read(MAX_FILE_READ_CHARS)
            if f.read(1):
                 file_content += f'[...File "{target_file}" truncated at {MAX_FILE_READ_CHARS} characters]'

            return file_content


    except Exception as e:
        return f"Error: {e}"
