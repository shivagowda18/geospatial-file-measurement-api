import geopandas as gpd

from app.services.crs_service import get_projected_gdf


def calculate_measurements(gdf: gpd.GeoDataFrame) -> list[dict]:
    """
    Calculate measurements for supported geometry types.

    Polygon    -> area in square metres
    LineString -> length in metres
    Point      -> no measurement required
    """

    projected_gdf = get_projected_gdf(gdf)

    results = []

    for index, row in projected_gdf.iterrows():
        geometry = row.geometry

        result = {
            "feature_id": index,
            "geometry_type": geometry.geom_type if geometry else None,
            "measurement": None,
            "unit": None,
        }

        if geometry is None:
            result["message"] = "Feature has no geometry."

        elif geometry.geom_type == "Polygon":
            result["measurement"] = geometry.area
            result["unit"] = "m²"

        elif geometry.geom_type == "LineString":
            result["measurement"] = geometry.length
            result["unit"] = "m"

        elif geometry.geom_type == "Point":
            result["message"] = "No measurement required for Point."

        else:
            result["message"] = (
                f"Unsupported geometry type: {geometry.geom_type}"
            )

        results.append(result)

    return results