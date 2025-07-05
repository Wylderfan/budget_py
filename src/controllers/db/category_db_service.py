from datetime import datetime

from database_connector import DatabaseConnector

class CategoryDBService():
    def __init__(self, db_connector) -> None:
        self.db_connector: DatabaseConnector = db_connector
