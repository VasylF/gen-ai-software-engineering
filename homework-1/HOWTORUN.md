# ▶️ How to Run the Banking Transactions API

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

## Setup

1. Navigate to the project directory:
```bash
cd homework-1/src
```

2. Create a virtual environment (recommended):
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the API

Start the Flask development server:
```bash
python app.py
```

The API will be available at `http://localhost:8000`

### Running on a Custom Port

If port 8000 is in use, you can specify a different port:
```bash
python -c "from app import app; app.run(debug=True, port=3000)"
```

## Testing the API

### Health Check
```bash
curl http://localhost:8000/health
```

### Create a Transaction (Deposit)
```bash
curl -X POST http://localhost:8000/transactions \
  -H "Content-Type: application/json" \
  -d '{
    "fromAccount": "ACC-00000",
    "toAccount": "ACC-12345",
    "amount": 100.50,
    "currency": "USD",
    "type": "deposit"
  }'
```

### Create a Transaction (Transfer)
```bash
curl -X POST http://localhost:8000/transactions \
  -H "Content-Type: application/json" \
  -d '{
    "fromAccount": "ACC-11111",
    "toAccount": "ACC-22222",
    "amount": 50.00,
    "currency": "EUR",
    "type": "transfer"
  }'
```

### Create a Transaction (Withdrawal)
```bash
curl -X POST http://localhost:8000/transactions \
  -H "Content-Type: application/json" \
  -d '{
    "fromAccount": "ACC-12345",
    "toAccount": "ACC-00000",
    "amount": 25.75,
    "currency": "USD",
    "type": "withdrawal"
  }'
```

### Get All Transactions
```bash
curl http://localhost:8000/transactions
```

### Filter Transactions by Account
```bash
curl "http://localhost:8000/transactions?accountId=ACC-12345"
```

### Filter Transactions by Type
```bash
curl "http://localhost:8000/transactions?type=transfer"
```

### Filter Transactions by Date Range
```bash
curl "http://localhost:8000/transactions?from=2024-01-01&to=2024-12-31"
```

### Combine Multiple Filters
```bash
curl "http://localhost:8000/transactions?accountId=ACC-12345&type=transfer&from=2024-01-01"
```

### Get a Specific Transaction
```bash
curl http://localhost:8000/transactions/<transaction-id>
```

### Get Account Balance
```bash
curl http://localhost:8000/accounts/ACC-12345/balance
```

### Get Account Summary (Task 4)
```bash
curl http://localhost:8000/accounts/ACC-12345/summary
```

## API Response Examples

### Successful Transaction Creation (201 Created)
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

### Validation Error (400 Bad Request)
```json
{
  "error": "Validation failed",
  "details": [
    {
      "field": "amount",
      "message": "Amount must be a positive number"
    },
    {
      "field": "currency",
      "message": "Invalid currency code. Must be a valid ISO 4217 code (e.g., USD, EUR, GBP)"
    }
  ]
}
```

### Account Balance Response (200 OK)
```json
{
  "accountId": "ACC-12345",
  "balance": 125.5,
  "currency": "USD"
}
```

### Account Summary Response (200 OK)
```json
{
  "accountId": "ACC-12345",
  "balance": 125.5,
  "currency": "USD",
  "totalDeposits": 250.75,
  "totalWithdrawals": 125.25,
  "numberOfTransactions": 5,
  "mostRecentTransactionDate": "2024-01-15T10:30:00Z"
}
```

## Deactivating Virtual Environment

When done, deactivate the virtual environment:
```bash
deactivate
```