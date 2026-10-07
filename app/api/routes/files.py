from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, File, UploadFile, HTTPException

from app.models.schemas import FileResponse, MeasurementsResponse
from app.services.geospatial_service import (
    read_geospatial_file,
    extract_features,
)
from app.services.measurement_service import calculate_measurements
from app.services.crs_service import get_crs_name
from app.services.database_service import (
    save_file_record,
    get_file_record,
)


router = APIRouter(prefix="/api/files", tags=["Files"])


UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


@router.post("/", response_model=FileResponse)
async def upload_file(file: UploadFile = File(...)):
    allowed_extensions = {".kml", ".zip"}

    filename = file.filename or ""
    extension = (
        "." + filename.rsplit(".", 1)[-1].lower()
        if "." in filename
        else ""
    )

    if extension not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail="Unsupported file type. Upload a .kml file or a .zip Shapefile.",
        )

    file_id = str(uuid4())
    saved_path = UPLOAD_DIR / f"{file_id}{extension}"

    try:
        with saved_path.open("wb") as buffer:
            while chunk := await file.read(1024 * 1024):
                buffer.write(chunk)

        gdf = read_geospatial_file(str(saved_path))

        features = extract_features(gdf)

        measurements = calculate_measurements(gdf)

        file_record = {
            "id": file_id,
            "filename": filename,
            "feature_count": len(features),
            "crs": get_crs_name(gdf),
            "status": "COMPLETED",
            "features": features,
            "measurements": measurements,
        }

        save_file_record(file_record)

        return file_record

    except ValueError as exc:
        if saved_path.exists():
            saved_path.unlink()

        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    except Exception:
        if saved_path.exists():
            saved_path.unlink()

        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred while processing the file.",
        )


@router.get("/{file_id}", response_model=FileResponse)
async def get_file(file_id: str):
    file_record = get_file_record(file_id)

    if file_record is None:
        raise HTTPException(
            status_code=404,
            detail="File not found.",
        )

    return file_record


@router.get(
    "/{file_id}/measurements/",
    response_model=MeasurementsResponse,
)
async def get_file_measurements(file_id: str):
    file_record = get_file_record(file_id)

    if file_record is None:
        raise HTTPException(
            status_code=404,
            detail="File not found.",
        )

    return {
        "file_id": file_id,
        "measurements": file_record["measurements"],
    }