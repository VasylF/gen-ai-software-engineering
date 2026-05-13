# 🏦 Homework 1: Banking Transactions API

> **Student Name**: Vasyl Fuchenko
> **Date Submitted**: May 9, 2026
> **AI Tools Used**: GitHub Copilot, Claude AI

---

## 📋 Project Overview

This project implements a REST API for managing banking transactions using Python and Flask. The API provides comprehensive transaction management with validation, filtering, and account balance tracking. It includes all required tasks (1-3) plus an additional feature for account summaries.

### Key Features Implemented

✅ **Task 1: Core API Implementation**
- POST `/transactions` - Create new transactions
- GET `/transactions` - List all transactions
- GET `/transactions/:id` - Get specific transaction details
- GET `/accounts/:accountId/balance` - Check account balance
- In-memory storage with transaction model
- Proper HTTP status codes (200, 201, 400, 404)

✅ **Task 2: Transaction Validation**
- Amount validation (positive, max 2 decimal places)
- Account format validation (ACC-XXXXX)
- ISO 4217 currency code validation
- Structured error responses with detailed field-level messages

✅ **Task 3: Transaction Filtering**
- Filter by account ID
- Filter by transaction type (deposit, withdrawal, transfer)
- Filter by date range (from/to)
- Support for combining multiple filters

✅ **Task 4: Additional Features**
- GET `/accounts/:accountId/summary` - Account transaction summary endpoint
  - Total deposits
  - Total withdrawals
  - Number of transactions
  - Most recent transaction date

## 🛠️ Technology Stack

- **Language**: Python 3.8+
- **Framework**: Flask 3.0.0
- **Dependencies**: Flask-CORS, python-dateutil
- **Storage**: In-memory (no database required)

## 📁 Project Structure

```
homework-1/
├── src/
│   ├── app.py              # Main Flask application with all endpoints
│   ├── requirements.txt    # Python dependencies
│   └── venv/              # Virtual environment (created during setup)
├── demo/                  # Demo files and test scripts
├── docs/
│   ├── task.md           # Project requirements
│   └── screenshots/      # API testing screenshots
├── HOWTORUN.md           # Setup and running instructions
└── README.md             # This file
```

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. Navigate to the project directory:
```bash
cd homework-1/src
```

2. Create and activate virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

### Running the API

```bash
python app.py
```

The API will start on `http://localhost:8000`

## 📚 API Documentation

### Core Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/transactions` | Create a new transaction |
| GET | `/transactions` | List all transactions with optional filters |
| GET | `/transactions/:id` | Get a specific transaction by ID |
| GET | `/accounts/:accountId/balance` | Get account balance |
| GET | `/accounts/:accountId/summary` | Get account transaction summary |
| GET | `/health` | Health check endpoint |

### Example Usage

**Create a Transfer:**
```bash
curl -X POST http://localhost:8000/transactions \
  -H "Content-Type: application/json" \
  -d '{
    "fromAccount": "ACC-11111",
    "toAccount": "ACC-22222",
    "amount": 50.00,
    "currency": "USD",
    "type": "transfer"
  }'
```

**Filter Transactions:**
```bash
# By account
curl "http://localhost:8000/transactions?accountId=ACC-12345"

# By type
curl "http://localhost:8000/transactions?type=transfer"

# By date range
curl "http://localhost:8000/transactions?from=2024-01-01&to=2024-12-31"

# Combined filters
curl "http://localhost:8000/transactions?accountId=ACC-12345&type=transfer"
```

**Get Account Summary:**
```bash
curl http://localhost:8000/accounts/ACC-12345/summary
```

## ✅ Validation Rules

### Amount Validation
- Must be a positive number
- Maximum 2 decimal places

### Account Format
- Must follow pattern: `ACC-XXXXX` where X is alphanumeric
- Applied to both fromAccount and toAccount

### Currency
- Must be valid ISO 4217 code (USD, EUR, GBP, JPY, CHF, etc.)
- Supported currencies: 30+ global currencies

### Transaction Type
- Must be one of: `deposit`, `withdrawal`, `transfer`
- For transfers: fromAccount and toAccount must be different

## 🔍 Error Handling

The API returns structured error responses:

```json
{
  "error": "Validation failed",
  "details": [
    {
      "field": "amount",
      "message": "Amount must be a positive number"
    }
  ]
}
```

HTTP Status Codes:
- **200**: Successful GET request
- **201**: Successful resource creation (POST)
- **400**: Bad request (validation error)
- **404**: Resource not found
- **500**: Server error

## 📊 Data Model

### Transaction Object
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "fromAccount": "ACC-11111",
  "toAccount": "ACC-22222",
  "amount": 50.0,
  "currency": "USD",
  "type": "transfer",
  "timestamp": "2024-01-15T10:30:00Z",
  "status": "completed"
}
```

### Account Summary Object
```json
{
  "accountId": "ACC-12345",
  "balance": 1250.50,
  "currency": "USD",
  "totalDeposits": 5000.00,
  "totalWithdrawals": 3749.50,
  "numberOfTransactions": 12,
  "mostRecentTransactionDate": "2024-01-15T10:30:00Z"
}
```

## 🧪 Testing

See `HOWTORUN.md` for comprehensive testing examples with curl commands.

## 📝 Notes

- All amounts are stored with up to 2 decimal places
- Timestamps are in ISO 8601 format (UTC)
- Account balances are tracked per currency
- The API is stateless - all data is reset when the server restarts
- CORS is enabled for cross-origin requests

## 🎓 Learning Outcomes

This project demonstrates:
- RESTful API design principles
- Input validation and error handling
- In-memory data persistence
- Query parameter filtering and date handling
- Python Flask framework best practices
- HTTP status code usage

<div align="center">

*This project was completed as part of the AI-Assisted Development course.*

</div>
