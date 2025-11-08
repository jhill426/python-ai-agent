import os


def get_file_content(working_directory, file_path):
    try:
        root_abs = os.path.realpath(working_directory)

        if os.path.isabs(file_path):
            target_abs = os.path.realpath(file_path)
        else:
            target_abs = os.path.realpath(os.path.join(working_directory, file_path))

        if os.path.commonpath([target_abs, root_abs]) != root_abs:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(target_abs):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        try:
            with open(target_abs, "r", encoding="utf-8", errors="replace") as f:
                data = f.read()
        except Exception as e:
            return f"Error: {e}"

        if len(data) > 10000:
            return (
                data[:10000] + f'[...File "{file_path}" truncated at 10000 characters]'
            )

        return data

    except Exception as e:
        return f"Error: {e}"
