from controllers.db.account_db_service import AccountDBService
from database_connector import DatabaseConnector

class TransactionDBService():
    def __init__(self, db_connector) -> None:
        self.db_connector: DatabaseConnector = db_connector

        self.account_db_service = AccountDBService(self.db_connector)

    def add_transaction(self, date, description, amount, category_id, transaction_type, account_id, notes=""):
        self.db_connector.connect()

        insert_query = """
        INSERT INTO transactions (date, description, amount, category, type, account, notes)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """

        result = self.db_connector.execute_query(
                insert_query,
                (date, description, amount, category_id, transaction_type, account_id, notes)
            )
        if result == 1:
            print("Transaction has been successfully added")
        else:
            print("Error with insert query")

        self.db_connector.close()
        return result

    def add_transfer(self, date, amount, from_account, to_account, notes):
        from_account_name = self.account_db_service.search_account(id=from_account)[0][1] # type: ignore
        to_account_name = self.account_db_service.search_account(id=to_account)[0][1] # type: ignore
        description = f"Transfer from {from_account_name} to {to_account_name}"
        transaction_type = "Transfer"

        self.db_connector.connect()
        query = """
        INSERT INTO transactions (date, description, amount, type, account, notes)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        result = self.db_connector.execute_query(query, (date, description, amount, transaction_type, to_account, notes))
        self.db_connector.close()
        return result

    def del_account_transactions(self, account_id):
        self.db_connector.connect()
        query = """
        DELETE FROM transactions WHERE account = %s
        """
        
        self.db_connector.set_safe_updates(False)
        result = self.db_connector.execute_query(query, (account_id,))
        self.db_connector.set_safe_updates(True)

        self.db_connector.close()
        return result

    def del_transaction(self, id):
        self.db_connector.connect()

        query = """
        DELETE FROM transactions WHERE id = %s
        """

        result = self.db_connector.execute_query(query, (id,))

        if result == 1:
            print(f"Successfully deleted transaction id: {id}")
        else:
            print(f"Error deleting transaction")

        self.db_connector.close()
        return result

    def search_transaction(self, id=None, description=None):
        """Needs either id or description"""
        self.db_connector.connect()

        if id is not None:
            query = """
            SELECT * FROM transactions WHERE id = %s
            """
        elif description is not None:
            query = """
            SELECT * FROM transactions WHERE description = %s
            """
        else:
            print("Must use arg id or description")
            return

        if id is not None:
            result = self.db_connector.execute_query(query, (id,))
        else:
            result = self.db_connector.execute_query(query, (description,))

        self.db_connector.close()
        
        return result

    def search_all(self):
        self.db_connector.connect()

        query = """
        SELECT t.date, t.description, t.amount, c.name as category_name, a.name as account_name, t.type
        FROM transactions t
        LEFT JOIN categories c ON t.category = c.id
        LEFT JOIN accounts a ON t.account = a.id
        ORDER BY t.date DESC
        """

        result = self.db_connector.execute_query(query)

        self.db_connector.close()

        return result

    def search_by_date_range(self, start_date, end_date):
        self.db_connector.connect()

        query = """
        SELECT t.date, t.description, t.amount, c.name as category_name, a.name as account_name, t.type
        FROM transactions t
        LEFT JOIN categories c ON t.category = c.id
        LEFT JOIN accounts a ON t.account = a.id
        WHERE t.date BETWEEN %s AND %s
        ORDER BY t.date DESC
        """

        result = self.db_connector.execute_query(query, (start_date, end_date))

        self.db_connector.close()

        return result

    def search_by_category(self, category_id):
        self.db_connector.connect()

        query = """
        SELECT t.date, t.description, t.amount, c.name as category_name, a.name as account_name, t.type
        FROM transactions t
        LEFT JOIN categories c ON t.category = c.id
        LEFT JOIN accounts a ON t.account = a.id
        WHERE t.category = %s
        ORDER BY t.date DESC
        """

        result = self.db_connector.execute_query(query, (category_id,))

        self.db_connector.close()

        return result

    def search_by_account(self, account_id):
        self.db_connector.connect()

        query = """
        SELECT t.date, t.description, t.amount, c.name as category_name, a.name as account_name, t.type
        FROM transactions t
        LEFT JOIN categories c ON t.category = c.id
        LEFT JOIN accounts a ON t.account = a.id
        WHERE t.account = %s
        ORDER BY t.date DESC
        """

        result = self.db_connector.execute_query(query, (account_id,))

        self.db_connector.close()

        return result

    def search_for_deletion(self, start_date=None, end_date=None):
        """Search transactions with ID for deletion purposes"""
        self.db_connector.connect()

        if start_date and end_date:
            query = """
            SELECT t.id, t.date, t.description, t.amount, c.name as category_name, a.name as account_name, t.type
            FROM transactions t
            LEFT JOIN categories c ON t.category = c.id
            LEFT JOIN accounts a ON t.account = a.id
            WHERE t.date BETWEEN %s AND %s
            ORDER BY t.date DESC
            """
            result = self.db_connector.execute_query(query, (start_date, end_date))
        else:
            query = """
            SELECT t.id, t.date, t.description, t.amount, c.name as category_name, a.name as account_name, t.type
            FROM transactions t
            LEFT JOIN categories c ON t.category = c.id
            LEFT JOIN accounts a ON t.account = a.id
            ORDER BY t.date DESC
            """
            result = self.db_connector.execute_query(query)

        self.db_connector.close()

        return result 
