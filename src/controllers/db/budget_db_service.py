from database_connector import DatabaseConnector

from .categories_db_service import CategoriesDBService

class BudgetDBService():
    def __init__(self, db_connector) -> None:
        self.db_connector: DatabaseConnector = db_connector

        self.categories_db_service = CategoriesDBService(self.db_connector)

    def search_all(self):
        """Returns category_names, category_types, (SUM of all transactions with same category_id), goals"""

        category_names = self.categories_db_service.select_category_names()
        category_types = self.categories_db_service.select_category_types()

        balance_query = """
        SELECT 
            category,
            SUM(amount) as total_spent
        FROM transactions 
        GROUP BY category
        """
        self.db_connector.connect()
        balance_result = self.db_connector.execute_query(balance_query)
        
        # Add goals query
        goals_query = """
        SELECT 
            category_id,
            goal
        FROM budget_goals
        """
        goals_result = self.db_connector.execute_query(goals_query)
        self.db_connector.close()

        # Sort each by ID and create lookup dictionaries
        names_dict = {item[0]: item[1] for item in sorted(category_names)}
        types_dict = {item[0]: item[1] for item in sorted(category_types)}
        balance_dict = {item[0]: item[1] for item in sorted(balance_result)} if balance_result else {}
        goals_dict = {item[0]: item[1] for item in sorted(goals_result)} if goals_result else {}

        # Get all unique IDs and sort them
        all_ids = sorted(set(names_dict.keys()) | set(types_dict.keys()) | set(balance_dict.keys()) | set(goals_dict.keys()))

        # Create combined tuples (name, type, balance, goal)
        result = []
        for category_id in all_ids:
            name = names_dict.get(category_id, "Unknown")
            category_type = types_dict.get(category_id, "Unknown") 
            balance = balance_dict.get(category_id, 0.0)
            goal = goals_dict.get(category_id, 0.0)
            result.append((name, category_type, balance, goal))

        return result
