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


class TestAccountTransactionMethods(unittest.TestCase):
    """Test account balance modification methods with is_credit logic."""
    
    def setUp(self):
        """Set up mock database connector for transaction tests."""
        self.mock_db = Mock()
        self.service = AccountDBService(self.mock_db)
    
    def test_add_transaction_to_non_credit_account(self):
        """Test adding transaction to non-credit account (checking/savings)."""
        # Setup mock
        self.mock_db.execute_query.return_value = 1
        
        account_id = 1
        amount = 100.00
        
        # Call method
        result = self.service.add_transaction(account_id, amount)
        
        # Verify database interactions
        self.mock_db.connect.assert_called_once()
        self.mock_db.close.assert_called_once()
        self.assertEqual(result, 1)
        
        # Verify the query structure
        call_args = self.mock_db.execute_query.call_args
        query = call_args[0][0]
        params = call_args[0][1]
        
        # Check that the query handles is_credit logic correctly
        self.assertIn("CASE", query)
        self.assertIn("WHEN is_credit = TRUE THEN -%s", query)
        self.assertIn("ELSE %s", query)
        
        # Check parameters: (amount, amount, account_id)
        self.assertEqual(params[0], amount)  # amount for credit case (subtracted)
        self.assertEqual(params[1], amount)  # amount for non-credit case (added)
        self.assertEqual(params[2], account_id)
    
    def test_add_transaction_with_negative_amount(self):
        """Test adding transaction with negative amount (like a refund)."""
        # Setup mock
        self.mock_db.execute_query.return_value = 1
        
        account_id = 1
        amount = -50.00
        
        # Call method
        result = self.service.add_transaction(account_id, amount)
        
        # Verify parameters
        call_args = self.mock_db.execute_query.call_args
        params = call_args[0][1]
        
        self.assertEqual(params[0], amount)  # -50.00
        self.assertEqual(params[1], amount)  # -50.00
        self.assertEqual(params[2], account_id)
    
    def test_add_transaction_zero_amount(self):
        """Test adding transaction with zero amount."""
        # Setup mock
        self.mock_db.execute_query.return_value = 1
        
        account_id = 1
        amount = 0.00
        
        # Call method
        result = self.service.add_transaction(account_id, amount)
        
        # Verify parameters
        call_args = self.mock_db.execute_query.call_args
        params = call_args[0][1]
        
        self.assertEqual(params[0], 0.00)
        self.assertEqual(params[1], 0.00)
        self.assertEqual(params[2], account_id)


class TestAccountTransferMethods(unittest.TestCase):
    """Test account transfer methods with complex is_credit logic."""
    
    def setUp(self):
        """Set up mock database connector for transfer tests."""
        self.mock_db = Mock()
        self.service = AccountDBService(self.mock_db)
    
    def test_add_transfer_basic_structure(self):
        """Test the basic structure of transfer query."""
        # Setup mock
        self.mock_db.execute_query.return_value = 2  # Two accounts updated
        
        from_account_id = 1
        to_account_id = 2
        amount = 100.00
        
        # Call method
        result = self.service.add_transfer(from_account_id, to_account_id, amount)
        
        # Verify database interactions
        self.mock_db.connect.assert_called_once()
        self.mock_db.close.assert_called_once()
        self.assertEqual(result, 2)
        
        # Verify the query structure
        call_args = self.mock_db.execute_query.call_args
        query = call_args[0][0]
        params = call_args[0][1]
        
        # Check that the query has proper CTE and CASE logic
        self.assertIn("WITH transfer_data AS", query)
        self.assertIn("accounts.id = transfer_data.from_id", query)
        self.assertIn("accounts.id = transfer_data.to_id", query)
        self.assertIn("WHEN is_credit = TRUE", query)
        
        # Check parameters: (from_account_id, to_account_id, amount)
        self.assertEqual(params[0], from_account_id)
        self.assertEqual(params[1], to_account_id)
        self.assertEqual(params[2], amount)
    
    def test_add_transfer_with_large_amount(self):
        """Test transfer with large amount."""
        # Setup mock
        self.mock_db.execute_query.return_value = 2
        
        from_account_id = 1
        to_account_id = 2
        amount = 10000.00
        
        # Call method
        result = self.service.add_transfer(from_account_id, to_account_id, amount)
        
        # Verify parameters
        call_args = self.mock_db.execute_query.call_args
        params = call_args[0][1]
        
        self.assertEqual(params[2], 10000.00)
    
    def test_add_transfer_same_account_ids(self):
        """Test transfer between same account (edge case)."""
        # Setup mock
        self.mock_db.execute_query.return_value = 1
        
        account_id = 1
        amount = 100.00
        
        # Call method
        result = self.service.add_transfer(account_id, account_id, amount)
        
        # Verify it still processes
        call_args = self.mock_db.execute_query.call_args
        params = call_args[0][1]
        
        self.assertEqual(params[0], account_id)  # from_account_id
        self.assertEqual(params[1], account_id)  # to_account_id
        self.assertEqual(params[2], amount)
    
    def test_add_transfer_zero_amount(self):
        """Test transfer with zero amount."""
        # Setup mock
        self.mock_db.execute_query.return_value = 2
        
        from_account_id = 1
        to_account_id = 2
        amount = 0.00
        
        # Call method
        result = self.service.add_transfer(from_account_id, to_account_id, amount)
        
        # Verify parameters
        call_args = self.mock_db.execute_query.call_args
        params = call_args[0][1]
        
        self.assertEqual(params[2], 0.00)


