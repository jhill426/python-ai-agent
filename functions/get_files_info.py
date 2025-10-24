import os

def get_files_info(working_directory, directory="."):
    try:
        root_abs = os.path.abspath(working_directory)
        target_abs = os.path.abspath(os.path.join(working_directory, directory))

        if os.path.commonpath([target_abs, root_abs]) != root_abs:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        if not os.path.isdir(target_abs):
            return f'Error: "{directory}" is not a directory'

        lines = []
        try:
            entries = os.listdir(target_abs)
        except Exception as e:
            return f"Error: {e}"

        for name in sorted(entries, key=str.lower):
            path = os.path.join(target_abs, name)
            try:
                size = os.path.getsize(path)
                is_dir = os.path.isdir(path)
            except Exception as e:
                return f"Error: {e}"

            lines.append(f"- {name}: file_size={size} bytes, is_dir={is_dir}")

        return "\n".join(lines)

    except Exception as e:
        return f"Error: {e}"
