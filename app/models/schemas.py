from typing import Any

from pydantic import BaseModel


class FeatureResponse(BaseModel):
    feature_id: int
    geometry_type: str | None
    geometry: dict[str, Any] | None
    crs: str | None
    properties: dict[str, Any]


class MeasurementResponse(BaseModel):
    feature_id: int
    geometry_type: str | None
    measurement: float | None
    unit: str | None
    message: str | None = None


class FileResponse(BaseModel):
    id: str
    filename: str
    feature_count: int
    crs: str | None
    status: str
    features: list[FeatureResponse]
    measurements: list[MeasurementResponse]


class MeasurementsResponse(BaseModel):
    file_id: str
    measurements: list[MeasurementResponse]