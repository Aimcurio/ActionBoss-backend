# ActionBoss File Helper Backend
A small, open-source FastAPI backend that gives your Custom GPT **real file-system powers**:

- List files and folders under a directory  
- Read the contents of a text file  
- Upload + unzip ZIP files  
- Return the extracted file tree  

This backend is designed to be used as a Custom GPT Action so your GPT can explore entire directories, repos, or assets just like a real agent.

---

# 🚀 Features

### `GET /health`
Simple health check endpoint.  
Used by Railway and Custom GPT to verify the server is running.

### `GET /fs/tree`
Return a list of files and subdirectories under a given `root`.

**Query params:**
- `root` (optional) — relative path. Default: `"."`.

### `GET /fs/file`
Read a text file and return the contents.

**Query params:**
- `path` (required) — file path relative to project root.

### `POST /fs/unzip`
Upload a ZIP file, extract it, and return the extracted tree.

**Body** (multipart/form-data):
- `file`: the ZIP file

**Response:**
- `extract_root`: extraction directory
- `tree`: extracted file tree

> Note: `python-multipart` is required for file uploads (included in requirements.txt).

---

# 🛠 Requirements

Your environment must have:

- Python 3.10+
- FastAPI
- Uvicorn
- python-multipart (for file uploads)

These are included in `requirements.txt`:

