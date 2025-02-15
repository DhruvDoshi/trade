# Trading Application with Angel One Integration

## Overview
This project aims to develop a comprehensive trading application tailored for the Indian stock markets, leveraging Angel One's SmartAPI for real-time data acquisition, order execution, and portfolio management. The application is designed with a modular architecture to ensure scalability, maintainability, and robustness.

## Features
- **Market Data Acquisition**: Real-time streaming of market data using WebSockets and REST APIs.
- **Analytics & Signal Generation**: Implementation of technical indicators (e.g., RSI, MACD, Moving Averages) and custom trading strategies.
- **Risk Management**: Enforcement of trading limits, position sizing, and automated stop-loss mechanisms.
- **Order Execution Engine**: Seamless integration with Angel One's API for order placement, modification, and cancellation.
- **Backtesting Framework**: Simulation of trading strategies against historical data to evaluate performance.
- **User Dashboard**: Interactive web-based interface for monitoring market trends, managing portfolios, and executing trades.

## Architecture
The application follows a modular architecture, inspired by the C4 Model and Hexagonal Architecture, ensuring a clear separation of concerns and facilitating ease of testing and maintenance.

## Modules
1. **Market Data Module**: Fetches and processes live market data from Angel One's SmartAPI.
2. **Analytics & Signal Generation Module**: Analyzes market data to generate trading signals.
3. **Risk Management Module**: Monitors and controls trading risks.
4. **Order Execution Engine**: Manages order lifecycle with the brokerage.
5. **Backtesting Framework**: Evaluates trading strategies using historical data.
6. **User Dashboard**: Provides a web interface for user interactions.
7. **Database & Storage**: Stores market data, user profiles, portfolios, and transactions.

## Installation & Setup

### Prerequisites
- Python 3.8+
- Node.js 14+
- PostgreSQL
- Redis

### Steps
1. **Clone the Repository**
    ```sh
    git clone https://github.com/your-username/trading-app.git
    cd trading-app
    ```

2. **Set Up Environment Variables**
    Create a `.env` file in the root directory with the following content:
    ```env
    ### Angel One API Credentials
    API_KEY=your_angel_one_api_key
    CLIENT_ID=your_client_id
    PASSWORD=your_password

    ### Database Configuration
    DB_HOST=localhost
    DB_PORT=5432
    DB_NAME=trading_db
    DB_USER=your_db_username
    DB_PASSWORD=your_db_password

    ### Redis Configuration
    REDIS_URL=redis://localhost:6379
    ```

3. **Install Backend Dependencies**
    ```sh
    cd backend
    python -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```

4. **Apply Database Migrations**
    ```sh
    alembic upgrade head
    ```

5. **Install Frontend Dependencies**
    ```sh
    cd ../frontend
    npm install
    ```

6. **Start the Application**
    - **Backend Server**
        ```sh
        cd ../backend
        uvicorn main:app --reload
        ```
    - **Frontend Server**
        ```sh
        cd ../frontend
        npm start
        ```

## Project Structure
```markdown
trading-app/
├── backend/
│   ├── main.py                 # Entry point for FastAPI backend
│   ├── market_data/
│   │   ├── fetcher.py          # Fetches market data
│   │   └── processor.py        # Processes market data
│   ├── analytics/
│   │   ├── indicators.py       # Technical indicators calculations
│   │   └── signals.py          # Signal generation
│   ├── risk_management/
│   │   └── risk_evaluator.py   # Risk assessment logic
│   ├── order_execution/
│   │   └── order_manager.py    # Order execution and management
│   ├── backtesting/
│   │   └── backtester.py       # Backtesting framework
│   ├── database/
│   │   ├── models.py           # Database models
│   │   └── session.py          # Database session
│   └── config.py               # Configuration settings
├── frontend/
│   ├── public/                 # Public assets
│   ├── src/
│   │   ├── components/         # React components
│   │   ├── pages/              # React pages
│   │   ├── services/           # API service calls
│   │   └── App.js              # Main React app
