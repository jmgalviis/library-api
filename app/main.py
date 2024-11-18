from fastapi import FastAPI

from app.infrastructure.api.book_router import book_router
from app.infrastructure.database import engine, Base

app = FastAPI(
    title="Library API",
    description="API for managing a library, including books and their details.",
    version="1.0.0",
    contact={
        "name": "Juan Manuel Galvis",
        "email": "jmgalviis@gmail.com",
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
    },
)

Base.metadata.create_all(bind=engine)

app.include_router(book_router, prefix="/api/v1", tags=["Books"])
