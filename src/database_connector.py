import mysql.connector

class DatabaseConnector:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None
        self.cursor = None

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            self.cursor = self.connection.cursor()
            print("Successfully connected to the database.")
        except mysql.connector.Error as e:
            print(f"Error connecting to MySQL: {e}")

    def execute_query(self, query, params=None):
            if self.connection and self.connection.is_connected(): # type: ignore
                try:
                    self.cursor.execute(query, params) # type: ignore
                    # Check if the query is a SELECT statement
                    if query.strip().lower().startswith('select'):
                        results = self.cursor.fetchall() # type: ignore
                        return [row[0] for row in results] # type: ignore
                    else:
                        # For INSERT, UPDATE, DELETE statements
                        self.connection.commit() # type: ignore
                        # Return the number of affected rows
                        return self.cursor.rowcount # type: ignore
                except mysql.connector.Error as e:
                    print(f"Error executing query: {e}")
                    return None
            else:
                print("Not connected to the database.")
                return None

    def close(self):
        if self.connection.is_connected(): # type: ignore
            self.cursor.close() # type: ignore
            self.connection.close() # type: ignore
            print("MySQL connection is closed.")