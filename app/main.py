from fastapi import FastAPI

from app.infrastructure.api.book_router import book_router
from app.infrastructure.database import engine, Base

app = FastAPI(title="Library API", version="1.0.0")

Base.metadata.create_all(bind=engine)

app.include_router(book_router, prefix="/api/v1", tags=["Books"])
