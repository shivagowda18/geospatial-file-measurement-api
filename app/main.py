from fastapi import FastAPI

from app.api.routes.files import router as files_router
from app.services.database_service import initialize_database


app = FastAPI(
    title="Geospatial File Measurement API",
    description="API for processing geospatial files and calculating measurements.",
    version="1.0.0",
)


initialize_database()


@app.get("/")
def root():
    return {
        "message": "Geospatial File Measurement API is running",
        "status": "healthy",
    }


app.include_router(files_router)