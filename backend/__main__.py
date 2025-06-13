from backend.main import app

# This enables `python -m backend` to run the dev server
import uvicorn

if __name__ == "__main__":
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)