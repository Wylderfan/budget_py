# Budget Application

A Python-based budget tracking application built with PyQt6 and MySQL.

## Features
- Track income and expenses
- Categorize transactions
- View budget summaries
- Monthly/yearly reports

## Setup
1. Install Python 3.8 or higher
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up your MySQL database
4. Create a `.env` file with your database credentials:
   ```
   DB_HOST=localhost
   DB_USER=your_username
   DB_PASSWORD=your_password
   DB_NAME=budget_db
   ```

## Running the Application
```bash
python src/main.py
```

## Project Structure
- `src/` - Main application code
  - `models/` - Database models
  - `views/` - PyQt UI components
  - `controllers/` - Business logic
- `database_connector.py` - Database connection handler 

## Database Structure
- budget_table
  - transactions
    - id
    - date
    - description
    - notes
    - amount
    - category
    - type
  - accounts
    - id
    - name
    - date_created
    - balance
    - type
    - is_credit (bool)
  - categories
    - id
    - date_created
    - name
    - type