# functions/write_file.py
import os


def write_file(working_directory, file_path, content):
    try:
        root_abs = os.path.realpath(working_directory)

        if os.path.isabs(file_path):
            target_abs = os.path.realpath(file_path)
        else:
            target_abs = os.path.realpath(os.path.join(working_directory, file_path))

        if os.path.commonpath([target_abs, root_abs]) != root_abs:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

        parent_dir = os.path.dirname(target_abs)
        try:
            os.makedirs(parent_dir, exist_ok=True)
        except Exception as e:
            return f"Error: {e}"

        try:
            with open(target_abs, "w", encoding="utf-8") as f:
                f.write(content)
        except Exception as e:
            return f"Error: {e}"

        return (
            f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        )

    except Exception as e:
        return f"Error: {e}"
