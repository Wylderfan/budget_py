import unittest
from unittest.mock import Mock, patch, MagicMock
import sys
import os

# Add the parent directory to the path so we can import database_connector
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database_connector import DatabaseConnector


class TestDatabaseConnector(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.db = DatabaseConnector("localhost", "testuser", "testpass", "testdb")
    
    def tearDown(self):
        """Clean up after each test method."""
        if hasattr(self.db, 'connection') and self.db.connection:
            self.db.close()
    
    @patch('database_connector.mysql.connector.connect')
    def test_successful_connection(self, mock_connect):
        """Test successful database connection."""
        # Mock the connection and cursor
        mock_connection = Mock()
        mock_cursor = Mock()
        mock_connection.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_connection
        
        # Test connection
        self.db.connect()
        
        # Verify connection was attempted with correct parameters
        mock_connect.assert_called_once_with(
            host="localhost",
            user="testuser", 
            password="testpass",
            database="testdb"
        )
        
        # Verify connection and cursor are set
        self.assertEqual(self.db.connection, mock_connection)
        self.assertEqual(self.db.cursor, mock_cursor)
    
    @patch('database_connector.mysql.connector.connect')
    def test_connection_failure(self, mock_connect):
        """Test database connection failure."""
        # Make connect raise an exception
        mock_connect.side_effect = Exception("Connection failed")
        
        # Test connection (should not raise exception)
        self.db.connect()
        
        # Connection should be None
        self.assertIsNone(self.db.connection)
        self.assertIsNone(self.db.cursor)
    
    def test_execute_query_select_full_results(self):
        """Test SELECT query returning full results (no specific_column)."""
        # Mock connection and cursor
        self.db.connection = Mock()
        self.db.connection.is_connected.return_value = True
        self.db.cursor = Mock()
        
        # Mock fetchall to return sample data
        sample_data = [
            ('2024-01-01', 'Groceries', 50.00, 'Food'),
            ('2024-01-02', 'Gas', 30.00, 'Transportation'),
            ('2024-01-03', 'Movie', 15.00, 'Entertainment')
        ]
        self.db.cursor.fetchall.return_value = sample_data
        
        # Execute query
        result = self.db.execute_query("SELECT date, description, amount, category FROM transactions")
        
        # Should return full results
        self.assertEqual(result, sample_data)
        self.db.cursor.execute.assert_called_once_with("SELECT date, description, amount, category FROM transactions", None)
    
    def test_execute_query_select_specific_column(self):
        """Test SELECT query returning specific column."""
        # Mock connection and cursor
        self.db.connection = Mock()
        self.db.connection.is_connected.return_value = True
        self.db.cursor = Mock()
        
        # Mock fetchall to return sample data
        sample_data = [
            ('2024-01-01', 'Groceries', 50.00, 'Food'),
            ('2024-01-02', 'Gas', 30.00, 'Transportation'),
            ('2024-01-03', 'Movie', 15.00, 'Entertainment')
        ]
        self.db.cursor.fetchall.return_value = sample_data
        
        # Test getting first column (dates)
        result = self.db.execute_query("SELECT date, description, amount, category FROM transactions", specific_column=0)
        expected = ['2024-01-01', '2024-01-02', '2024-01-03']
        self.assertEqual(result, expected)
        
        # Test getting second column (descriptions)
        result = self.db.execute_query("SELECT date, description, amount, category FROM transactions", specific_column=1)
        expected = ['Groceries', 'Gas', 'Movie']
        self.assertEqual(result, expected)
        
        # Test getting fourth column (categories)
        result = self.db.execute_query("SELECT date, description, amount, category FROM transactions", specific_column=3)
        expected = ['Food', 'Transportation', 'Entertainment']
        self.assertEqual(result, expected)
    
    def test_execute_query_insert_update_delete(self):
        """Test INSERT, UPDATE, DELETE queries."""
        # Mock connection and cursor
        self.db.connection = Mock()
        self.db.connection.is_connected.return_value = True
        self.db.cursor = Mock()
        self.db.cursor.rowcount = 1
        
        # Test INSERT
        result = self.db.execute_query("INSERT INTO transactions (amount, description) VALUES (%s, %s)", (50.00, "Test"))
        self.assertEqual(result, 1)
        self.db.connection.commit.assert_called()
        
        # Test UPDATE
        result = self.db.execute_query("UPDATE transactions SET amount = %s WHERE id = %s", (60.00, 1))
        self.assertEqual(result, 1)
        
        # Test DELETE
        result = self.db.execute_query("DELETE FROM transactions WHERE id = %s", (1,))
        self.assertEqual(result, 1)
    
    def test_execute_query_with_parameters(self):
        """Test query execution with parameters."""
        # Mock connection and cursor
        self.db.connection = Mock()
        self.db.connection.is_connected.return_value = True
        self.db.cursor = Mock()
        self.db.cursor.fetchall.return_value = [('Groceries', 50.00)]
        
        # Execute query with parameters
        params = ('Food', '2024-01-01')
        result = self.db.execute_query("SELECT description, amount FROM transactions WHERE category = %s AND date = %s", params)
        
        # Verify parameters were passed correctly
        self.db.cursor.execute.assert_called_once_with("SELECT description, amount FROM transactions WHERE category = %s AND date = %s", params)
        self.assertEqual(result, [('Groceries', 50.00)])
    
    def test_execute_query_no_connection(self):
        """Test query execution when not connected."""
        # No connection
        self.db.connection = None
        
        result = self.db.execute_query("SELECT * FROM transactions")
        self.assertIsNone(result)
    
    def test_execute_query_connection_lost(self):
        """Test query execution when connection is lost."""
        # Mock connection that reports as disconnected
        self.db.connection = Mock()
        self.db.connection.is_connected.return_value = False
        
        result = self.db.execute_query("SELECT * FROM transactions")
        self.assertIsNone(result)
    
    @patch('database_connector.mysql.connector.Error', Exception)
    def test_execute_query_mysql_error(self):
        """Test query execution with MySQL error."""
        # Mock connection and cursor
        self.db.connection = Mock()
        self.db.connection.is_connected.return_value = True
        self.db.cursor = Mock()
        
        # Make execute raise an exception
        self.db.cursor.execute.side_effect = Exception("SQL Error")
        
        result = self.db.execute_query("SELECT * FROM transactions")
        self.assertIsNone(result)
    
    def test_close_connection(self):
        """Test closing database connection."""
        # Mock connection and cursor
        mock_connection = Mock()
        mock_cursor = Mock()
        mock_connection.is_connected.return_value = True
        
        self.db.connection = mock_connection
        self.db.cursor = mock_cursor
        
        # Close connection
        self.db.close()
        
        # Verify close methods were called
        mock_cursor.close.assert_called_once()
        mock_connection.close.assert_called_once()
    
    def test_close_no_connection(self):
        """Test closing when no connection exists."""
        self.db.connection = None
        # Should not raise an exception
        self.db.close()


class TestDatabaseConnectorIntegration(unittest.TestCase):
    """Integration tests that demonstrate how to use the DatabaseConnector."""
    
    def setUp(self):
        """Set up mock database connector for integration tests."""
        self.db = DatabaseConnector("localhost", "testuser", "testpass", "testdb")
        
        # Mock the connection for integration tests
        self.db.connection = Mock()
        self.db.connection.is_connected.return_value = True
        self.db.cursor = Mock()

if __name__ == '__main__':
    # Create the tests directory if it doesn't exist
    os.makedirs('tests', exist_ok=True)
    
    # Run the tests
    unittest.main(verbosity=2)
