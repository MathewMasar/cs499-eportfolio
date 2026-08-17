# Grazioso Salvare Animal Shelter Dashboard

This enhanced CS-499 database artifact redesigns the original CS-340 animal shelter dashboard into a modular, database-driven web application for animal rescue filtering, shelter record searching, geospatial visualization, and administrative reporting.

The application uses Python, Dash, MongoDB, PyMongo, Pandas, Plotly, and Dash Leaflet. The enhanced application runs independently as a standalone Dash application through `app.py`.

## Dashboard Views

### Rescue Dashboard

The Rescue Dashboard supports the operational rescue-animal workflow.

Users can:

- View shelter records in an interactive data table
- Filter candidates for Water Rescue
- Filter candidates for Mountain / Wilderness Rescue
- Filter candidates for Disaster / Tracking Rescue
- Reset the dashboard to the complete shelter dataset
- Sort and filter displayed records
- View rescue-candidate and breed-distribution charts
- Select an animal and display its shelter location on an interactive map

The rescue filters use breed, sex, and age requirements to identify animals that meet the criteria for each rescue program.

### Search Dashboard

The Search Dashboard provides multi-criteria shelter record searching.

Search criteria include:

- Animal type
- Breed
- Outcome type
- Minimum age in weeks
- Maximum age in weeks

Breed options are loaded dynamically based on the selected animal type. Age values are validated before a search is executed, and invalid ranges are rejected.

Search results are displayed in a sortable, filterable, paginated table.

### Admin / Reporting Dashboard

The Admin / Reporting Dashboard uses MongoDB aggregation pipelines to convert shelter records into reporting metrics and visualizations.

Reports include:

- Total animal records
- Total adoptions
- Overall adoption rate
- Shelter outcome distribution
- Adoption rate by animal type
- Adoption rate among the ten most-adopted breeds
- Adoption statistics by age group

The top-breed report ranks breeds by completed adoption count and excludes breeds with no adoption records. Hover information provides the number adopted, total records, and adoption rate for each displayed breed.

## Database Enhancements

The enhanced `AnimalRepository` separates database operations from connection management and dashboard presentation.

The repository provides:

- Create, Read, Update, and Delete operations
- Duplicate `animal_id` prevention
- Automatic record-number generation
- Validation of update and delete targets
- Protection against unsafe or overly broad modifications
- Multi-criteria animal searching
- Dynamic breed retrieval by animal type
- GeoJSON location generation
- Nearby-animal geospatial searching
- MongoDB index creation
- PyMongo error handling

## MongoDB Indexing

The repository can create indexes for fields frequently used by the application:

```text
animal_id
animal_type
breed
outcome_type
location (2dsphere)
```

The `location` field uses a MongoDB `2dsphere` index to support geospatial queries.

## Geospatial Data

Animal records containing valid latitude and longitude values can be converted into MongoDB GeoJSON points.

GeoJSON coordinates are stored in MongoDB's required order:

```text
[longitude, latitude]
```

Example:

```json
{
    "type": "Point",
    "coordinates": [-97.34087807, 30.50665787]
}
```

The Rescue Dashboard uses shelter coordinates to display the selected animal on an interactive map.

## Project Structure

The enhanced project separates responsibilities across database, repository, reporting, layout, and callback modules.

```text
animal-shelter-dashboard/
│
├── app.py
├── config.py
├── database.py
├── animal_repository.py
├── reporting_service.py
├── requirements.txt
├── README.md
├── .env.example
├── .gitignore
│
├── data/
│   └── aac_shelter_outcomes.csv
│
├── layouts/
│   ├── __init__.py
│   ├── rescue_layout.py
│   ├── search_layout.py
│   └── admin_layout.py
│
├── callbacks/
│   ├── __init__.py
│   ├── rescue_callbacks.py
│   ├── search_callbacks.py
│   └── admin_callbacks.py
│
└── tests/
    ├── test_animal_repository.py
    ├── test_database.py
    └── test_reporting_service.py
```

Generated and machine-specific directories such as `.pytest_cache`, `__pycache__`, `.vscode`, and local virtual environments are intentionally excluded from the project structure above.

## Main Components

### `app.py`

The application entry point.

It:

- Creates the shared database connection
- Creates the animal repository
- Creates the reporting service
- Registers Rescue Dashboard callbacks
- Registers Search Dashboard callbacks
- Registers Admin Dashboard callbacks
- Defines dashboard navigation
- Starts the Dash web server

