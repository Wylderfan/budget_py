import unittest
from unittest.mock import Mock, patch
import sys
import os
from datetime import datetime, date

# Add the parent directory to the path so we can import the service
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from controllers.db.transaction_db_service import TransactionDBService


class TestTransactionDBService(unittest.TestCase):
    """Test basic CRUD operations for transactions."""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        # Create a mock database connector
        self.mock_db = Mock()
        self.service = TransactionDBService(self.mock_db)
    
    def test_add_transaction_basic(self):
        """Test adding a basic transaction."""
        # Setup mock
        self.mock_db.execute_query.return_value = 1
        
        # Test data
        transaction_date = "2024-01-15"
        description = "Grocery shopping"
        amount = 85.50
        category_id = 1
        transaction_type = "Expense"
        account_id = 1
        notes = "Weekly groceries"
        
        # Call method
        result = self.service.add_transaction(
            transaction_date, description, amount, category_id, 
            transaction_type, account_id, notes
        )
        
        # Verify database interactions
        self.mock_db.connect.assert_called_once()
        self.mock_db.close.assert_called_once()
        self.assertEqual(result, 1)
        
        # Verify the query was called correctly
        self.mock_db.execute_query.assert_called_once()
        call_args = self.mock_db.execute_query.call_args
        
        # Check the query structure
        query = call_args[0][0]
        params = call_args[0][1]
        
        self.assertIn("INSERT INTO transactions", query)
        self.assertIn("date, description, amount, category, type, account, notes", query)
        
        # Check parameters
        self.assertEqual(params[0], transaction_date)
        self.assertEqual(params[1], description)
        self.assertEqual(params[2], amount)
        self.assertEqual(params[3], category_id)
        self.assertEqual(params[4], transaction_type)
        self.assertEqual(params[5], account_id)
        self.assertEqual(params[6], notes)
    
    def test_add_transaction_without_notes(self):
        """Test adding transaction without notes (default empty string)."""
        # Setup mock
        self.mock_db.execute_query.return_value = 1
        
        # Call method without notes
        result = self.service.add_transaction(
            "2024-01-15", "Test transaction", 100.00, 1, "Expense", 1
        )
        
        # Verify default notes parameter
        call_args = self.mock_db.execute_query.call_args
        params = call_args[0][1]
        self.assertEqual(params[6], "")  # notes should be empty string
    
    def test_add_transaction_with_negative_amount(self):
        """Test adding transaction with negative amount (refund)."""
        # Setup mock
        self.mock_db.execute_query.return_value = 1
        
        # Call method with negative amount
        result = self.service.add_transaction(
            "2024-01-15", "Refund", -50.00, 1, "Income", 1, "Store refund"
        )
        
        # Verify negative amount is passed correctly
        call_args = self.mock_db.execute_query.call_args
        params = call_args[0][1]
        self.assertEqual(params[2], -50.00)
    
    @patch('builtins.print')
    def test_add_transaction_success_message(self, mock_print):
        """Test success message when transaction is added."""
        # Setup mock to return successful insert
        self.mock_db.execute_query.return_value = 1
        
        self.service.add_transaction("2024-01-15", "Test", 100.00, 1, "Expense", 1)
        
        # Verify success message was printed
        mock_print.assert_called_with("Transaction has been successfully added")
    
    @patch('builtins.print')
    def test_add_transaction_error_message(self, mock_print):
        """Test error message when transaction insert fails."""
        # Setup mock to return failed insert
        self.mock_db.execute_query.return_value = 0
        
        self.service.add_transaction("2024-01-15", "Test", 100.00, 1, "Expense", 1)
        
        # Verify error message was printed
        mock_print.assert_called_with("Error with insert query")


