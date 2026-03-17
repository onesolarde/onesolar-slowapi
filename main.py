import os
from typing import Any

from dotenv import load_dotenv
from fastapi import FastAPI
from app.database import engine, Base

# Create SQLAlchemy metadata
Base.metadata.create_all(bind=engine)

# Load environment variables
load_dotenv()

# Load app configuration
app_config: dict[str, Any] = {
    "ENV": os.getenv("ENV", "production"),
    "DATABASE_URL": os.getenv("DATABASE_URL", "sqlite:///./app.db"),
    "SECRET_KEY": os.getenv("SECRET_KEY"),
    "VERSION": "2.0.0",
}

app = FastAPI(
    title="OneSolar Super Hub",
    version=app_config["VERSION"],
    description="Updated version of our Solar Park Project Management backend™",
)

@app.get("/healthcheck")
def health_check():
    return {"status": "healthy"}


@app.get("/config")
def get_config():
    return app_config