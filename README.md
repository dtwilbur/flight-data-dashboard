# flight-data-dashboard
Flight Data Visualization App
This repository contains a full‑stack flight data visualization application built with a Python FastAPI backend and a React frontend. The project demonstrates how to ingest satellite‑derived flight telemetry, store it in a relational database, and present the data through a responsive web dashboard. It is designed as a showcase of modern full‑stack development practices and includes a clean codebase, typed schemas, reusable components and Docker configuration for easy deployment.

Motivation
Flight operations and remote sensing systems produce huge streams of telemetry. Making sense of this information requires a robust ingestion pipeline and a clear user interface. This project is inspired by the architecture used in similar applications: a React frontend communicates with a Python API over REST; the API persists data to a database; and a background job ingests raw telemetry into structured records. Official FastAPI documentation highlights how the framework delivers high performance and ease of use for building APIs by leveraging Python type hints and automatic OpenAPI generation
fastapi.tiangolo.com
. Likewise, the React documentation emphasises its component‑based approach, letting developers build user interfaces by composing small pieces into complete pages
react.dev
.

Features
Data ingestion – A background script (ingest.py) reads comma‑separated satellite telemetry and writes structured Flight and Position rows into a SQLite database via SQLAlchemy.

Typed API – The FastAPI service exposes CRUD endpoints to list flights, fetch flight details and stream the latest positions. FastAPI generates interactive documentation automatically based on the Pydantic models
fastapi.tiangolo.com
.

React dashboard – The frontend is bootstrapped with Vite and Tailwind CSS. Components include a flight table, a detail pane and a map/graph view. React’s declarative component model makes it straightforward to build reusable UI building blocks
react.dev
.

Responsive UI – The dashboard uses responsive layouts to work well on desktop and mobile. Charts are rendered with Chart.js; maps use Leaflet via the react‑leaflet library.

Containerised – A docker-compose.yml orchestrates the backend, frontend and database services for local development. Each service runs in its own container.

Project structure
graphql
Copy
Edit
flight_data_app/
├── backend/                 # FastAPI service and data ingestion
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py          # API routes and startup
│   │   ├── database.py      # SQLAlchemy database session
│   │   ├── models.py        # ORM models
│   │   ├── schemas.py       # Pydantic schemas
│   │   ├── crud.py          # CRUD helpers
│   │   └── ingest.py        # Data ingestion script
│   ├── tests/               # pytest tests (optional)
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/                # React application (Vite + Tailwind)
│   ├── package.json
│   ├── vite.config.js
│   ├── tailwind.config.js
│   └── src/
│       ├── main.jsx
│       ├── App.jsx
│       ├── api.js          # API abstraction
│       └── components/
│           ├── FlightTable.jsx
│           ├── FlightDetails.jsx
│           ├── MapView.jsx
│           └── ChartView.jsx
├── data/
│   └── sample_satellite_data.csv
├── docker-compose.yml
└── README.md
Quickstart
Clone the repository and install dependencies for both backend and frontend:

bash
Copy
Edit
git clone https://github.com/your_username/flight_data_app.git
cd flight_data_app
python3 -m venv .venv && source .venv/bin/activate
pip install -r backend/requirements.txt
cd frontend
npm install
Ingest data – The ingestion script reads raw satellite telemetry (CSV) and writes records into the SQLite database. Run:

bash
Copy
Edit
python backend/app/ingest.py --csv-file data/sample_satellite_data.csv
Start services – Launch the FastAPI backend and the React development server in separate terminals:

bash
Copy
Edit
# Terminal 1
cd backend
uvicorn app.main:app --reload --port 8000

# Terminal 2
cd frontend
npm run dev
Navigate to http://localhost:5173 to see the dashboard. The frontend proxies API calls to the backend running on port 8000.

Docker – Alternatively, run everything with Docker Compose:

bash
Copy
Edit
docker-compose up --build
Extending the project
Data ingestion – Replace sample_satellite_data.csv with real telemetry logs. Extend ingest.py to parse additional fields, handle different file formats (e.g. binary packets) or ingest from an API.

Authentication & caching – Add JWT authentication and caching with Redis following the architecture described in the React + Flask recipe manager article
amlanscloud.com
. Use fastapi-users or fastapi-auth for user management.

Persistent storage – Swap SQLite for PostgreSQL using SQLAlchemy and Dockerised Postgres. Add Alembic migrations to manage schema changes.

Real‑time updates – For near real‑time tracking, serve a WebSocket endpoint via FastAPI (Uvicorn). Use socket.io or stomp.js in React to subscribe to updates. Alternatively, publish telemetry to an MQTT broker as shown in the flight dashboard example
akpolatcem.medium.com
 and subscribe from the frontend.

Deploy to cloud – Containerise the services and deploy to a Kubernetes cluster, or serverless functions, following the production architecture patterns described in the React‑Flask architecture article
amlanscloud.com
.

License
This project is open‑source under the MIT License.
