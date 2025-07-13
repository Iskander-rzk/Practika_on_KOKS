import uvicorn
from fastapi import FastAPI
from pathlib import Path
from app.api.router import router as api_router

BASE_DIR = Path(__file__).resolve().parent
ENV_FILE = BASE_DIR / ".env"

app = FastAPI()
app.include_router(api_router)

if __name__ == "__main__":
    uvicorn.run(
        "main:app", reload=True, env_file=ENV_FILE
    )