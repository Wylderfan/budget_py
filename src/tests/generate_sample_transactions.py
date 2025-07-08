#!/usr/bin/env python3
"""
Random Transaction Generator

This script generates realistic random transactions for testing the budget application.
It uses predefined data from sample_data.json to create varied, realistic transactions.
"""

import json
import random
import os
import sys
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
from dotenv import load_dotenv

# Add the src directory to the path so we can import our modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database_connector import DatabaseConnector
from controllers.db.categories_db_service import CategoriesDBService
from controllers.db.account_db_service import AccountDBService
from controllers.db.transaction_db_service import TransactionDBService


class TransactionGenerator:
    def __init__(self, db_config: Dict[str, str]):
        """Initialize the transaction generator with database configuration."""
        self.db = DatabaseConnector(**db_config)
        self.categories_service = CategoriesDBService(self.db)
        self.accounts_service = AccountDBService(self.db)
        self.transactions_service = TransactionDBService(self.db)
        
        # Load sample data
        self.sample_data = self._load_sample_data()
        
        # Store database IDs for categories and accounts
        self.category_ids = {}
        self.account_ids = {}
        
        # Initialize database with sample categories and accounts
        self._setup_database()

    def _load_sample_data(self) -> Dict:
        """Load sample data from JSON file."""
        try:
            json_path = os.path.join(os.path.dirname(__file__), 'sample_data.json')
            with open(json_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print("Error: sample_data.json not found. Please ensure it exists in the src/tests directory.")
            sys.exit(1)
        except json.JSONDecodeError:
            print("Error: Invalid JSON in sample_data.json")
            sys.exit(1)

    def _setup_database(self):
        """Ensure all required categories and accounts exist in the database."""
        print("Setting up database with sample categories and accounts...")
        
        # Create categories if they don't exist
        try:
            existing_categories = self.categories_service.search_all()
            existing_category_names = []
            if existing_categories and isinstance(existing_categories, list):
                existing_category_names = [cat[1] for cat in existing_categories]
            
            for category_name, category_data in self.sample_data['categories'].items():
                if category_name not in existing_category_names:
                    print(f"Creating category: {category_name}")
                    self.categories_service.add_category(category_name, category_data['type'])
                
                # Get category ID
                category_record = self.categories_service.search_categories(name=category_name)
                if category_record and isinstance(category_record, list) and len(category_record) > 0:
                    self.category_ids[category_name] = category_record[0][0]
                    
        except Exception as e:
            print(f"Error setting up categories: {e}")
            return
        
        # Create accounts if they don't exist
        try:
            existing_accounts = self.accounts_service.search_all()
            existing_account_names = []
            if existing_accounts and isinstance(existing_accounts, list):
                existing_account_names = [acc[1] for acc in existing_accounts]
            
            for account_data in self.sample_data['accounts']:
                if account_data['name'] not in existing_account_names:
                    print(f"Creating account: {account_data['name']}")
                    self.accounts_service.add_account(
                        account_data['name'], 
                        account_data['balance'], 
                        account_data['type']
                    )
                
                # Get account ID
                account_record = self.accounts_service.search_account(name=account_data['name'])
                if account_record and isinstance(account_record, list) and len(account_record) > 0:
                    self.account_ids[account_data['name']] = account_record[0][0]
                    
        except Exception as e:
            print(f"Error setting up accounts: {e}")
            return
        
        print(f"Database setup complete. Categories: {len(self.category_ids)}, Accounts: {len(self.account_ids)}")

    def _generate_random_date(self, days_back: int = 365) -> datetime:
        """Generate a random date within the specified number of days back."""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days_back)
        
        # Generate random date
        time_between = end_date - start_date
        random_days = random.randrange(time_between.days)
        random_date = start_date + timedelta(days=random_days)
        
        return random_date

    def _generate_random_amount(self, category_name: str) -> float:
        """Generate a realistic random amount for the given category."""
        category_data = self.sample_data['categories'][category_name]
        
        # 70% chance to use a common amount, 30% chance to use random amount in range
        if random.random() < 0.7 and category_data['common_amounts']:
            amount = random.choice(category_data['common_amounts'])
        else:
            min_amount, max_amount = category_data['amount_range']
            amount = round(random.uniform(min_amount, max_amount), 2)
        
        return amount

    def _get_random_note(self) -> str:
        """Get a random note from the templates."""
        return random.choice(self.sample_data['notes_templates'])

    def _get_weighted_category(self, expense_only: bool = False) -> str:
        """Get a weighted random category based on typical spending patterns."""
        categories = list(self.sample_data['categories'].keys())
        
        if expense_only:
            categories = [cat for cat in categories if self.sample_data['categories'][cat]['type'] == 'Expense']
        
        # Weight categories based on typical frequency
        weights = []
        for category in categories:
            if category == 'Food':
                weights.append(30)  # Most frequent
            elif category == 'Transportation':
                weights.append(25)  # Very frequent
            elif category == 'Bills':
                weights.append(15)  # Regular but less frequent
            elif category == 'Shopping':
                weights.append(12)  # Regular
            elif category == 'Entertainment':
                weights.append(10)  # Moderate
            elif category == 'Health':
                weights.append(5)   # Less frequent
            elif category == 'Income':
                weights.append(8)   # Regular but less than expenses
            else:
                weights.append(5)   # Default weight
        
        return random.choices(categories, weights=weights)[0]

    def _get_random_account(self, transaction_type: str) -> str:
        """Get a random account based on transaction type."""
        account_names = list(self.account_ids.keys())
        
        # Weight accounts based on transaction type and typical usage
        if transaction_type == 'Income':
            # Income usually goes to checking or savings
            checking_savings = [name for name in account_names if 'checking' in name.lower() or 'savings' in name.lower()]
            return random.choice(checking_savings if checking_savings else account_names)
        else:
            # Expenses can come from any account, but credit cards for larger purchases
            if random.random() < 0.3:  # 30% chance to use credit card
                credit_cards = [name for name in account_names if 'credit' in name.lower() or 'card' in name.lower()]
                if credit_cards:
                    return random.choice(credit_cards)
            
            # Otherwise use checking or savings
            checking_savings = [name for name in account_names if 'checking' in name.lower() or 'savings' in name.lower()]
            return random.choice(checking_savings if checking_savings else account_names)

    def generate_transactions(self, num_transactions: int = 100, days_back: int = 365) -> List[Dict]:
        """Generate a specified number of random transactions."""
        print(f"Generating {num_transactions} random transactions over the last {days_back} days...")
        
        transactions = []
        
        for i in range(num_transactions):
            # Generate basic transaction data
            category_name = self._get_weighted_category()
            category_data = self.sample_data['categories'][category_name]
            transaction_type = category_data['type']
            
            # Generate transaction details
            date = self._generate_random_date(days_back)
            description = random.choice(category_data['descriptions'])
            amount = self._generate_random_amount(category_name)
            notes = self._get_random_note()
            account_name = self._get_random_account(transaction_type)
            
            # Get database IDs
            category_id = self.category_ids.get(category_name)
            account_id = self.account_ids.get(account_name)
            
            if category_id is None or account_id is None:
                print(f"Warning: Skipping transaction due to missing category or account ID")
                continue
            
            transaction = {
                'date': date.date(),
                'description': description,
                'amount': amount,
                'category_id': category_id,
                'category_name': category_name,
                'transaction_type': transaction_type,
                'account_id': account_id,
                'account_name': account_name,
                'notes': notes
            }
            
            transactions.append(transaction)
            
            # Progress indicator
            if (i + 1) % 20 == 0:
                print(f"Generated {i + 1}/{num_transactions} transactions...")
        
        return transactions

    def save_transactions_to_database(self, transactions: List[Dict]):
        """Save generated transactions to the database."""
        print(f"Saving {len(transactions)} transactions to database...")
        
        successful = 0
        failed = 0
        
        for transaction in transactions:
            try:
                result = self.transactions_service.add_transaction(
                    date=transaction['date'],
                    description=transaction['description'],
                    amount=transaction['amount'],
                    category_id=transaction['category_id'],
                    transaction_type=transaction['transaction_type'],
                    account_id=transaction['account_id'],
                    notes=transaction['notes']
                )
                
                if result == 1:
                    successful += 1
                else:
                    failed += 1
                    print(f"Failed to save transaction: {transaction['description']}")
                    
            except Exception as e:
                failed += 1
                print(f"Error saving transaction: {e}")
        
        print(f"Transaction generation complete!")
        print(f"Successfully saved: {successful}")
        print(f"Failed to save: {failed}")
        
        return successful, failed

    def print_transaction_summary(self, transactions: List[Dict]):
        """Print a summary of the generated transactions."""
        if not transactions:
            print("No transactions to summarize.")
            return
        
        print("\n" + "="*50)
        print("TRANSACTION SUMMARY")
        print("="*50)
        
        # Summary by category
        category_totals = {}
        for trans in transactions:
            cat = trans['category_name']
            if cat not in category_totals:
                category_totals[cat] = {'count': 0, 'total': 0.0}
            category_totals[cat]['count'] += 1
            category_totals[cat]['total'] += trans['amount']
        
        print("\nBy Category:")
        for category, data in sorted(category_totals.items()):
            avg_amount = data['total'] / data['count']
            print(f"  {category}: {data['count']} transactions, ${data['total']:.2f} total, ${avg_amount:.2f} avg")
        
        # Summary by account
        account_totals = {}
        for trans in transactions:
            acc = trans['account_name']
            if acc not in account_totals:
                account_totals[acc] = {'count': 0, 'total': 0.0}
            account_totals[acc]['count'] += 1
            account_totals[acc]['total'] += trans['amount']
        
        print("\nBy Account:")
        for account, data in sorted(account_totals.items()):
            print(f"  {account}: {data['count']} transactions, ${data['total']:.2f} total")
        
        # Date range
        dates = [trans['date'] for trans in transactions]
        print(f"\nDate Range: {min(dates)} to {max(dates)}")
        
        # Total amounts
        total_income = sum(trans['amount'] for trans in transactions if trans['transaction_type'] == 'Income')
        total_expenses = sum(trans['amount'] for trans in transactions if trans['transaction_type'] == 'Expense')
        
        print(f"\nTotals:")
        print(f"  Income: ${total_income:.2f}")
        print(f"  Expenses: ${total_expenses:.2f}")
        print(f"  Net: ${total_income - total_expenses:.2f}")


