import geopandas as gpd
from shapely.geometry import MultiPoint
from pathlib import Path


output_dir = Path("sample_data/test_multipoint")
output_dir.mkdir(parents=True, exist_ok=True)

multipoint = MultiPoint(
    [
        (77.5946, 12.9716),
        (77.6046, 12.9816),
    ]
)

gdf = gpd.GeoDataFrame(
    {
        "name": ["Test MultiPoint"],
    },
    geometry=[multipoint],
    crs="EPSG:4326",
)

gdf.to_file(
    output_dir / "test_multipoint.shp",
    driver="ESRI Shapefile",
)

print("Test MultiPoint Shapefile created successfully.")
print(gdf)
print("CRS:", gdf.crs)