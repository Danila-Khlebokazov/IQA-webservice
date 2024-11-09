import uvicorn

from app import app

__all__ = ("app",)

if __name__ == "__main__":
    uvicorn.run("run:app", reload=True, host="0.0.0.0", port=8000)
