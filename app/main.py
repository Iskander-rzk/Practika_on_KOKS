import uvicorn
from fastapi import FastAPI
from pathlib import Path
from app.api.router import router as api_router
from app.api.router import router

app = FastAPI()
app.include_router(router)

BASE_DIR = Path(__file__).resolve().parent
ENV_FILE = BASE_DIR / ".env"

app = FastAPI()
app.include_router(api_router)

def run():
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        env_file=ENV_FILE
    )

if __name__ == "__main__":
    run()