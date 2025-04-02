# Risk Monitoring System Backend

This is the backend for the Risk Monitoring System, built with FastAPI. It provides APIs for managing clients, positions, market data, and margin calculations.

## Overview

This application is a risk monitoring system built with the following architecture:

- **Frontend**: Next.js
- **Backend**: FastAPI
- **Real-time Updates**: WebSockets
- **Data Provider**: Twelve Data API for financial data

The system is designed to provide real-time updates and insights based on market data. It retrieves data from the Twelve Data API and pushes updates to the frontend through WebSockets.

## Architecture

### Frontend (Next.js)

The frontend is built using **Next.js**, a React framework that enables server-side rendering, static site generation, and easy routing. The frontend interacts with the backend through API endpoints and subscribes to WebSocket connections for real-time data updates.

**Key Features**:

- Fetching and displaying market data via RESTful APIs
- Real-time updates via WebSocket connections
- Responsive and user-friendly interface

### Backend (FastAPI)

The backend is built using **FastAPI**, a modern web framework for Python that allows for fast API development with automatic validation and asynchronous support. The backend is responsible for:

- Interfacing with the Twelve Data API to retrieve market data
- Providing endpoints to fetch historical and real-time market data
- Establishing WebSocket connections for real-time updates to the frontend

**Key Features**:

- REST API for data retrieval
- WebSocket implementation for real-time updates
- Integration with Twelve Data API for market data

### Real-time Data Updates (WebSockets)

To provide real-time updates, the backend uses **WebSockets**. The frontend listens to the WebSocket connection to get live data feeds and updates the UI dynamically.

### Data Retrieval (Twelve Data API)

The system retrieves financial data from the **Twelve Data API**, which offers real-time and historical stock market data. The API is used to fetch market data for display and analysis.

## Prerequisites

Before running the application, ensure you have the following installed:

- Python 3.11
- Docker and Docker Compose
- PostgreSQL (if not using Docker for the database)

## Backend Setup Instructions

You can set up the backend either locally or using Docker. Follow the appropriate instructions below.

### **1. Local Setup**

#### Prerequisites

- Python 3.11 installed
- PostgreSQL installed and running
- `pip` and `virtualenv` installed

#### Steps

1. Clone the repository:

   ```bash
   git clone <repository-url>
   cd risk-monitoring-backend
   ```

2. Create and activate a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Set up the `.env` file:
   Create a `.env` file in the root directory with the following content:

   ```env
   DATABASE_URL=postgresql://<username>:<password>@localhost:5432/<database_name>
   TWELVE_DATA_API_KEY=<your-twelve-data-api-key>
   TWELVE_DATA_API_URL=https://api.twelvedata.com/
   TWELVE_DATA_WEBSOCKET_URL=wss://ws.twelvedata.com/v1/
   ```

5. Apply database migrations:

   ```bash
   alembic upgrade head
   ```

6. Start the backend server:

   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8000
   ```

7. Access the API at `http://127.0.0.1:8000`.

---

### **2. Docker Setup**

#### Prerequisites

- Docker and Docker Compose installed

#### Steps

1. Clone the repository:

   ```bash
   git clone <repository-url>
   cd risk-monitoring-backend
   ```

2. Set up the `.env` file:
   Create a `.env` file in the root directory with the following content:

   ```env
   DATABASE_URL=postgresql://riskuser:TAKEHOMEASSIGNMENT@db:5432/riskdb
   TWELVE_DATA_API_KEY=<your-twelve-data-api-key>
   TWELVE_DATA_API_URL=https://api.twelvedata.com/
   TWELVE_DATA_WEBSOCKET_URL=wss://ws.twelvedata.com/v1/
   ```

3. Start the backend and database services:

   ```bash
   docker-compose up
   ```

4. Apply database migrations:

   ```bash
   docker-compose exec backend alembic upgrade head
   ```

5. Stop the services:

   ```bash
   docker-compose down
   ```

6. Restart the backend and database services:

   ```bash
   docker-compose up
   ```

7. Access the API at `http://127.0.0.1:8000`.

---

## Running the Application Locally

Follow these steps to run the application locally:

1. Clone the repository:

   ```bash
   git clone <repository-url>
   cd risk-monitoring-backend
   ```

2. Set up environment variables:
   Create a `.env` file in the root directory with the required content (see above).

3. Start the database:

   ```bash
   docker-compose up db
   ```

4. Install dependencies:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

5. Apply database migrations:

   ```bash
   alembic upgrade head
   ```

6. Start the application:

   ```bash
   uvicorn app.main:app --reload
   ```

7. Access the API documentation at `http://127.0.0.1:8000/docs`.

---

## API Usage

The following APIs are available:

### Clients

- **Create a Client**: `POST /api/clients`  
  Create a new client by providing the required client details in the request body.
- **Get a Client**: `GET /api/clients/{client_id}`  
  Retrieve details of a specific client by their unique ID.
- **Update Client Loan**: `PUT /api/clients/{client_id}`  
  Update the loan details of a specific client by their unique ID.
- **Delete a Client**: `DELETE /api/clients/{client_id}`  
  Remove a client from the system by their unique ID.

### Positions

- **Create a Position**: `POST /api/positions`  
  Add a new position for a client by providing the required details in the request body.
- **Get Positions by Client**: `GET /api/positions/client/{client_id}`  
  Retrieve all positions associated with a specific client.
- **Update a Position**: `PUT /api/positions/{position_id}`  
  Modify the details of an existing position by its unique ID.
- **Delete a Position**: `DELETE /api/positions/{position_id}`  
  Remove a position from the system by its unique ID.

### Market Data

- **Get All Market Data**: `GET /api/market-data/all`  
  Retrieve market data for all instruments.
- **Get Market Data by Client**: `GET /api/market-data/client/{client_id}`  
  Retrieve market data relevant to a specific client.
- **Get Market Data by Instrument**: `GET /api/market-data/instrument?instrument={symbol}:{exchange}`  
  Retrieve market data for a specific instrument by providing its symbol and exchange.
- **Get Market History**: `GET /api/market-history/all`  
  Retrieve historical market data for all instruments.

### Margin

- **Get Margin Status**: `GET /api/margin-status/{client_id}`  
  Retrieve the margin status of a specific client, including margin requirements and utilization.

### WebSocket

- **Connect to WebSocket**: `ws://127.0.0.1:8000/ws/{client_id}`  
  Establish a WebSocket connection to receive real-time updates for a specific client.

---

## Testing

Due to time constraints, automated tests for the backend were not fully implemented. Instead, testing was conducted manually by:

1. Sending API requests to the backend endpoints using tools like [Postman](https://www.postman.com/) or `curl`.
2. Verifying the responses to ensure they match the expected behavior.
3. Checking the database directly to confirm that the data is being updated correctly.
4. Reviewing the application logs to identify any errors or unexpected behavior.

For future improvements, automated tests using `pytest` and `FastAPI`'s `TestClient` are recommended to ensure comprehensive test coverage and faster validation of changes.

## Limitations of Twelve Data WebSocket and API (Free Tier)

While Twelve Data provides powerful financial data through their WebSocket and API services, the **Free Tier** comes with certain limitations. Please keep the following in mind when using the free tier:

### API Limitations:
1. **Request Limits**: The free tier has a **limit of 800 requests per day**. This can be easily exhausted if you're making frequent requests. Be sure to plan your API calls accordingly.
2. **Data Types**: The free tier may have limited access to certain data types and endpoints. For instance, you might have restricted access to premium features such as historical data, advanced indicators, or more granular market data.
3. **Rate Limits**: There are **rate limits on the API**. Requests made too quickly in succession may result in temporary blocks or throttling.
4. **No Extended Historical Data**: You may not have access to the full range of historical data on the free tier, as it is often limited to recent data points (e.g., last 30 days).
5. **No Support for Advanced Features**: Features such as **intraday data** or **financial data APIs** beyond basic stock quotes may not be accessible in the free tier.
6. **Limited API Endpoints**: The free tier may provide access to only basic endpoints. More advanced functionalities like **multiple symbols per request** or **streaming data** may require upgrading to a paid plan.

### WebSocket Limitations:
1. **Connection Limits**: The free-tier WebSocket connection supports only **one connection per user**. If you're building a multi-user or multi-connection service, you’ll need to consider upgrading to a higher tier.
2. **Limited Symbol Subscriptions**: WebSockets on the free tier can only subscribe to **specific symbols**. You are restricted to a smaller set of symbols and cannot subscribe to multiple symbols or use wildcard subscriptions.
3. **Data Stream Limits**: The data streams for the free tier are typically limited to basic information and fewer symbols. You may experience interruptions in the data stream or be restricted from accessing certain market data.
4. **Limited Data Depth**: WebSocket on the free tier may provide **less frequent updates** and may limit the depth of data for some instruments. You could receive data at a lower frequency or with a delay compared to premium users.
5. **Inactive Connections**: WebSocket connections may be **terminated after inactivity** or could be disconnected more frequently for free-tier users compared to those on paid plans.  

For more information about Twelve Data's WebSocket limitations, visit [https://support.twelvedata.com/en/articles/5335783-trial](https://support.twelvedata.com/en/articles/5335783-trial)

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
