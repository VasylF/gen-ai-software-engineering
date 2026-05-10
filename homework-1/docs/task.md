Technology Stack
Python
Other technolgies which you will comfortable with
📝 Tasks

Task 1: Core API Implementation (Required) ⭐

Create a REST API with the following endpoints:

Method	Endpoint	Description
POST	/transactions	Create a new transaction
GET	/transactions	List all transactions
GET	/transactions/:id	Get a specific transaction by ID
GET	/accounts/:accountId/balance	Get account balance
Transaction Model:

{
  "id": "string (auto-generated)",
  "fromAccount": "string",
  "toAccount": "string",
  "amount": "number",
  "currency": "string (ISO 4217: USD, EUR, GBP, etc.)",
  "type": "string (deposit | withdrawal | transfer)",
  "timestamp": "ISO 8601 datetime",
  "status": "string (pending | completed | failed)"
}
Requirements:

Use in-memory storage (array or object) — no database required
Validate that amounts are positive numbers
Return appropriate HTTP status codes (200, 201, 400, 404)
Include basic error handling
Task 2: Transaction Validation (Required)

Add validation logic for transactions:

Amount validation: Must be positive, maximum 2 decimal places
Account validation: Account numbers should follow format ACC-XXXXX (where X is alphanumeric)
Currency validation: Only accept valid ISO 4217 currency codes (USD, EUR, GBP, JPY, etc.)
Return meaningful error messages for invalid requests
Example validation error response:

{
  "error": "Validation failed",
  "details": [
    {"field": "amount", "message": "Amount must be a positive number"},
    {"field": "currency", "message": "Invalid currency code"}
  ]
}
Task 3: Basic Transaction History (Required) 

Implement transaction filtering on the GET /transactions endpoint:

Filter by account: ?accountId=ACC-12345
Filter by type: ?type=transfer
Filter by date range: ?from=2024-01-01&to=2024-01-31
Combine multiple filters
Task 4: Additional Features

Implement at least one of the following additional features:

Option A: Transaction Summary Endpoint 📈

GET /accounts/:accountId/summary
Returns:

Total deposits
Total withdrawals
Number of transactions
Most recent transaction date
Option B: Simple Interest Calculation 💰

GET /accounts/:accountId/interest?rate=0.05&days=30
Calculate simple interest on current balance.

Option C: Transaction Export 📤

GET /transactions/export?format=csv
Export transactions as CSV format.

Option D: Rate Limiting 🚦

Implement basic rate limiting:

Maximum 100 requests per minute per IP
Return 429 Too Many Requests when exceeded