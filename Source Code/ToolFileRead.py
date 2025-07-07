def file_read(file_path: str) -> str:
    try:
        with open(file_path, 'r') as f:
            return f.read()
    except Exception as e:
        return f"Error: {str(e)}"
