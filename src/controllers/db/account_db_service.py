from datetime import datetime
import re

from database_connector import DatabaseConnector

class AccountDBService():
    def __init__(self, db_connector) -> None:
        self.db_connector: DatabaseConnector = db_connector
        
    def add_account(self, name, balance, account_type):
        date_created = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        if account_type.lower() == "credit card" or account_type.lower() == "line of credit": # TODO change to search env file for proper sorting
            is_credit = True
        else:
            is_credit = False
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

        return result

    def select_name_id_all_accounts(self):
        self.db_connector.connect()

        query = """
        SELECT name, id FROM accounts
        """

        result = self.db_connector.execute_query(query)

        self.db_connector.close()

        return result
