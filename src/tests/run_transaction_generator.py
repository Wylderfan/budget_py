#!/usr/bin/env python3
"""
Simple script to run the transaction generator with your specific database configuration.
Edit the database configuration below to match your setup.
"""

import os
import sys
from dotenv import load_dotenv

# Import the transaction generator from the same directory
from generate_sample_transactions import TransactionGenerator


def main():
    """Run the transaction generator with your database configuration."""
    
    # Load environment variables from .env file
    load_dotenv()
    
    # Database configuration from environment variables
    db_config = {
        'host': os.getenv('DB_HOST', 'localhost'),
        'user': os.getenv('DB_USER'),
        'password': os.getenv('DB_PASSWORD'),
        'database': os.getenv('DB_NAME')
    }
    
    # Check if all required environment variables are set
    missing_vars = [key for key, value in db_config.items() if value is None]
    if missing_vars:
        print("Error: Missing required environment variables in .env file:")
        for var in missing_vars:
            env_var = f"DB_{var.upper()}" if var != 'database' else 'DB_NAME'
            print(f"  - {env_var}")
        print("\nPlease ensure your .env file contains:")
        print("  DB_HOST=localhost")
        print("  DB_USER=your_username")
        print("  DB_PASSWORD=your_password") 
        print("  DB_NAME=budget_db")
        return
    
    print("Budget App - Transaction Generator")
    print("=" * 50)
    print("This script will generate realistic random transactions for testing.")
    print()
    
    # Configuration options
    num_transactions = 50  # Change this to generate more or fewer transactions
    days_back = 180  # Generate transactions over the last 6 months
    
    print(f"Configuration:")
    print(f"  - Transactions to generate: {num_transactions}")
    print(f"  - Date range: Last {days_back} days")
    print(f"  - Database: {db_config['database']} on {db_config['host']}")
    print()
    
    try:
        # Create and run the generator
        generator = TransactionGenerator(db_config)
        
        # Generate transactions
        transactions = generator.generate_transactions(num_transactions, days_back)
        
        # Show summary
        generator.print_transaction_summary(transactions)
        
        # Save to database
        print("\nSaving transactions to database...")
        successful, failed = generator.save_transactions_to_database(transactions)
        
        print(f"\n✅ Complete! Generated {successful} transactions successfully.")
        if failed > 0:
            print(f"⚠️  {failed} transactions failed to save.")
        
    except Exception as e:
        print(f"Error: {e}")
        print("\nPlease check:")
        print("1. Your .env file contains correct database credentials")
        print("2. Database is running")
        print("3. Database and tables exist")
        print("4. User has proper permissions")


if __name__ == "__main__":
    main() 