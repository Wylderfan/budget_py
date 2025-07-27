from datetime import datetime

from database_connector import DatabaseConnector
from config.config_loader import ConfigLoader

class AccountDBService():
    def __init__(self, db_connector) -> None:
        self.db_connector: DatabaseConnector = db_connector
        self.json_config_loader = ConfigLoader()
        
    def add_account(self, name, balance, account_type):
        date_created = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        is_credit = self.json_config_loader.is_credit_account(account_type)
        self.db_connector.connect()

        insert_query = """
        INSERT INTO accounts (date_created, name, balance, type, is_credit)
        VALUES (%s, %s, %s, %s, %s)
        """

        result = self.db_connector.execute_query(
                insert_query,
                (date_created, name, balance, account_type, is_credit)
            )
        if result == 1:
            print("Account has successfully been added")
        else:
            print("Error with insert query")

        self.db_connector.close()

        return result

    def del_account(self, id):
        self.db_connector.connect()

        query = """
        DELETE FROM accounts WHERE id = %s
        """

        result = self.db_connector.execute_query(query, (id,))

        print(f"The result from deletion is {result}")

        self.db_connector.close()
        return result

    def search_account(self, id=None, name=None):
        """Needs either id || name"""
        self.db_connector.connect()

        if id is not None:
            query = """
            SELECT * FROM accounts WHERE id = %s
            """
        elif name is not None:
            query = """
            SELECT * FROM accounts WHERE name = %s
            """
        else:
            print("Must use arg id or name")
            return
        
        if id is not None:
            result = self.db_connector.execute_query(query, (id,))
        else:
            result = self.db_connector.execute_query(query, (name,))

        self.db_connector.close()
        
        return result

    def search_all(self):
        self.db_connector.connect()

        query = """
        SELECT * FROM accounts
        """

        result = self.db_connector.execute_query(query)

        self.db_connector.close()

        return result

    def modify_balance(self, id, amount):
        self.db_connector.connect()

        query = """
        UPDATE accounts
        SET balance = %s
        WHERE id = %s
        """

        result = self.db_connector.execute_query(query, (amount, id))

        if result == 1:
            print("Balance successfully modified")
        else:
            print("Error modifying balance")

        self.db_connector.close()

        return result

    def select_name_id_all_accounts(self):
        self.db_connector.connect()

        query = """
        SELECT id, name FROM accounts
        """

        result = self.db_connector.execute_query(query)

        self.db_connector.close()

        return result

    def transfer_transactions(self, account_id, transfer_account_id):
        self.db_connector.connect()
        
        query = """
        UPDATE transactions
        SET account = %s
        WHERE account = %s
        """
        
        try:
            self.db_connector.set_safe_updates(False)
            rows_affected = self.db_connector.execute_query(query, (transfer_account_id, account_id))
            self.db_connector.set_safe_updates(True)
        except Exception as e:
            self.db_connector.set_safe_updates(True)
            print(f"Error transferring transactions: {e}")
            rows_affected = None
        
        self.db_connector.close()

        return rows_affected

    def add_transaction(self, id, amount):
        self.db_connector.connect()

        query = """
        UPDATE accounts
        SET balance = balance + CASE
            WHEN is_credit = TRUE THEN -%s
            ELSE %s
        END
        WHERE id = %s
        """

        rows_affected = self.db_connector.execute_query(query, (amount, amount, id,))
        
        self.db_connector.close()
        
        return rows_affected

    def add_transfer(self, from_account_id, to_account_id, amount):
        self.db_connector.connect()

        query = """
        WITH transfer_data AS (
            SELECT %s as from_id, %s as to_id, %s as amount
        )
        UPDATE accounts
        JOIN transfer_data ON accounts.id IN (transfer_data.from_id, transfer_data.to_id)
        SET balance = balance + CASE
            WHEN accounts.id = transfer_data.from_id THEN 
                CASE
                    WHEN is_credit = TRUE THEN transfer_data.amount
                    ELSE -transfer_data.amount
                END
            WHEN accounts.id = transfer_data.to_id THEN 
                CASE
                    WHEN is_credit = TRUE THEN -transfer_data.amount
                    ELSE transfer_data.amount
                END
        END
        """

        result = self.db_connector.execute_query(query, (from_account_id, to_account_id, amount))

        self.db_connector.close()

        return result
