"""
Banking Transactions REST API
Implements core transaction endpoints with validation and filtering
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
from dateutil import parser as date_parser
import uuid
import re

app = Flask(__name__)
CORS(app)

# In-memory storage
transactions = []
accounts = {}

# ISO 4217 currency codes
VALID_CURRENCIES = {
    'USD', 'EUR', 'GBP', 'JPY', 'CHF', 'CAD', 'AUD', 'NZD', 'CNY', 'INR',
    'MXN', 'SGD', 'HKD', 'NOK', 'SEK', 'DKK', 'ZAR', 'KRW', 'TRY', 'RUB',
    'BRL', 'THB', 'MYR', 'PHP', 'IDR', 'VND', 'PKR', 'BDT', 'NGN', 'KES'
}

# ==================== VALIDATION FUNCTIONS ====================

def validate_amount(amount):
    """Validate that amount is positive and has max 2 decimal places"""
    errors = []
    
    try:
        amount_float = float(amount)
    except (TypeError, ValueError):
        errors.append({
            "field": "amount",
            "message": "Amount must be a valid number"
        })
        return errors
    
    if amount_float <= 0:
        errors.append({
            "field": "amount",
            "message": "Amount must be a positive number"
        })
    
    # Check decimal places
    amount_str = str(amount)
    if '.' in amount_str:
        decimal_places = len(amount_str.split('.')[1])
        if decimal_places > 2:
            errors.append({
                "field": "amount",
                "message": "Amount must have maximum 2 decimal places"
            })
    
    return errors


def validate_account_format(account):
    """Validate account format: ACC-XXXXX (where X is alphanumeric)"""
    errors = []
    pattern = r'^ACC-[A-Za-z0-9]{5}$'
    
    if not re.match(pattern, str(account)):
        errors.append({
            "field": "account",
            "message": "Account must follow format ACC-XXXXX (where X is alphanumeric)"
        })
    
    return errors


def validate_currency(currency):
    """Validate ISO 4217 currency code"""
    errors = []
    
    if currency.upper() not in VALID_CURRENCIES:
        errors.append({
            "field": "currency",
            "message": f"Invalid currency code. Must be a valid ISO 4217 code (e.g., USD, EUR, GBP)"
        })
    
    return errors


def validate_transaction_type(trans_type):
    """Validate transaction type"""
    errors = []
    valid_types = ['deposit', 'withdrawal', 'transfer']
    
    if trans_type not in valid_types:
        errors.append({
            "field": "type",
            "message": f"Type must be one of: {', '.join(valid_types)}"
        })
    
    return errors


def validate_transaction_request(data):
    """Validate entire transaction request"""
    errors = []
    
    # Validate amount
    if 'amount' not in data:
        errors.append({"field": "amount", "message": "Amount is required"})
    else:
        errors.extend(validate_amount(data['amount']))
    
    # Validate currency
    if 'currency' not in data:
        errors.append({"field": "currency", "message": "Currency is required"})
    else:
        errors.extend(validate_currency(data['currency']))
    
    # Validate transaction type
    if 'type' not in data:
        errors.append({"field": "type", "message": "Type is required"})
    else:
        errors.extend(validate_transaction_type(data['type']))
    
    # Validate accounts
    if 'fromAccount' not in data:
        errors.append({"field": "fromAccount", "message": "From account is required"})
    else:
        errors.extend(validate_account_format(data['fromAccount']))
    
    if 'toAccount' not in data:
        errors.append({"field": "toAccount", "message": "To account is required"})
    else:
        errors.extend(validate_account_format(data['toAccount']))
    
    # Validate transfer type
    if data.get('type') == 'transfer':
        if data.get('fromAccount') == data.get('toAccount'):
            errors.append({
                "field": "accounts",
                "message": "From and to accounts must be different for transfers"
            })
    
    return errors


# ==================== TRANSACTION ENDPOINTS ====================

@app.route('/transactions', methods=['POST'])
def create_transaction():
    """Create a new transaction"""
    data = request.get_json()
    
    if not data:
        return jsonify({"error": "Request body must be valid JSON"}), 400
    
    # Validate transaction
    validation_errors = validate_transaction_request(data)
    if validation_errors:
        return jsonify({
            "error": "Validation failed",
            "details": validation_errors
        }), 400
    
    # Create transaction object
    transaction = {
        "id": str(uuid.uuid4()),
        "fromAccount": data['fromAccount'],
        "toAccount": data['toAccount'],
        "amount": float(data['amount']),
        "currency": data['currency'].upper(),
        "type": data['type'],
        "timestamp": datetime.utcnow().isoformat() + 'Z',
        "status": "completed"  # Default to completed for in-memory storage
    }
    
    # Store transaction
    transactions.append(transaction)
    
    # Update account balances
    update_account_balances(transaction)
    
    return jsonify(transaction), 201


@app.route('/transactions', methods=['GET'])
def get_transactions():
    """Get all transactions with optional filters"""
    filtered = transactions.copy()
    
    # Filter by accountId (either fromAccount or toAccount)
    account_id = request.args.get('accountId')
    if account_id:
        filtered = [t for t in filtered if t['fromAccount'] == account_id or t['toAccount'] == account_id]
    
    # Filter by type
    trans_type = request.args.get('type')
    if trans_type:
        filtered = [t for t in filtered if t['type'] == trans_type]
    
    # Filter by date range
    from_date = request.args.get('from')
    to_date = request.args.get('to')
    
    if from_date or to_date:
        try:
            from_dt = date_parser.parse(from_date) if from_date else datetime.min
            to_dt = date_parser.parse(to_date) if to_date else datetime.max
            
            filtered = [
                t for t in filtered
                if from_dt <= date_parser.parse(t['timestamp']) <= to_dt
            ]
        except Exception as e:
            return jsonify({
                "error": "Invalid date format",
                "message": "Use ISO 8601 format (e.g., 2024-01-01 or 2024-01-01T12:00:00Z)"
            }), 400
    
    return jsonify(filtered), 200


@app.route('/transactions/<transaction_id>', methods=['GET'])
def get_transaction(transaction_id):
    """Get a specific transaction by ID"""
    transaction = next((t for t in transactions if t['id'] == transaction_id), None)
    
    if not transaction:
        return jsonify({"error": "Transaction not found"}), 404
    
    return jsonify(transaction), 200


@app.route('/accounts/<account_id>/balance', methods=['GET'])
def get_account_balance(account_id):
    """Get account balance"""
    # Validate account format
    validation_errors = validate_account_format(account_id)
    if validation_errors:
        return jsonify({
            "error": "Invalid account ID",
            "details": validation_errors
        }), 400
    
    if account_id not in accounts:
        return jsonify({
            "accountId": account_id,
            "balance": 0.0,
            "currency": "USD"
        }), 200
    
    account = accounts[account_id]
    return jsonify({
        "accountId": account_id,
        "balance": account['balance'],
        "currency": account['currency']
    }), 200


@app.route('/accounts/<account_id>/summary', methods=['GET'])
def get_account_summary(account_id):
    """Get account transaction summary (Task 4: Option A)"""
    # Validate account format
    validation_errors = validate_account_format(account_id)
    if validation_errors:
        return jsonify({
            "error": "Invalid account ID",
            "details": validation_errors
        }), 400
    
    # Filter transactions for this account
    account_transactions = [
        t for t in transactions 
        if t['fromAccount'] == account_id or t['toAccount'] == account_id
    ]
    
    # Calculate summary
    total_deposits = 0.0
    total_withdrawals = 0.0
    most_recent = None
    
    for trans in account_transactions:
        if trans['type'] == 'deposit' and trans['toAccount'] == account_id:
            total_deposits += trans['amount']
        elif trans['type'] == 'withdrawal' and trans['fromAccount'] == account_id:
            total_withdrawals += trans['amount']
        elif trans['type'] == 'transfer':
            if trans['toAccount'] == account_id:
                total_deposits += trans['amount']
            elif trans['fromAccount'] == account_id:
                total_withdrawals += trans['amount']
        
        # Track most recent transaction
        trans_time = date_parser.parse(trans['timestamp'])
        if most_recent is None or trans_time > most_recent:
            most_recent = trans_time
    
    # Get current balance
    balance = 0.0
    currency = "USD"
    if account_id in accounts:
        balance = accounts[account_id]['balance']
        currency = accounts[account_id]['currency']
    
    return jsonify({
        "accountId": account_id,
        "balance": balance,
        "currency": currency,
        "totalDeposits": total_deposits,
        "totalWithdrawals": total_withdrawals,
        "numberOfTransactions": len(account_transactions),
        "mostRecentTransactionDate": most_recent.isoformat() + 'Z' if most_recent else None
    }), 200


# ==================== HELPER FUNCTIONS ====================

def update_account_balances(transaction):
    """Update account balances based on transaction"""
    currency = transaction['currency']
    amount = transaction['amount']
    from_account = transaction['fromAccount']
    to_account = transaction['toAccount']
    trans_type = transaction['type']
    
    # Initialize accounts if not exists
    if from_account not in accounts:
        accounts[from_account] = {'balance': 0.0, 'currency': currency}
    if to_account not in accounts:
        accounts[to_account] = {'balance': 0.0, 'currency': currency}
    
    # Update balances based on transaction type
    if trans_type == 'deposit':
        accounts[to_account]['balance'] += amount
    elif trans_type == 'withdrawal':
        accounts[from_account]['balance'] -= amount
    elif trans_type == 'transfer':
        accounts[from_account]['balance'] -= amount
        accounts[to_account]['balance'] += amount


# ==================== ERROR HANDLERS ====================

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({"error": "Endpoint not found"}), 404


@app.errorhandler(500)
def server_error(error):
    """Handle 500 errors"""
    return jsonify({"error": "Internal server error"}), 500


# ==================== HEALTH CHECK ====================

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "ok"}), 200


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
