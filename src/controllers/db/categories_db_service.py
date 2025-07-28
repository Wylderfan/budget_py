from datetime import datetime

from database_connector import DatabaseConnector

class CategoriesDBService():
    def __init__(self, db_connector) -> None:
        self.db_connector: DatabaseConnector = db_connector

    def add_category(self, name, category_type):
        date_created = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        self.db_connector.connect()

        insert_query = """
        INSERT INTO categories (date_created, name, type)
        VALUES (%s, %s, %s)
        """

        result = self.db_connector.execute_query(
                insert_query,
                (date_created, name, category_type)
                )
        if result == 1:
            print("Category has been successfully added")
        else:
            print("Error with insert query")

        self.db_connector.close()

        return result

    def del_category(self, id):
        self.db_connector.connect()

        query = """
        DELETE FROM categories WHERE id = %s
        """

        result = self.db_connector.execute_query(query, (id,))

        if result == 1:
            print(f"successfully deleted category id: {id}")
        else:
            print(f"Error deleting category")

        self.db_connector.close()
        return result

    def add_goal(self, category_name, goal_amount):
        category_id = self.search_categories(name=category_name)[0][0] # type: ignore
        date_created = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        self.db_connector.connect()

        insert_query = """
        INSERT INTO budget_goals (category_id, goal, date_created)
        VALUES (%s, %s, %s)
        """
        
        result = self.db_connector.execute_query(insert_query, (category_id, goal_amount, date_created))

        self.db_connector.close()
        return result

    def modify_goal(self, category_id, goal):
        self.db_connector.connect()

        query = """
        UPDATE budget_goals
        SET goal = %s
        WHERE category_id = %s
        """

        print(f"Debug statment: {(goal, category_id)}")
        result = self.db_connector.execute_query(query, (goal, category_id))

        self.db_connector.close()
        return result

    def search_categories(self, id=None, name=None):
        """Needs either id || name"""
        self.db_connector.connect()

        if id is not None:
            query = """
            SELECT * FROM categories WHERE id = %s
            """
        elif name is not None:
            query = """
            SELECT * FROM categories WHERE name = %s
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
        SELECT * FROM categories
        """

        result = self.db_connector.execute_query(query)

        self.db_connector.close()

        return result

    def select_category_names(self):
        self.db_connector.connect()

        query = """
        SELECT id, name FROM categories
        """

        result = self.db_connector.execute_query(query)

        self.db_connector.close()

        return result

    def select_category_types(self):
        self.db_connector.connect()

        query = """
        SELECT id, type FROM categories
        """

        result = self.db_connector.execute_query(query)

        self.db_connector.close()

        return result
