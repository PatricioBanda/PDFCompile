import os

def ensure_dir(path: str):
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)
    return path

def join_path(*parts):
    return os.path.normpath(os.path.join(*parts))

def list_files(path: str, extension: str = None):
    if not os.path.exists(path):
        return []
    files = []
    for f in os.listdir(path):
        full = os.path.join(path, f)
        if os.path.isfile(full):
            if extension is None or f.lower().endswith(extension.lower()):
                files.append(full)
    return files
