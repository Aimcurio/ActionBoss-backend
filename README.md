# FastAPI File Helper Backend

This is a small, open‑source FastAPI backend that gives your Custom GPT
basic "file system" powers:

- List files and folders under a directory
- Read the contents of a text file
- Upload and unzip a ZIP file, and return the extracted file tree

## Endpoints

### `GET /health`
Simple health check.

### `GET /fs/tree`
List files and directories under a given root.

**Query parameters:**
- `root` (optional): Path relative to the project root. Defaults to `"."`.

### `GET /fs/file`
Read a text file and return its contents.

**Query parameters:**
- `path` (required): Path to the file, relative to the project root.

### `POST /fs/unzip`
Upload a ZIP file and extract it on the server.

**Body:** `multipart/form-data`
- `file`: The ZIP file to upload.

**Response:**
- `extract_root`: Where the ZIP contents were extracted.
- `tree`: A simple listing of extracted files and folders.

## Quickstart (local)

1. Make sure you have Python 3.10+ installed.
2. Create a virtual environment (recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate   # On Windows: .venv\Scripts\activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Run the server:

   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

5. Open your browser at:

   - http://localhost:8000/docs  → interactive API docs
   - http://localhost:8000/health → health check

## Connecting to a Custom GPT (high‑level)

Once this backend is deployed somewhere (for example on a VPS, Render,
Railway, or another host), you'll get a public URL like:

```text
https://your-backend-url.example.com
```

In your Custom GPT "Actions" settings, you can then define endpoints such as:

- `GET /health`
- `GET /fs/tree`
- `GET /fs/file`
- `POST /fs/unzip`

so the GPT can call them to explore your files and ZIP archives.