def main():
    """Main function to run the transaction generator."""
    print("Random Transaction Generator")
    print("=" * 50)
    
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
        print("❌ Error: Missing required environment variables in .env file:")
        for var in missing_vars:
            env_var = f"DB_{var.upper()}" if var != 'database' else 'DB_NAME'
            print(f"  - {env_var}")
        print("\nPlease ensure your .env file contains:")
        print("  DB_HOST=localhost")
        print("  DB_USER=your_username")
        print("  DB_PASSWORD=your_password") 
        print("  DB_NAME=budget_db")
        return
    
    # Get user input
    try:
        num_transactions = int(input("How many transactions to generate? (default: 100): ") or "100")
        days_back = int(input("Generate transactions over how many days back? (default: 365): ") or "365")
    except ValueError:
        print("Invalid input. Using defaults.")
        num_transactions = 100
        days_back = 365
    
    # Create generator and generate transactions
    try:
        generator = TransactionGenerator(db_config)
        transactions = generator.generate_transactions(num_transactions, days_back)
        
        # Show preview
        generator.print_transaction_summary(transactions)
        
        # Ask for confirmation
        response = input("\nSave these transactions to the database? (y/N): ").lower()
        if response == 'y' or response == 'yes':
            generator.save_transactions_to_database(transactions)
        else:
            print("Transactions not saved.")
    
    except Exception as e:
        print(f"Error: {e}")
        print("\nPlease check:")
        print("1. Your .env file contains correct database credentials")
        print("2. Database is running")
        print("3. Database and tables exist")
        print("4. User has proper permissions")


if __name__ == "__main__":
    main() 