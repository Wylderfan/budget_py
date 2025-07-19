from database_connector import DatabaseConnector

from .categories_db_service import CategoriesDBService

class BudgetDBService():
    def __init__(self, db_connector) -> None:
        self.db_connector: DatabaseConnector = db_connector

        self.categories_db_service = CategoriesDBService(self.db_connector)

    def search_all(self):
        """Returns category_names, category_types, (SUM of all transactions with same category_id), goals"""

        self.db_connector.connect()

        category_names = self.categories_db_service.select_category_names()
        category_types = self.categories_db_service.select_category_types()

        balance_query = """
        SELECT 
            category,
            SUM(amount) as total_spent
        FROM transactions 
        GROUP BY category
        """
        balance_result = self.db_connector.execute_query(balance_query)

        print(f"Balance: {balance_result}")
            

