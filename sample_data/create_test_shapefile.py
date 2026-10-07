import geopandas as gpd
from shapely.geometry import Polygon
from pathlib import Path


output_dir = Path("sample_data/test_shapefile")
output_dir.mkdir(parents=True, exist_ok=True)

polygon = Polygon(
    [
        (77.5946, 12.9716),
        (77.6046, 12.9716),
        (77.6046, 12.9816),
        (77.5946, 12.9816),
        (77.5946, 12.9716),
    ]
)

gdf = gpd.GeoDataFrame(
    {
        "name": ["Test Area"],
    },
    geometry=[polygon],
    crs="EPSG:4326",
)

gdf.to_file(
    output_dir / "test_polygon.shp",
    driver="ESRI Shapefile",
)

print("Test Shapefile created successfully.")
print(gdf)
print("CRS:", gdf.crs)