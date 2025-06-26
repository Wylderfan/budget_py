import sys
import os
from dotenv import load_dotenv
from PyQt6.QtWidgets import QApplication
from views.main_window import MainWindow
from database_connector import DatabaseConnector

def main():
    # Load environment variables
    load_dotenv()
    
    # Initialize database connection
    db = DatabaseConnector(
        host=os.getenv('DB_HOST'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        database=os.getenv('DB_NAME')
    )
    
    # Create Qt application
    app = QApplication(sys.argv)
    
    # Create and show main window
    window = MainWindow(db)
    window.show()
    
    # Start application event loop
    sys.exit(app.exec())

if __name__ == '__main__':
    main() 