class TestAccountBalanceLogicScenarios(unittest.TestCase):
    """Test specific business logic scenarios for account balance calculations."""
    
    def setUp(self):
        """Set up mock database connector for scenario tests."""
        self.mock_db = Mock()
        self.service = AccountDBService(self.mock_db)
    
    def test_credit_card_payment_scenario(self):
        """Test scenario: Making a payment to credit card reduces debt."""
        # Setup mock
        self.mock_db.execute_query.return_value = 1
        
        credit_card_id = 1
        payment_amount = 200.00  # Payment to credit card
        
        # For credit cards, payments should reduce the debt
        # The query logic: WHEN is_credit = TRUE THEN -payment_amount
        # This means if card has -500 balance, payment of 200 makes it -300
        result = self.service.add_transaction(credit_card_id, payment_amount)
        
        # Verify the amount is passed correctly to handle credit logic
        call_args = self.mock_db.execute_query.call_args
        params = call_args[0][1]
        
        self.assertEqual(params[0], payment_amount)  # Will be subtracted for credit
        self.assertEqual(params[1], payment_amount)  # Will be added for non-credit
        self.assertEqual(params[2], credit_card_id)
    
    def test_credit_card_purchase_scenario(self):
        """Test scenario: Making a purchase on credit card increases debt."""
        # Setup mock
        self.mock_db.execute_query.return_value = 1
        
        credit_card_id = 1
        purchase_amount = -150.00  # Purchase on credit card (negative amount)
        
        # For credit cards, purchases (negative amounts) should increase debt
        result = self.service.add_transaction(credit_card_id, purchase_amount)
        
        # Verify the amount is passed correctly
        call_args = self.mock_db.execute_query.call_args
        params = call_args[0][1]
        
        self.assertEqual(params[0], purchase_amount)  # -150, will become +150 for credit
        self.assertEqual(params[1], purchase_amount)  # -150, will subtract 150 for non-credit
        self.assertEqual(params[2], credit_card_id)
    
    def test_transfer_checking_to_credit_card_scenario(self):
        """Test scenario: Transfer from checking to credit card (payment)."""
        # Setup mock
        self.mock_db.execute_query.return_value = 2
        
        checking_id = 1     # Non-credit account
        credit_card_id = 2  # Credit account
        payment_amount = 300.00
        
        # Transfer logic:
        # From checking (non-credit): balance - payment_amount
        # To credit card (credit): balance - payment_amount (reduces debt)
        result = self.service.add_transfer(checking_id, credit_card_id, payment_amount)
        
        # Verify parameters
        call_args = self.mock_db.execute_query.call_args
        params = call_args[0][1]
        
        self.assertEqual(params[0], checking_id)
        self.assertEqual(params[1], credit_card_id)
        self.assertEqual(params[2], payment_amount)
    
    def test_transfer_credit_to_checking_scenario(self):
        """Test scenario: Transfer from credit card to checking (cash advance)."""
        # Setup mock
        self.mock_db.execute_query.return_value = 2
        
        credit_card_id = 1  # Credit account
        checking_id = 2     # Non-credit account
        advance_amount = 500.00
        
        # Transfer logic:
        # From credit card (credit): balance + advance_amount (increases debt)
        # To checking (non-credit): balance + advance_amount (increases balance)
        result = self.service.add_transfer(credit_card_id, checking_id, advance_amount)
        
        # Verify parameters
        call_args = self.mock_db.execute_query.call_args
        params = call_args[0][1]
        
        self.assertEqual(params[0], credit_card_id)
        self.assertEqual(params[1], checking_id)
        self.assertEqual(params[2], advance_amount)


if __name__ == '__main__':
    # Create the test directory if it doesn't exist
    os.makedirs('test', exist_ok=True)
    
    # Run the tests
    unittest.main(verbosity=2)
