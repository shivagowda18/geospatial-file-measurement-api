import geopandas as gpd
from shapely.geometry import LineString
from pathlib import Path


output_dir = Path("sample_data/test_line")
output_dir.mkdir(parents=True, exist_ok=True)

line = LineString(
    [
        (77.5946, 12.9716),
        (77.6046, 12.9816),
    ]
)

gdf = gpd.GeoDataFrame(
    {
        "name": ["Test Line"],
    },
    geometry=[line],
    crs="EPSG:4326",
)

gdf.to_file(
    output_dir / "test_line.shp",
    driver="ESRI Shapefile",
)

print("Test LineString Shapefile created successfully.")
print(gdf)
print("CRS:", gdf.crs)