class TestTransactionTransferMethods(unittest.TestCase):
    """Test transaction transfer functionality."""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.mock_db = Mock()
        self.service = TransactionDBService(self.mock_db)
    
    def test_add_transfer_basic(self):
        """Test adding a basic transfer transaction."""
        # Setup mock for account lookups and insert
        # Mock the account search calls to return account names
        self.service.account_db_service.search_account = Mock()
        self.service.account_db_service.search_account.side_effect = [
            [(1, "Checking Account", 1000.00, "Chequing", False)],  # from_account
            [(2, "Savings Account", 2000.00, "Savings", False)]     # to_account
        ]
        self.mock_db.execute_query.return_value = 1
        
        # Test data
        transfer_date = "2024-01-15"
        amount = 500.00
        from_account = 1
        to_account = 2
        notes = "Monthly savings transfer"
        
        # Call method
        result = self.service.add_transfer(transfer_date, amount, from_account, to_account, notes)
        
        # Verify database interactions
        self.mock_db.connect.assert_called_once()
        self.mock_db.close.assert_called_once()
        self.assertEqual(result, 1)
        
        # Verify account searches were called
        self.service.account_db_service.search_account.assert_any_call(id=from_account)
        self.service.account_db_service.search_account.assert_any_call(id=to_account)
        
        # Verify the query was called correctly
        call_args = self.mock_db.execute_query.call_args
        query = call_args[0][0]
        params = call_args[0][1]
        
        self.assertIn("INSERT INTO transactions", query)
        self.assertIn("date, description, amount, type, account, notes", query)
        
        # Check parameters
        self.assertEqual(params[0], transfer_date)
        self.assertEqual(params[1], "Transfer from Checking Account to Savings Account")
        self.assertEqual(params[2], amount)
        self.assertEqual(params[3], "Transfer")
        self.assertEqual(params[4], to_account)  # Transfer goes to the destination account
        self.assertEqual(params[5], notes)
    
    def test_add_transfer_description_format(self):
        """Test that transfer description is formatted correctly."""
        # Setup mock
        self.service.account_db_service.search_account = Mock()
        self.service.account_db_service.search_account.side_effect = [
            [(1, "Main Checking", 1500.00, "Chequing", False)],
            [(3, "Credit Card", -200.00, "Credit Card", True)]
        ]
        self.mock_db.execute_query.return_value = 1
        
        # Call method
        result = self.service.add_transfer("2024-01-15", 300.00, 1, 3, "Payment")
        
        # Verify description format
        call_args = self.mock_db.execute_query.call_args
        params = call_args[0][1]
        
        expected_description = "Transfer from Main Checking to Credit Card"
        self.assertEqual(params[1], expected_description)
    
    def test_add_transfer_zero_amount(self):
        """Test transfer with zero amount (edge case)."""
        # Setup mock
        self.service.account_db_service.search_account = Mock()
        self.service.account_db_service.search_account.side_effect = [
            [(1, "Account A", 1000.00, "Chequing", False)],
            [(2, "Account B", 2000.00, "Savings", False)]
        ]
        self.mock_db.execute_query.return_value = 1
        
        # Call method with zero amount
        result = self.service.add_transfer("2024-01-15", 0.00, 1, 2, "Test zero transfer")
        
        # Verify amount is passed correctly
        call_args = self.mock_db.execute_query.call_args
        params = call_args[0][1]
        self.assertEqual(params[2], 0.00)
    
    def test_add_transfer_large_amount(self):
        """Test transfer with large amount."""
        # Setup mock
        self.service.account_db_service.search_account = Mock()
        self.service.account_db_service.search_account.side_effect = [
            [(1, "Business Checking", 50000.00, "Chequing", False)],
            [(2, "Investment Account", 100000.00, "Savings", False)]
        ]
        self.mock_db.execute_query.return_value = 1
        
        # Call method with large amount
        large_amount = 25000.00
        result = self.service.add_transfer("2024-01-15", large_amount, 1, 2, "Investment transfer")
        
        # Verify amount is passed correctly
        call_args = self.mock_db.execute_query.call_args
        params = call_args[0][1]
        self.assertEqual(params[2], large_amount)


