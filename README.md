# Geospatial File Measurement API

A backend REST API for uploading, processing, and measuring geospatial files.

The application supports KML files and Shapefile ZIP files, extracts geospatial features and their attributes, handles coordinate reference systems (CRS), calculates measurements, and stores processed file information in SQLite.

## Features

- Upload KML files.
- Upload Shapefile ZIP files.
- Validate uploaded file types.
- Validate Shapefile ZIP contents.
- Extract feature geometry and properties.
- Return geometry type, geometry, CRS, and attributes.
- Calculate Polygon area in square metres.
- Calculate LineString length in metres.
- Handle Point geometries without measurement.
- Handle unsupported geometry types gracefully.
- Detect and handle geographic CRS such as EPSG:4326.
- Transform geographic coordinates to a suitable projected CRS before calculating measurements.
- Store processed file information in SQLite.
- Provide REST API endpoints for file information and measurements.
- Automated API testing using pytest.

## Technology Stack

- Python
- FastAPI
- GeoPandas
- Shapely
- PyProj
- Pydantic
- SQLite
- Pytest

## Project Structure

```text
geospatial-file-measurement-api/
│
├── app/
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes/
│   │       ├── __init__.py
│   │       └── files.py
│   │
│   ├── core/
│   │   └── __init__.py
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   └── schemas.py
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── crs_service.py
│   │   ├── database_service.py
│   │   ├── geospatial_service.py
│   │   └── measurement_service.py
│   │
│   ├── __init__.py
│   └── main.py
│
├── sample_data/
│   ├── create_test_line.py
│   ├── create_test_multipoint.py
│   ├── create_test_point.py
│   ├── create_test_shapefile.py
│   ├── test_line.zip
│   ├── test_multipoint.zip
│   ├── test_point.zip
│   ├── test_polygon.kml
│   └── test_shapefile.zip
│
├── tests/
│   ├── conftest.py
│   └── test_api.py
│
├── .gitignore
├── requirements.txt
└── README.md

## Setup

### 1. Clone the repository

```bash
git clone <your-github-repository-url>
cd geospatial-file-measurement-api
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

### 3. Activate the virtual environment

Windows:

```bash
.venv\Scripts\activate
```

### 4. Install the dependencies

```bash
pip install -r requirements.txt
```

## Running the API

Start the FastAPI development server:

```bash
uvicorn app.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

Interactive Swagger API documentation:

```text
http://127.0.0.1:8000/docs
```
## API Endpoints

### Health Check

```http
GET /
```

Example response:

```json
{
  "message": "Geospatial File Measurement API is running",
  "status": "healthy"
}
```

### Upload a Geospatial File

```http
POST /api/files/
```

Accepted file types:

- `.kml`
- `.zip` containing a Shapefile

Example using cURL:

```bash
curl -X POST "http://127.0.0.1:8000/api/files/" -F "file=@sample_data/test_polygon.kml"
```

Example response:

```json
{
  "id": "file-id",
  "filename": "test_polygon.kml",
  "feature_count": 1,
  "crs": "EPSG:4326",
  "status": "COMPLETED"
}
```

The response also contains the extracted features and calculated measurements.

### Get File Information

```http
GET /api/files/{file_id}
```

Returns the stored information for a previously processed file.

The response includes:

- File ID
- Filename
- Feature count
- CRS
- Processing status
- Extracted features
- Measurements

### Get Measurements

```http
GET /api/files/{file_id}/measurements/
```

Returns the measurements calculated for the specified file.

## File Processing Flow

1. The API receives a KML file or Shapefile ZIP file.
2. The uploaded file is saved in the `uploads` directory.
3. The uploaded file type is validated.
4. For ZIP files, the application validates that the archive contains a complete Shapefile.
5. GeoPandas reads the geospatial data.
6. Features, geometry, CRS, and properties are extracted.
7. The CRS is checked.
8. Measurements are calculated for supported geometry types.
9. The processed file record is stored in SQLite.
10. The processed result is returned through the API.

## Measurement Flow

The application handles measurements based on geometry type.

| Geometry Type | Measurement |
|---|---|
| Polygon | Area in square metres |
| LineString | Length in metres |
| Point | No measurement required |
| Unsupported geometry | Reported without measurement |

For Polygon geometries, the area is calculated after transforming geographic coordinates to a suitable projected CRS when required.

For LineString geometries, the length is calculated after applying the same CRS handling strategy.

Point geometries do not require a measurement.

Unsupported geometry types are handled gracefully and returned with an explanatory message.

## CRS Handling

Geospatial data can use either geographic or projected coordinate reference systems.

For example, EPSG:4326 represents geographic coordinates using longitude and latitude in degrees.

Area and distance should not be calculated directly from longitude and latitude values because the results would not represent square metres or metres.

The application therefore:

1. Checks whether the uploaded data has a CRS.
2. Checks whether the CRS is geographic.
3. If the CRS is geographic, estimates a suitable local UTM projected CRS.
4. Transforms the geometry to that projected CRS.
5. Calculates area or length using the projected geometry.
6. If the data is already projected, the existing projected CRS is used directly.

If a suitable projected CRS cannot be determined, the application reports an error instead of returning an unreliable measurement.s

## Architecture

The application uses a layered structure so that API routing, geospatial processing, CRS handling, measurements, and database operations remain separated.

### API Layer

**File:**

```text
app/api/routes/files.py
```

Handles HTTP requests, file uploads, responses, and API-level error handling.

### Geospatial Service

**File:**

```text
app/services/geospatial_service.py
```

Responsible for:

- Validating supported file types.
- Validating Shapefile ZIP files.
- Reading KML and Shapefile data.
- Extracting features and their properties.

### CRS Service

**File:**

```text
app/services/crs_service.py
```

Responsible for:

- Reading the input CRS.
- Detecting geographic CRS.
- Estimating a suitable projected CRS.
- Transforming geographic data before measurement.

### Measurement Service

**File:**

```text
app/services/measurement_service.py
```

Responsible for calculating:

- Polygon area.
- LineString length.
- Point handling.
- Unsupported geometry handling.

### Database Service

**File:**

```text
app/services/database_service.py
```

Responsible for:

- Creating the SQLite database table.
- Saving processed file records.
- Retrieving stored file records.

### Models

**File:**

```text
app/models/schemas.py
```

Contains the Pydantic response models used by the API.

### Application Entry Point

**File:**

```text
app/main.py
```

Creates the FastAPI application, initializes the database, and registers the API routes.

## Database

The application uses SQLite for persistent storage.

The database stores:

- File ID
- Original filename
- Feature count
- CRS
- Processing status
- Extracted features
- Calculated measurements

The local database and uploaded files are excluded from Git using `.gitignore`.

## Error Handling

The API handles invalid input without crashing the application.

Examples include:

- Unsupported file extension → HTTP 400
- Invalid ZIP file → HTTP 400
- ZIP without a complete Shapefile → HTTP 400
- Missing file ID → HTTP 404
- Unexpected processing error → HTTP 500

## Testing

The project uses pytest for automated API testing.

Run the complete test suite with:

```bash
pytest
```

The test suite covers:

- Health endpoint
- KML file upload
- Polygon measurement
- Measurements endpoint
- File retrieval
- Unsupported file type
- Invalid ZIP file
- Missing file ID
- Point geometry handling

Current test result:

```text
8 passed
```

## Design Decisions

### FastAPI

FastAPI was selected because it provides a clean REST API structure, automatic OpenAPI documentation, request validation, and straightforward endpoint development.

### GeoPandas

GeoPandas provides support for reading and processing geospatial vector data while working well with CRS transformations.

### Shapely

Shapely is used for geometry operations and calculating geometry measurements such as area and length.

### PyProj

PyProj is used through the geospatial processing stack for coordinate reference system handling and transformations.

### SQLite

SQLite provides simple persistent storage without requiring a separate database server. It keeps the project easy to run locally while demonstrating persistent data storage.

### Layered Architecture

The application separates API routes from geospatial processing, CRS handling, measurements, and database operations. This makes the code easier to maintain and extend.

## Learning

Through this project, I learned how to build a REST API using FastAPI and how to process geospatial vector data using GeoPandas and Shapely.

I also learned how coordinate reference systems affect geospatial measurements and why geographic coordinates should be transformed to a suitable projected CRS before calculating area or distance.

The project also provided practical experience with file validation, persistent SQLite storage, API response models, automated testing, and organizing a Python backend into separate services.

## Future Scope

Possible future improvements include:

- Support for additional geospatial file formats.
- More advanced geometry validation.
- File size and resource limits.
- Background processing for large files.
- Improved logging and monitoring.
- Authentication and authorization.
- PostgreSQL/PostGIS for larger production workloads.
- Additional geospatial measurements and statistics.
- A frontend interface for uploading files and displaying measurements on a map.