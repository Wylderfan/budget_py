# Random Transaction Generator

This collection of scripts generates realistic random transactions for testing your budget tracking application.

## Files Included

1. **`src/tests/sample_data.json`** - Contains realistic transaction data organized by categories
2. **`src/tests/generate_sample_transactions.py`** - Main transaction generator class and interactive script
3. **`src/tests/run_transaction_generator.py`** - Simple script with predefined configuration

## Features

- **Realistic Data**: Generates transactions with realistic descriptions, amounts, and patterns
- **Weighted Randomness**: More frequent categories (like Food) appear more often than others
- **Smart Account Selection**: Income goes to checking/savings, expenses can use credit cards
- **Date Distribution**: Spreads transactions realistically over the specified time period
- **Database Integration**: Automatically creates missing categories and accounts
- **Progress Tracking**: Shows progress and provides detailed summaries

## Sample Data Categories

The generator includes these categories with realistic transaction patterns:

- **Food** (30% frequency): Groceries, restaurants, coffee shops, etc.
- **Transportation** (25% frequency): Gas, Uber, parking, maintenance, etc.
- **Bills** (15% frequency): Utilities, insurance, rent, subscriptions, etc.
- **Shopping** (12% frequency): Amazon, clothing, electronics, etc.
- **Entertainment** (10% frequency): Movies, concerts, games, streaming, etc.
- **Health** (5% frequency): Doctor visits, prescriptions, therapy, etc.
- **Income** (8% frequency): Salary, freelance, dividends, bonuses, etc.

## Quick Start

### Option 1: Use the Simple Script

1. Ensure your `.env` file contains your database configuration:
   ```
   DB_HOST=localhost
   DB_USER=your_username
   DB_PASSWORD=your_password
   DB_NAME=budget_db
   ```

2. Optionally adjust the generation settings in `src/tests/run_transaction_generator.py`:
   ```python
   num_transactions = 50  # How many transactions to generate
   days_back = 180  # Generate over last 6 months
   ```

3. Run the script:
   ```bash
   cd src/tests
   python run_transaction_generator.py
   ```

### Option 2: Use the Interactive Script

1. Run the interactive generator:
   ```bash
   cd src/tests
   python generate_sample_transactions.py
   ```

2. Ensure your `.env` file is properly configured (same as Option 1)

3. Follow the prompts to enter:
   - Number of transactions to generate
   - Time period (days back from today)

4. Review the generated transaction summary

5. Confirm to save to database

## What the Scripts Do

1. **Setup Database**: Automatically creates categories and accounts from `sample_data.json` if they don't exist
2. **Generate Transactions**: Creates random transactions with realistic patterns:
   - Weighted category selection (Food and Transportation are most common)
   - Realistic amounts based on category (Bills are larger, Coffee is smaller)
   - Smart account selection (Income goes to checking, some expenses use credit cards)
   - Random dates distributed over the specified period
   - Realistic descriptions matching each category
3. **Save to Database**: Uses your existing database services to insert transactions
4. **Provide Summary**: Shows breakdown by category, account, and totals

## Sample Output

```
Budget App - Transaction Generator
==================================================
Setting up database with sample categories and accounts...
Creating category: Food
Creating category: Transportation
Creating account: Main Checking
Creating account: Credit Card
Database setup complete. Categories: 7, Accounts: 5

Generating 50 random transactions over the last 180 days...
Generated 20/50 transactions...
Generated 40/50 transactions...

==================================================
TRANSACTION SUMMARY
==================================================

By Category:
  Entertainment: 4 transactions, $156.48 total, $39.12 avg
  Food: 18 transactions, $567.23 total, $31.51 avg
  Health: 2 transactions, $187.50 total, $93.75 avg
  Income: 3 transactions, $4250.00 total, $1416.67 avg
  Shopping: 5 transactions, $289.47 total, $57.89 avg
  Transportation: 15 transactions, $743.75 total, $49.58 avg
  Bills: 3 transactions, $845.50 total, $281.83 avg

By Account:
  Credit Card: 12 transactions, $456.78 total
  Main Checking: 32 transactions, $5234.56 total
  Savings Account: 6 transactions, $1348.59 total

Date Range: 2024-06-15 to 2024-12-12

Totals:
  Income: $4250.00
  Expenses: $2789.93
  Net: $1460.07

✅ Complete! Generated 50 transactions successfully.
```

## Customization

### Adding New Categories

Edit `sample_data.json` to add new categories:

```json
"NewCategory": {
  "type": "Expense",
  "descriptions": [
    "Custom description 1",
    "Custom description 2"
  ],
  "amount_range": [10.00, 200.00],
  "common_amounts": [25.00, 50.00, 75.00]
}
```

### Adjusting Frequency

Modify the weights in `_get_weighted_category()` method in `generate_sample_transactions.py`:

```python
if category == 'YourCategory':
    weights.append(40)  # Higher number = more frequent
```

### Changing Amount Patterns

Edit the `amount_range` and `common_amounts` in `sample_data.json` for each category.

## Requirements

- Python 3.6+
- `python-dotenv` package for loading .env files
- MySQL database with your budget app schema
- Existing database services (categories_db_service, account_db_service, transaction_db_service)
- `.env` file with database configuration

## Troubleshooting

- **"Module not found"**: Make sure you're running from the `src/tests` directory
- **"Missing required environment variables"**: Ensure your `.env` file contains all required database variables (DB_HOST, DB_USER, DB_PASSWORD, DB_NAME)
- **"Database connection failed"**: Check your `.env` file configuration and ensure MySQL is running
- **"Permission denied"**: Ensure your database user has INSERT permissions
- **"Categories/Accounts not created"**: Check database connection and permissions

## Notes

- The script will not duplicate categories or accounts that already exist
- Generated transactions are completely random and for testing purposes only
- The script respects your existing database schema and uses proper foreign key relationships
- All amounts are in the currency format expected by your application (typically USD with 2 decimal places) 