class TestTransactionSearchMethods(unittest.TestCase):
    """Test transaction search and retrieval methods."""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.mock_db = Mock()
        self.service = TransactionDBService(self.mock_db)
    
    def test_search_transaction_by_id(self):
        """Test searching transaction by ID."""
        # Setup mock
        expected_transaction = [(1, "2024-01-15", "Test transaction", 100.00, 1, "Expense", 1, "Notes")]
        self.mock_db.execute_query.return_value = expected_transaction
        
        # Call method
        result = self.service.search_transaction(id=1)
        
        # Verify database interactions
        self.mock_db.connect.assert_called_once()
        self.mock_db.close.assert_called_once()
        self.assertEqual(result, expected_transaction)
        
        # Verify correct query was used
        call_args = self.mock_db.execute_query.call_args
        query = call_args[0][0]
        params = call_args[0][1]
        
        self.assertIn("SELECT * FROM transactions WHERE id = %s", query)
        self.assertEqual(params[0], 1)
    
    def test_search_transaction_by_description(self):
        """Test searching transaction by description."""
        # Setup mock
        expected_transaction = [(1, "2024-01-15", "Grocery shopping", 85.50, 1, "Expense", 1, "")]
        self.mock_db.execute_query.return_value = expected_transaction
        
        # Call method
        result = self.service.search_transaction(description="Grocery shopping")
        
        # Verify correct query and parameters
        call_args = self.mock_db.execute_query.call_args
        query = call_args[0][0]
        params = call_args[0][1]
        
        self.assertIn("SELECT * FROM transactions WHERE description = %s", query)
        self.assertEqual(params[0], "Grocery shopping")
    
    @patch('builtins.print')
    def test_search_transaction_no_parameters(self, mock_print):
        """Test search transaction with no parameters (should print error)."""
        # Call method without parameters
        result = self.service.search_transaction()
        
        # Verify error message was printed
        mock_print.assert_called_with("Must use arg id or description")
        
        # Verify database was connected but method returned early
        self.mock_db.connect.assert_called_once()
        self.mock_db.execute_query.assert_not_called()  # Should not execute query
        self.assertIsNone(result)
    
    def test_search_all_transactions(self):
        """Test searching all transactions with joins."""
        # Setup mock
        expected_transactions = [
            ("2024-01-15", "Grocery shopping", 85.50, "Food", "Checking", "Expense"),
            ("2024-01-14", "Gas", 45.00, "Transportation", "Credit Card", "Expense")
        ]
        self.mock_db.execute_query.return_value = expected_transactions
        
        # Call method
        result = self.service.search_all()
        
        # Verify database interactions
        self.mock_db.connect.assert_called_once()
        self.mock_db.close.assert_called_once()
        self.assertEqual(result, expected_transactions)
        
        # Verify query structure includes joins
        call_args = self.mock_db.execute_query.call_args
        query = call_args[0][0]
        
        self.assertIn("LEFT JOIN categories c ON t.category = c.id", query)
        self.assertIn("LEFT JOIN accounts a ON t.account = a.id", query)
        self.assertIn("ORDER BY t.date DESC", query)
    
    def test_search_by_date_range(self):
        """Test searching transactions by date range."""
        # Setup mock
        expected_transactions = [("2024-01-15", "Transaction 1", 100.00, "Category", "Account", "Expense")]
        self.mock_db.execute_query.return_value = expected_transactions
        
        # Call method
        start_date = "2024-01-01"
        end_date = "2024-01-31"
        result = self.service.search_by_date_range(start_date, end_date)
        
        # Verify parameters
        call_args = self.mock_db.execute_query.call_args
        params = call_args[0][1]
        
        self.assertEqual(params[0], start_date)
        self.assertEqual(params[1], end_date)
    
    def test_search_by_category(self):
        """Test searching transactions by category."""
        # Setup mock
        expected_transactions = [("2024-01-15", "Food purchase", 50.00, "Food", "Checking", "Expense")]
        self.mock_db.execute_query.return_value = expected_transactions
        
        # Call method
        category_id = 2
        result = self.service.search_by_category(category_id)
        
        # Verify parameters
        call_args = self.mock_db.execute_query.call_args
        params = call_args[0][1]
        
        self.assertEqual(params[0], category_id)
    
    def test_search_by_account(self):
        """Test searching transactions by account."""
        # Setup mock
        expected_transactions = [("2024-01-15", "Transaction", 100.00, "Category", "Checking", "Expense")]
        self.mock_db.execute_query.return_value = expected_transactions
        
        # Call method
        account_id = 1
        result = self.service.search_by_account(account_id)
        
        # Verify parameters
        call_args = self.mock_db.execute_query.call_args
        params = call_args[0][1]
        
        self.assertEqual(params[0], account_id)


