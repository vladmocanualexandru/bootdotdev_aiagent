import os

def get_files_info(working_dir:str, directory:str) -> str:
    try:
        working_dir_abs = os.path.abspath(working_dir)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))

        if os.path.commonpath([working_dir_abs, target_dir]) != working_dir_abs:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        if not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'

        contents = []
        for file_name in os.listdir(target_dir):
            file_path = os.path.join(target_dir, file_name)
            file_size = os.path.getsize(file_path)
            is_dir = os.path.isdir(file_path)

            contents.append(f"- {file_name}: file_size={file_size} bytes, is_dir={is_dir}")

        return "\n".join(contents)
    except Exception as e:
        return f"Error: {e}"
