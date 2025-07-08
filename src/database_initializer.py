import mysql.connector
from database_connector import DatabaseConnector

class DatabaseInitializer:
    def __init__(self, db_connector: DatabaseConnector):
        self.db = db_connector
        
        # Define the exact schema from README.md
        self.required_tables = {
            'transactions': {
                'id': 'INT AUTO_INCREMENT PRIMARY KEY',
                'date': 'DATE NOT NULL',
                'description': 'VARCHAR(255) NOT NULL',
                'amount': 'DECIMAL(10,2) NOT NULL',
                'category': 'INT NOT NULL',
                'type': 'VARCHAR(10) NOT NULL',
                'notes': 'VARCHAR(1000)',
                'account': 'INT NOT NULL'
            },
            'accounts': {
                'id': 'INT AUTO_INCREMENT PRIMARY KEY',
                'name': 'VARCHAR(45) NOT NULL',
                'date_created': 'DATE',
                'balance': 'DECIMAL(10,2) NOT NULL',
                'type': 'VARCHAR(45) NOT NULL',
                'is_credit': 'TINYINT NOT NULL'
            },
            'categories': {
                'id': 'INT AUTO_INCREMENT PRIMARY KEY',
                'name': 'VARCHAR(45) NOT NULL',
                'date_created': 'DATE',
                'type': 'VARCHAR(45) NOT NULL'
            }
        }
    
    def initialize_database(self):
        try:
            # Connect to database
            self.db.connect()
            if not self.db.connection or not self.db.connection.is_connected():
                print("Failed to connect to database")
                return False
            
            print("Checking database schema...")
            
            # Check and create each required table
            for table_name, schema in self.required_tables.items():
                if not self._table_exists(table_name):
                    print(f"Creating missing table: {table_name}")
                    self._create_table(table_name, schema)
                elif not self._validate_table_schema(table_name, schema):
                    print(f"Table {table_name} schema mismatch - recreating")
                    self._drop_table(table_name)
                    self._create_table(table_name, schema)
                else:
                    print(f"Table {table_name} - OK")
            
            print("Database schema validation complete")
            return True
            
        except Exception as e:
            print(f"Database initialization failed: {e}")
            return False
    
    def _table_exists(self, table_name):
        query = """
        SELECT COUNT(*) 
        FROM information_schema.tables 
        WHERE table_schema = %s AND table_name = %s
        """
        result = self.db.execute_query(query, (self.db.database, table_name))
        if result is None or not isinstance(result, list) or len(result) == 0:
            return False
        return result[0][0] > 0 # type: ignore
    
    def _validate_table_schema(self, table_name, expected_schema):
        query = """
        SELECT column_name, column_type, is_nullable, column_key, extra
        FROM information_schema.columns 
        WHERE table_schema = %s AND table_name = %s
        ORDER BY ordinal_position
        """
        
        result = self.db.execute_query(query, (self.db.database, table_name))
        if not result or not isinstance(result, list):
            return False
        
        # Convert result to a more manageable format
        current_columns = {}
        for row in result:
            col_name, col_type, is_nullable, col_key, extra = row
            current_columns[col_name] = {
                'type': col_type,
                'nullable': is_nullable == 'YES',
                'key': col_key,
                'extra': extra
            }
        
        # Check if all expected columns exist with correct properties
        for col_name, col_def in expected_schema.items():
            if col_name not in current_columns:
                return False
            
            # Basic type checking (simplified for lightweight validation)
            current_col = current_columns[col_name]
            if not self._column_types_match(col_def, current_col):
                return False
        
        return True
    
    def _column_types_match(self, expected_def, current_col):
        expected_upper = expected_def.upper()
        current_type_upper = current_col['type'].upper()
        
        # Check basic type compatibility
        if 'INT' in expected_upper and 'INT' not in current_type_upper:
            return False
        if 'VARCHAR' in expected_upper and 'VARCHAR' not in current_type_upper:
            return False
        if 'DECIMAL' in expected_upper and 'DECIMAL' not in current_type_upper:
            return False
        if 'DATE' in expected_upper and current_type_upper != 'DATE':
            return False
        if 'TINYINT' in expected_upper and 'TINYINT' not in current_type_upper:
            return False
        
        # Check NOT NULL constraint
        if 'NOT NULL' in expected_upper and current_col['nullable']:
            return False
        
        return True
    
    def _create_table(self, table_name, schema):
        columns = []
        for col_name, col_def in schema.items():
            columns.append(f"{col_name} {col_def}")
        
        create_query = f"CREATE TABLE {table_name} ({', '.join(columns)})"
        self.db.execute_query(create_query)
        print(f"Created table: {table_name}")
    
    def _drop_table(self, table_name):
        drop_query = f"DROP TABLE IF EXISTS {table_name}"
        self.db.execute_query(drop_query)
        print(f"Dropped table: {table_name}") 