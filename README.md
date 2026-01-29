# Auction Service

Real-time auction service built with FastAPI, PostgreSQL, and WebSocket support for live bid updates.

## Features

- REST API for managing auction lots and bids
- WebSocket support for real-time bid notifications
- Async SQLAlchemy with PostgreSQL
- Three-layer architecture (Presentation, Business Logic, Data Access)
- Docker containerization with docker-compose
- Database migrations with Alembic

## Project Structure

```
UDATA_test_task/
├── app/
│   ├── main.py                 # FastAPI application entry point
│   ├── database.py             # Database configuration
│   ├── dependencies.py        # Dependency injection
│   ├── websocket.py            # WebSocket connection manager
│   ├── api/                    # Presentation Layer
│   │   └── endpoints.py        # REST API endpoints
│   ├── services/               # Business Logic Layer
│   │   ├── base_service.py
│   │   ├── lot_service.py
│   │   └── bid_service.py
│   ├── repositories/           # Data Access Layer
│   │   ├── base_repository.py
│   │   ├── lot_repository.py
│   │   └── bid_repository.py
│   ├── models/                 # SQLAlchemy models
│   │   ├── base_model.py
│   │   ├── lot_model.py
│   │   └── bid_model.py
│   └── schemas/                # Pydantic schemas
│       ├── lot_schema.py
│       └── bid_schema.py
├── migrations/                 # Alembic migrations
│   └── versions/
├── alembic.ini                 # Alembic configuration
├── .env                        # Environment variables
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

## Quick Start

### Using Docker (Recommended)

1. Clone the repository and navigate to the project directory:
   ```bash
   cd UDATA_test_task
   ```

2. Create `.env` file with database configuration:
   ```env
   DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5435/auction_db
   POSTGRES_USER=postgres
   POSTGRES_PASSWORD=postgres
   POSTGRES_DB=auction_db
   ```

3. Build and start the services:
   ```bash
   docker-compose up --build
   ```

4. The API will be available at `http://localhost:8000`
   - Swagger documentation: `http://localhost:8000/docs`
   - ReDoc documentation: `http://localhost:8000/redoc`
   - Root endpoint: `http://localhost:8000/`


## API Endpoints

#### Create a Lot
```http
POST /api/lots
Content-Type: application/json

{
  "title": "Vintage Watch",
  "description": "A beautiful vintage watch",
  "start_price": 100.0,
  "end_time": "2024-12-31T23:59:59"
}
```

#### Get Active Lots
```http
GET /api/lots?skip=0&limit=100
```

#### Get Lot Details
```http
GET /api/lots/{lot_id}
```

#### Place a Bid
```http
POST /api/lots/{lot_id}/bids
Content-Type: application/json

{
  "bidder_name": "John Doe",
  "amount": 150.0
}
```

#### Get Bid History
```http
GET /api/lots/{lot_id}/bids
```

### WebSocket API

Connect to real-time bid updates:

```javascript
const ws = new WebSocket('ws://localhost:8000/ws/lots/{lot_id}');

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log('New bid:', data);
  // {
  //   "type": "bid_placed",
  //   "lot_id": 1,
  //   "bidder": "John Doe",
  //   "amount": 150.0
  // }
};
```