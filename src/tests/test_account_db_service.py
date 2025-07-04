import unittest
from unittest.mock import Mock, patch
import sys
import os
from datetime import datetime

# Add the parent directory to the path so we can import the service
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from controllers.db.account_db_service import AccountDBService


class TestAccountDBService(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        # Create a mock database connector
        self.mock_db = Mock()
        self.service = AccountDBService(self.mock_db)
    
    def test_add_account_checking(self):
        """Test adding a checking account (non-credit)."""
        # Setup mock
        self.mock_db.execute_query.return_value = 1
        
        # Test data
        name = "Main Checking"
        balance = 1500.00
        account_type = "Chequing"
        
        # Call method
        self.service.add_account(name, balance, account_type)
        
        # Verify database interactions
        self.mock_db.connect.assert_called_once()
        self.mock_db.close.assert_called_once()
        
        # Verify the query was called correctly
        self.mock_db.execute_query.assert_called_once()
        call_args = self.mock_db.execute_query.call_args
        
        # Check the query structure
        query = call_args[0][0]
        params = call_args[0][1]
        
        self.assertIn("INSERT INTO accounts", query)
        self.assertIn("date_created, name, balance, type, is_credit", query)
        
        # Check parameters (date_created, name, balance, account_type, is_credit)
        self.assertEqual(params[1], name)
        self.assertEqual(params[2], balance)
        self.assertEqual(params[3], account_type)
        self.assertEqual(params[4], False)  # is_credit should be False for checking
    
    def test_add_account_credit_card(self):
        """Test adding a credit card account (credit type)."""
        # Setup mock
        self.mock_db.execute_query.return_value = 1
        
        # Test data
        name = "Main Credit Card"
        balance = -500.00
        account_type = "Credit Card"
        
        # Call method
        self.service.add_account(name, balance, account_type)
        
        # Verify the query was called
        call_args = self.mock_db.execute_query.call_args
        params = call_args[0][1]
        
        # Check that is_credit is True for credit card
        self.assertEqual(params[4], True)  # is_credit should be True
    
    def test_add_account_line_of_credit(self):
        """Test adding a line of credit account (credit type)."""
        # Setup mock
        self.mock_db.execute_query.return_value = 1
        
        # Test data
        name = "Personal LOC"
        balance = 0.00
        account_type = "Line of Credit"
        
        # Call method
        self.service.add_account(name, balance, account_type)
        
        # Verify the query was called
        call_args = self.mock_db.execute_query.call_args
        params = call_args[0][1]
        
        # Check that is_credit is True for line of credit
        self.assertEqual(params[4], True)  # is_credit should be True
    
    def test_add_account_case_insensitive_credit(self):
        """Test that credit type detection is case insensitive."""
        # Setup mock
        self.mock_db.execute_query.return_value = 1
        
        # Test with different cases
        test_cases = [
            "CREDIT CARD",
            "credit card", 
            "Credit Card",
            "LINE OF CREDIT",
            "line of credit",
            "Line Of Credit"
        ]
        
        for account_type in test_cases:
            with self.subTest(account_type=account_type):
                self.mock_db.reset_mock()
                
                self.service.add_account("Test Account", 100.00, account_type)
                
                call_args = self.mock_db.execute_query.call_args
                params = call_args[0][1]
                self.assertEqual(params[4], True, f"Failed for account type: {account_type}")
    
    @patch('builtins.print')
    def test_add_account_success_message(self, mock_print):
        """Test success message when account is added."""
        # Setup mock to return successful insert
        self.mock_db.execute_query.return_value = 1
        
        self.service.add_account("Test Account", 100.00, "Savings")
        
        # Verify success message was printed
        mock_print.assert_called_with("Account has successfully been added")
    
    @patch('builtins.print')
    def test_add_account_error_message(self, mock_print):
        """Test error message when account insert fails."""
        # Setup mock to return failed insert
        self.mock_db.execute_query.return_value = 0
        
        self.service.add_account("Test Account", 100.00, "Savings")
        
        # Verify error message was printed
        mock_print.assert_called_with("Error with insert query")
    
class TestAccountDBServiceIntegration(unittest.TestCase):
    """Integration tests demonstrating typical usage patterns."""
    
    def setUp(self):
        """Set up mock database connector for integration tests."""
        self.mock_db = Mock()
        self.service = AccountDBService(self.mock_db)
    
    def test_multiple_account_types(self):
        """Test adding different types of accounts."""
        # Setup mock to always return success
        self.mock_db.execute_query.return_value = 1
        
        accounts_to_add = [
            ("Checking Account", 1500.00, "Chequing"),
            ("Savings Account", 5000.00, "Savings"),
            ("Credit Card", -200.00, "Credit Card"),
            ("Line of Credit", 0.00, "Line of Credit")
        ]
        
        for name, balance, account_type in accounts_to_add:
            with self.subTest(account_type=account_type):
                self.mock_db.reset_mock()
                
                self.service.add_account(name, balance, account_type)
                
                # Verify database was called
                self.mock_db.execute_query.assert_called_once()
                
                # Check the parameters
                call_args = self.mock_db.execute_query.call_args
                params = call_args[0][1]
                
                expected_is_credit = account_type.lower() in ["credit card", "line of credit"]
                self.assertEqual(params[4], expected_is_credit)


if __name__ == '__main__':
    # Create the test directory if it doesn't exist
    os.makedirs('test', exist_ok=True)
    
    # Run the tests
    unittest.main(verbosity=2)