class TestTransactionDeletionMethods(unittest.TestCase):
    """Test transaction deletion functionality."""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.mock_db = Mock()
        self.service = TransactionDBService(self.mock_db)
    
    def test_del_transaction(self):
        """Test deleting a single transaction."""
        # Setup mock
        self.mock_db.execute_query.return_value = 1
        
        # Call method
        transaction_id = 5
        result = self.service.del_transaction(transaction_id)
        
        # Verify database interactions
        self.mock_db.connect.assert_called_once()
        self.mock_db.close.assert_called_once()
        self.assertEqual(result, 1)
        
        # Verify correct query and parameters
        call_args = self.mock_db.execute_query.call_args
        query = call_args[0][0]
        params = call_args[0][1]
        
        self.assertIn("DELETE FROM transactions WHERE id = %s", query)
        self.assertEqual(params[0], transaction_id)
    
    @patch('builtins.print')
    def test_del_transaction_success_message(self, mock_print):
        """Test success message when transaction is deleted."""
        # Setup mock to return successful deletion
        self.mock_db.execute_query.return_value = 1
        
        transaction_id = 5
        self.service.del_transaction(transaction_id)
        
        # Verify success message was printed
        mock_print.assert_called_with(f"Successfully deleted transaction id: {transaction_id}")
    
    @patch('builtins.print')
    def test_del_transaction_error_message(self, mock_print):
        """Test error message when transaction deletion fails."""
        # Setup mock to return failed deletion
        self.mock_db.execute_query.return_value = 0
        
        self.service.del_transaction(5)
        
        # Verify error message was printed
        mock_print.assert_called_with("Error deleting transaction")
    
    def test_del_account_transactions(self):
        """Test deleting all transactions for an account."""
        # Setup mock
        self.mock_db.execute_query.return_value = 5  # 5 transactions deleted
        
        # Call method
        account_id = 3
        result = self.service.del_account_transactions(account_id)
        
        # Verify database interactions
        self.mock_db.connect.assert_called_once()
        self.mock_db.close.assert_called_once()
        self.assertEqual(result, 5)
        
        # Verify safe updates were handled
        self.mock_db.set_safe_updates.assert_any_call(False)
        self.mock_db.set_safe_updates.assert_any_call(True)
        
        # Verify correct query and parameters
        call_args = self.mock_db.execute_query.call_args
        query = call_args[0][0]
        params = call_args[0][1]
        
        self.assertIn("DELETE FROM transactions WHERE account = %s", query)
        self.assertEqual(params[0], account_id)


class TestTransactionServiceIntegration(unittest.TestCase):
    """Integration tests for transaction service business logic."""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.mock_db = Mock()
        self.service = TransactionDBService(self.mock_db)
    
    def test_search_for_deletion_with_date_range(self):
        """Test search for deletion with date range."""
        # Setup mock
        expected_results = [
            (1, "2024-01-15", "Transaction 1", 100.00, "Food", "Checking", "Expense"),
            (2, "2024-01-16", "Transaction 2", 50.00, "Gas", "Credit Card", "Expense")
        ]
        self.mock_db.execute_query.return_value = expected_results
        
        # Call method
        start_date = "2024-01-01"
        end_date = "2024-01-31"
        result = self.service.search_for_deletion(start_date, end_date)
        
        # Verify results include ID for deletion
        self.assertEqual(result, expected_results)
        
        # Verify query includes ID field
        call_args = self.mock_db.execute_query.call_args
        query = call_args[0][0]
        
        self.assertIn("SELECT t.id,", query)
        self.assertIn("WHERE t.date BETWEEN %s AND %s", query)
    
    def test_search_for_deletion_all_transactions(self):
        """Test search for deletion without date range (all transactions)."""
        # Setup mock
        expected_results = [(1, "2024-01-15", "Transaction", 100.00, "Category", "Account", "Type")]
        self.mock_db.execute_query.return_value = expected_results
        
        # Call method without date parameters
        result = self.service.search_for_deletion()
        
        # Verify query doesn't include WHERE clause for dates
        call_args = self.mock_db.execute_query.call_args
        query = call_args[0][0]
        
        self.assertIn("SELECT t.id,", query)
        self.assertNotIn("WHERE t.date BETWEEN", query)
        self.assertIn("ORDER BY t.date DESC", query)
    
    def test_transaction_type_consistency(self):
        """Test that transaction types are handled consistently."""
        # Setup mock
        self.mock_db.execute_query.return_value = 1
        
        # Test different transaction types
        transaction_types = ["Income", "Expense", "Transfer", "Adjustment"]
        
        for transaction_type in transaction_types:
            with self.subTest(transaction_type=transaction_type):
                self.mock_db.reset_mock()
                
                self.service.add_transaction(
                    "2024-01-15", f"Test {transaction_type}", 100.00, 
                    1, transaction_type, 1, "Test"
                )
                
                # Verify transaction type is passed correctly
                call_args = self.mock_db.execute_query.call_args
                params = call_args[0][1]
                self.assertEqual(params[4], transaction_type)


if __name__ == '__main__':
    # Create the test directory if it doesn't exist
    os.makedirs('test', exist_ok=True)
    
    # Run the tests
    unittest.main(verbosity=2)