### `config.py`

Loads MongoDB configuration from environment variables.

This keeps database connection settings separate from the application source code.

### `database.py`

Manages the shared MongoDB connection used throughout the application.

It also provides a database health check that can verify whether the configured MongoDB server is reachable.

### `animal_repository.py`

Contains the enhanced database-access layer for animal records.

Responsibilities include:

- CRUD operations
- Input validation
- Duplicate prevention
- Record-number generation
- Multi-criteria searching
- Breed retrieval
- MongoDB indexing
- GeoJSON generation
- Geospatial searching
- Database error handling

### `reporting_service.py`

Contains the MongoDB aggregation pipelines used by the Admin / Reporting Dashboard.

The reporting service keeps analytical queries separate from normal CRUD and search operations.

### `layouts/`

Contains the presentation structure for each dashboard:

```text
rescue_layout.py
search_layout.py
admin_layout.py
```

### `callbacks/`

Contains the interactive Dash callback logic for each dashboard:

```text
rescue_callbacks.py
search_callbacks.py
admin_callbacks.py
```

Separating layouts from callbacks reduces the amount of UI and application logic contained in a single file and makes the dashboard easier to maintain.

### `tests/`

Contains the automated pytest suite:

```text
test_animal_repository.py
test_database.py
test_reporting_service.py
```

### `data/aac_shelter_outcomes.csv`

Contains the AAC animal shelter dataset used to populate the MongoDB `animals` collection.

### `CRUD_Python_Module.py`

Preserves the AnimalShelter CRUD implementation associated with the original artifact.

The enhanced dashboard application itself uses the separated `DatabaseConnection`, `AnimalRepository`, and `ReportingService` architecture.

## Environment Configuration

Database configuration is loaded from environment variables rather than placing credentials directly in the enhanced application source code.

The application expects the following values:

```text
MONGO_HOST=localhost
MONGO_PORT=27017
MONGO_DB=aac
MONGO_COLLECTION=animals

MONGO_USERNAME=
MONGO_PASSWORD=
```

The repository includes `.env.example` as a configuration template.

A local `.env` file should be created from this template before running the application.

### Windows PowerShell

```bash
Copy-Item .env.example .env
```

### macOS / Linux

```bash
cp .env.example .env
```

If the local MongoDB instance does not require authentication, the username and password values may remain blank.

> **Important:** Do not commit `.env` to source control. The included `.gitignore` excludes the local environment file so credentials and machine-specific configuration are not stored in the repository.

## Requirements

The enhanced application requires:

- Python
- MongoDB
- MongoDB Database Tools for `mongoimport`

Python dependencies are defined in `requirements.txt`:

```text
dash==4.4.1
dash-leaflet==1.1.3
pandas==3.0.5
plotly==6.9.0
pymongo==4.17.0
python-dotenv==1.2.3
pytest==9.1.1
```

Jupyter is not required to run the enhanced application.

## Setup

### 1. Clone or Download the Repository

Clone or download the project and navigate to the enhanced dashboard directory:

```bash
cd animal-shelter-dashboard
```

### 2. Create a Virtual Environment

#### Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```

#### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies

With the virtual environment activated, install the required Python packages:

```bash
python -m pip install -r requirements.txt
```

### 4. Configure MongoDB

Make sure a MongoDB server is installed and running.

The default application configuration uses:

```text
Host: localhost
Port: 27017
Database: aac
Collection: animals
```

If your MongoDB configuration is different, update the corresponding values in `.env`.

### 5. Import the AAC Shelter Dataset

The repository includes the shelter dataset at:

```text
data/aac_shelter_outcomes.csv
```

From the project root, import the dataset into MongoDB with:

```bash
mongoimport --db aac --collection animals --type csv --headerline --file data/aac_shelter_outcomes.csv
```

This creates or populates:

```text
Database: aac
Collection: animals
```

If the `animals` collection already contains the dataset, do not import it again unless you intend to rebuild the collection.

To intentionally rebuild the collection from the included dataset, use:

```bash
mongoimport --db aac --collection animals --type csv --headerline --drop --file data/aac_shelter_outcomes.csv
```

> **Warning:** The `--drop` option deletes the existing `animals` collection before importing the dataset. Use it only when you intentionally want to rebuild the collection.

