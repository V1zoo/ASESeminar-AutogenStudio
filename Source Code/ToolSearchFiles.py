import re
import os
import fnmatch

def search_files(directory: str, pattern: str) -> list:
    try:
        matches = []
        for root, _, filenames in os.walk(directory):
            for filename in filenames:
                absolute_path = os.path.join(root, filename)
                with open(absolute_path,encoding="latin-1") as f:
                    if len(re.findall(pattern,f.read()))>0:
                        matches.append(absolute_path)
            for filename in fnmatch.filter(filenames, pattern):
                absolute_path = os.path.join(root, filename)
                matches.append(absolute_path)
        if matches:
            return "\n".join(matches)
        else:
            return f"No files found for pattern {pattern} in directory {directory}"
    except Exception as e:
        return f"Error: {str(e)}"
