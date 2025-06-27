from datetime import datetime
from ...database_connector import DatabaseConnector

class ModifyAccountDBService():
    def __init__(self, db_connector) -> None:
        self.db_connector: DatabaseConnector = db_connector
        
    def add_account(self, name, balance, account_type):
        date_added = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        if account_type.lower() == "credit card" or account_type.lower() == "line of credit":
            is_credit = True
        else:
            is_credit = False
        self.db_connector.connect()

        # Add logic here

        self.db_connector.close()

    def del_account(self, id):
        self.db_connector.connect()

        # Add logic here

        self.db_connector.close()

    def search_account(self, id=None, name=None):
        """Needs either id || name"""
        self.db_connector.connect()

        # Add logic here

        self.db_connector.close()

