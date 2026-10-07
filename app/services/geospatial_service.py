from pathlib import Path
import zipfile

import geopandas as gpd


SUPPORTED_EXTENSIONS = {".kml", ".zip"}


def validate_shapefile_zip(file_path: str) -> None:
    """Validate that a ZIP contains a complete Shapefile."""

    path = Path(file_path)

    if not zipfile.is_zipfile(path):
        raise ValueError("Uploaded ZIP file is invalid.")

    with zipfile.ZipFile(path, "r") as zip_file:
        members = zip_file.namelist()

        # Prevent unsafe paths inside the ZIP.
        for member in members:
            member_path = Path(member)

            if member_path.is_absolute() or ".." in member_path.parts:
                raise ValueError("ZIP file contains an unsafe file path.")

        files = {
            Path(member).name.lower()
            for member in members
            if not member.endswith("/")
        }

        shapefiles = [
            Path(member).stem.lower()
            for member in members
            if Path(member).suffix.lower() == ".shp"
        ]

        if not shapefiles:
            raise ValueError(
                "ZIP file does not contain a Shapefile (.shp)."
            )

        for stem in shapefiles:
            required_files = {
                f"{stem}.shp",
                f"{stem}.shx",
                f"{stem}.dbf",
                f"{stem}.prj",
            }

            if required_files.issubset(files):
                return

        raise ValueError(
            "ZIP file does not contain a complete Shapefile "
            "(.shp, .shx, .dbf, .prj)."
        )


def read_geospatial_file(file_path: str) -> gpd.GeoDataFrame:
    """Read a supported geospatial file into a GeoDataFrame."""

    path = Path(file_path)
    extension = path.suffix.lower()

    if extension not in SUPPORTED_EXTENSIONS:
        raise ValueError(
            "Unsupported file type. Only .kml and .zip files are supported."
        )

    if extension == ".kml":
        return gpd.read_file(path, driver="KML")

    if extension == ".zip":
     validate_shapefile_zip(str(path))
     return gpd.read_file(path)

    raise ValueError("Unable to process the uploaded file.")


def extract_features(gdf: gpd.GeoDataFrame) -> list[dict]:
    """Extract the required information from each feature."""

    features = []

    for index, row in gdf.iterrows():
        geometry = row.geometry

        properties = {}

        for column in gdf.columns:
            if column != "geometry":
                value = row[column]

                if value is not None:
                    properties[column] = str(value)

        features.append(
    {
        "feature_id": index,
        "geometry_type": geometry.geom_type if geometry else None,
        "geometry": geometry.__geo_interface__ if geometry else None,
        "crs": gdf.crs.to_string() if gdf.crs else None,
        "properties": properties,
    }
)

    return features