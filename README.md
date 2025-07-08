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
    - id INT (PK, NN, AI)
    - date DATE (NN)
    - description VARCHAR(255) (NN)
    - amount Decimal(10.2) (NN)
    - category INT (NN)
    - type VARCHAR(10) (NN)
    - notes VARCHAR(1000)
    - account INT (NN)
  - accounts
    - id INT (PK, NN, AI)
    - name VARCHAR(45) (NN)
    - date_created DATE
    - balance DECIMAL(10.2) (NN)
    - type VARCHAR(45) (NN)
    - is_credit TINYINT (NN)
  - categories
    - id INT (PK, NN, AI)
    - name VARCHAR(45) (NN)
    - date_created DATE
    - type VARCHAR(45) (NN)