### 6. Create the Environment File

Copy the example configuration.

#### Windows PowerShell

```bash
Copy-Item .env.example .env
```

#### macOS / Linux

```bash
cp .env.example .env
```

For the default local MongoDB configuration, the resulting `.env` can use:

```text
MONGO_HOST=localhost
MONGO_PORT=27017
MONGO_DB=aac
MONGO_COLLECTION=animals

MONGO_USERNAME=
MONGO_PASSWORD=
```

If authentication is enabled on the MongoDB server, enter the appropriate username and password.

## Automated Testing

The project includes **20 pytest tests** covering the database connection, repository operations, validation, searching, geospatial functionality, and reporting service.

### Animal Repository Tests

The `test_animal_repository.py` suite verifies:

- Animal creation
- Duplicate animal ID rejection
- Multi-filter animal searching
- Invalid age-range rejection
- Automatic GeoJSON location generation
- Nearby-animal geospatial searching
- Valid record updates
- Protection of `animal_id` during updates
- Empty-update rejection
- Valid record deletion
- Rejection of broad delete queries

Temporary test records are removed after testing so the imported AAC dataset is preserved.

### Database Tests

The `test_database.py` suite verifies:

- MongoDB health-check connectivity
- Access to the configured animals collection
- Presence of imported AAC shelter records

### Reporting Service Tests

The `test_reporting_service.py` suite verifies:

- Overall adoption summaries
- Adoption statistics by animal type
- Breed adoption statistics and result limits
- Rejection of invalid breed-report limits
- Adoption statistics by age group
- Outcome distribution percentages

## Run Tests

Make sure MongoDB is running and the AAC dataset has been imported.

From the project root, run:

```bash
python -m pytest
```

A successful run should end with output similar to:

```text
============================= 20 passed =============================
```

The exact execution time may vary by system.

## Run the Dashboard

Before starting the application, make sure:

- The virtual environment is activated
- Required Python packages are installed
- MongoDB is running
- The AAC dataset has been imported
- `.env` has been configured

Run the application from the project root:

```bash
python app.py
```

At startup, the application performs a MongoDB health check and starts the Dash web server.

The terminal will display the local address for the application. Open that address in a web browser.

The application contains three dashboard views:

```text
Rescue Dashboard
Search Dashboard
Admin / Reporting
```

## Original vs. Enhanced Artifact

The original CS-340 artifact consisted of a Jupyter-based animal shelter dashboard and MongoDB CRUD functionality.

For the CS-499 enhancement, the application was redesigned as a standalone, modular Dash web application.

The enhanced version separates database connectivity, repository operations, reporting logic, dashboard layouts, callbacks, configuration, and automated testing into dedicated Python modules.

Major enhancements include:

- Modular application architecture
- Standalone Dash application execution
- Environment-based database configuration
- Shared MongoDB connection management
- Expanded CRUD validation
- Safer update and delete operations
- Advanced multi-criteria searching
- Dynamic breed filtering
- MongoDB indexing
- GeoJSON data support
- Geospatial searching
- Interactive map visualization
- Administrative aggregation reports
- Adoption metrics and visualizations
- Automated pytest coverage
- Separation of presentation, interaction, database, and reporting logic

## Technologies

```text
Python
Dash
MongoDB
PyMongo
Pandas
Plotly
Dash Leaflet
python-dotenv
pytest
```

## Security and Data Integrity

The enhanced application improves database safety by:

- Loading database connection settings from environment variables
- Keeping `.env` out of source control
- Removing the need for hardcoded credentials in the enhanced application
- Validating data before database operations
- Rejecting duplicate animal identifiers
- Requiring targeted update and delete operations
- Protecting identifying fields from unsafe modification
- Validating geographic coordinates before creating GeoJSON data
- Handling PyMongo database errors
- Testing data-integrity rules with automated tests

## Portfolio Purpose

This project was enhanced for the CS-499 Computer Science Capstone as a database-focused ePortfolio artifact.

The enhancement demonstrates practical experience with:

- Database-backed application design
- MongoDB query and aggregation development
- CRUD operations
- Database indexing
- Geospatial data
- Data validation
- Secure configuration
- Modular software architecture
- Interactive dashboard development
- Data visualization
- Automated testing
- Refactoring an existing application into a more maintainable design