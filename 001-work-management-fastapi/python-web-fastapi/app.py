"""Start the generated FastAPI workspace."""
import os
from pathlib import Path

import uvicorn

from app.main import app


if __name__ == "__main__":
    database = Path(__file__).resolve().with_name("app.sqlite3")
    os.environ.setdefault("DATABASE_PATH", str(database))
    uvicorn.run(app, host=os.environ.get("HOST", "0.0.0.0"), port=int(os.environ.get("PORT", "3000")))