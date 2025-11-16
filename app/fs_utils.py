import os
import zipfile
import tempfile
from typing import List, Dict
from fastapi import UploadFile, HTTPException


BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


def _safe_join(base: str, *paths: str) -> str:
    """Join paths and ensure the result stays within the base directory."""
    joined = os.path.abspath(os.path.join(base, *paths))
    if not joined.startswith(base):
        raise ValueError("Path escapes base directory.")
    return joined


def list_tree(root: str = ".") -> List[Dict[str, str]]:
    """List files and directories directly under `root` (non-recursive)."""
    target = _safe_join(BASE_DIR, root)
    if not os.path.exists(target):
        raise ValueError(f"Path does not exist: {root}")

    entries = []
    for name in os.listdir(target):
        full = os.path.join(target, name)
        entry_type = "dir" if os.path.isdir(full) else "file"
        entries.append({"name": name, "type": entry_type})
    return entries


def read_text_file(path: str) -> str:
    """Read a UTF-8 text file under BASE_DIR."""
    target = _safe_join(BASE_DIR, path)
    if os.path.isdir(target):
        raise IsADirectoryError(target)
    with open(target, "r", encoding="utf-8") as f:
        return f.read()


async def extract_zip_upload(upload: UploadFile):
    """
    Save the uploaded ZIP to a temp file, extract it under a temp directory
    inside BASE_DIR/tmp, and return the extraction root + a shallow file tree.
    """
    tmp_root = _safe_join(BASE_DIR, "tmp")
    os.makedirs(tmp_root, exist_ok=True)

    # Save upload to a temporary file
    try:
        suffix = ".zip"
        with tempfile.NamedTemporaryFile(delete=False, dir=tmp_root, suffix=suffix) as tmp:
            contents = await upload.read()
            tmp.write(contents)
            tmp_path = tmp.name
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to store uploaded zip: {e}")

    # Directory where we extract
    extract_dir = tempfile.mkdtemp(dir=tmp_root)

    # Extract ZIP
    try:
        with zipfile.ZipFile(tmp_path, "r") as zf:
            zf.extractall(extract_dir)
    except zipfile.BadZipFile:
        raise HTTPException(status_code=400, detail="Invalid ZIP file.")
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)

    # Build a shallow tree (one level under extract_dir)
    entries = []
    for name in os.listdir(extract_dir):
        full = os.path.join(extract_dir, name)
        entry_type = "dir" if os.path.isdir(full) else "file"
        # For now we only return names and types. You can expand later.
        entries.append({"name": name, "type": entry_type})

    # Return path relative to BASE_DIR to avoid leaking full disk path
    rel_extract_root = os.path.relpath(extract_dir, BASE_DIR)
    return rel_extract_root, entries
