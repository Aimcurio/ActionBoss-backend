from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from .fs_utils import list_tree, read_text_file, extract_zip_upload

app = FastAPI(
    title="File Helper Backend",
    description="Small FastAPI backend to help a Custom GPT explore files, "
                "read text files, and extract ZIP archives.",
    version="0.1.0",
)

# Allow everything by default; tighten later if needed.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health():
    """Simple health check endpoint."""
    return {"status": "ok", "service": "file-helper-backend"}


@app.get("/fs/tree")
async def fs_tree(root: str = "."):
    """List files and directories under a given root (relative to project root)."""
    try:
        tree = list_tree(root)
        return {"root": root, "entries": tree}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")


@app.get("/fs/file")
async def fs_file(path: str):
    """Read a text file and return its contents."""
    if not path:
        raise HTTPException(status_code=400, detail="Missing 'path' query parameter.")

    try:
        content = read_text_file(path)
        return {"path": path, "content": content}
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="File not found.")
    except IsADirectoryError:
        raise HTTPException(status_code=400, detail="Path refers to a directory, not a file.")
    except UnicodeDecodeError:
        raise HTTPException(status_code=400, detail="File is not valid UTF-8 text.")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")


@app.post("/fs/unzip")
async def fs_unzip(file: UploadFile = File(...)):
    """
    Upload a ZIP file, extract it on the server, and return a simple file tree
    of the extracted contents.
    """
    if not file.filename.lower().endswith(".zip"):
        raise HTTPException(status_code=400, detail="Uploaded file must be a .zip archive.")

    try:
        extract_root, tree = await extract_zip_upload(file)
        return {"extract_root": extract_root, "entries": tree}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")
