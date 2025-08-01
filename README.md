# Budget Application

A Python-based budget tracking application built with PyQt6 and MySQL.

## Features
- Track income and expenses
- Categorize transactions
- View budget summaries

## Setup

### Prerequisites
- Python 3.8 or higher
- MySQL Server (local or remote)
- Git (for cloning the repository)

### Installation Steps

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd budget_py
   ```

2. **Create and activate a virtual environment**
   ```bash
   # Create virtual environment
   python -m venv venv
   
   # Activate virtual environment
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up MySQL database**
   - Install MySQL Server if not already installed
   - Create a new database named `budget_db` (or your preferred name)
   - Create a MySQL user with appropriate permissions

5. **Configure environment variables**
   Create a `.env` file in the project root with your database credentials:
   ```
   DB_HOST=localhost
   DB_USER=your_username
   DB_PASSWORD=your_password
   DB_NAME=budget_db
   ```

6. **Initialize the database**
   The application will automatically create the necessary tables on first run.

### Building Executable (Optional)
To create a standalone executable:
```bash
pyinstaller --onefile --windowed --add-data "../.env:." --add-data "config/account_types.json:config" --name "BudgetApp" main.py
```
## Running the Application without building

Make sure your virtual environment is activated, then run:
```bash
python src/main.py
```

## Development and Testing

### Running Tests
```bash
# Run all tests from src/ directory
cd src
python -m pytest tests/
```

### Generate Sample Data
For testing purposes, you can generate sample transactions:
```bash
cd src/tests
python run_transaction_generator.py
# OR for interactive mode:
python generate_sample_transactions.py
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
