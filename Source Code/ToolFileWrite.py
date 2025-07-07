def file_write(file_path: str, content: str) -> str:
    try:
        with open(file_path, 'w') as f:
            f.write(content)
        return f"Successfully written to {file_path}"
    except Exception as e:
        return f"Error: {str(e)}"