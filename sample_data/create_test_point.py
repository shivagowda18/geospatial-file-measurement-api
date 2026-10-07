import geopandas as gpd
from shapely.geometry import Point
from pathlib import Path


output_dir = Path("sample_data/test_point")
output_dir.mkdir(parents=True, exist_ok=True)

point = Point(77.5946, 12.9716)

gdf = gpd.GeoDataFrame(
    {
        "name": ["Test Point"],
    },
    geometry=[point],
    crs="EPSG:4326",
)

gdf.to_file(
    output_dir / "test_point.shp",
    driver="ESRI Shapefile",
)

print("Test Point Shapefile created successfully.")
print(gdf)
print("CRS:", gdf.crs)