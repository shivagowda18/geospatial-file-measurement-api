import geopandas as gpd


def get_crs_name(gdf: gpd.GeoDataFrame) -> str | None:
    """Return the CRS name of the GeoDataFrame."""

    if gdf.crs is None:
        return None

    return gdf.crs.to_string()


def get_projected_gdf(gdf: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    """
    Transform geographic coordinates into a suitable projected CRS
    for accurate distance and area calculations.
    """

    if gdf.crs is None:
        raise ValueError("The uploaded file does not contain a CRS.")

    # If the data is already projected, use it directly.
    if not gdf.crs.is_geographic:
        return gdf

    # Estimate a suitable local projected CRS.
    projected_crs = gdf.estimate_utm_crs()

    if projected_crs is None:
        raise ValueError("Unable to determine a suitable projected CRS.")

    return gdf.to_crs(projected_crs)