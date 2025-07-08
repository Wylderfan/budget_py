from PyQt6.QtWidgets import (
    QLineEdit, QVBoxLayout, QPushButton, QFormLayout, 
    QComboBox, QHBoxLayout, QMessageBox, QLabel, QDateEdit
)
from PyQt6.QtCore import Qt, QDate
from views.popup_window import PopUpWindow

from controllers.db.categories_db_service import CategoriesDBService
from controllers.db.account_db_service import AccountDBService
from controllers.db.transaction_db_service import TransactionDBService

class AddTransactionsWindow(PopUpWindow):
    def __init__(self, window_name: str, min_width: int, min_height: int, db, parent=None, refresh_callback=None) -> None:
        super().__init__(window_name, min_width, min_height, db, parent)
        self.refresh_callback = refresh_callback

        # Initialize database services
        self.categories_db_service = CategoriesDBService(self.get_db())
        self.accounts_db_service = AccountDBService(self.get_db())
        self.transaction_db_service = TransactionDBService(self.get_db())

        self.setup_ui()

    def setup_ui(self):
        main_layout = QVBoxLayout()
        
        title_label = QLabel("Add New Transaction")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title_label)
        
        # Form layout for inputs
        form_layout = QFormLayout()
        
        # Amount input
        self.amount_input = QLineEdit()
        self.amount_input.setPlaceholderText("0.00")
        form_layout.addRow("Amount ($):", self.amount_input)
        
        # Description input
        self.description_input = QLineEdit()
        self.description_input.setPlaceholderText("Description")
        form_layout.addRow("Description:", self.description_input)
        
        # Category combo box
        self.category_combo = QComboBox()
        self.load_categories()
        form_layout.addRow("Category:", self.category_combo)
        
        # Account combo box
        self.account_combo = QComboBox()
        self.load_accounts()
        form_layout.addRow("Account:", self.account_combo)
        
        # Date input
        self.date_input = QDateEdit()
        self.date_input.setDate(QDate.currentDate())
        form_layout.addRow("Date:", self.date_input)
        
        # Transaction type combo box
        self.type_combo = QComboBox()
        self.type_combo.addItems(["Expense", "Income"])
        form_layout.addRow("Type:", self.type_combo)
        
        # Notes input
        self.notes_input = QLineEdit()
        self.notes_input.setPlaceholderText("Notes (optional)")
        form_layout.addRow("Notes:", self.notes_input)
        
        main_layout.addLayout(form_layout)
        
        # Buttons layout
        button_layout = QHBoxLayout()
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setAutoDefault(False)
        cancel_btn.clicked.connect(self.reject)
        
        add_transaction_btn = QPushButton("Add Transaction")
        add_transaction_btn.clicked.connect(self.add_transaction)
        
        button_layout.addWidget(cancel_btn)
        button_layout.addWidget(add_transaction_btn)
        
        main_layout.addLayout(button_layout)
        
        self.setLayout(main_layout)

    def load_categories(self):
        """Load categories from database into combo box"""
        self.category_combo.clear()
        try:
            categories = self.categories_db_service.select_category_names()
            if categories and isinstance(categories, list):
                for category in categories:
                    # category is (name, id)
                    self.category_combo.addItem(str(category[0]), category[1])
        except Exception as e:
            print(f"Error loading categories: {e}")
            QMessageBox.warning(self, "Error", "Could not load categories from database.")

    def load_accounts(self):
        """Load accounts from database into combo box"""
        self.account_combo.clear()
        try:
            accounts = self.accounts_db_service.select_name_id_all_accounts()
            if accounts and isinstance(accounts, list):
                for account in accounts:
                    # account is (name, id)
                    self.account_combo.addItem(str(account[0]), account[1])
        except Exception as e:
            print(f"Error loading accounts: {e}")
            QMessageBox.warning(self, "Error", "Could not load accounts from database.")
    
    def add_transaction(self):
        try:
            amount = float(self.amount_input.text())
            description = self.description_input.text()
            category_id = self.category_combo.currentData()
            account_id = self.account_combo.currentData()
            date = self.date_input.date().toPyDate()
            transaction_type = self.type_combo.currentText()
            notes = self.notes_input.text()
            
            # Basic validation
            if not description or amount <= 0:
                QMessageBox.warning(self, "Invalid Input", "Please fill in all required fields correctly.")
                return
            
            if category_id is None:
                QMessageBox.warning(self, "Invalid Input", "Please select a category.")
                return
                
            if account_id is None:
                QMessageBox.warning(self, "Invalid Input", "Please select an account.")
                return
                
            print(f"Adding Transaction:")
            print(f"Amount: ${amount:.2f}")
            print(f"Description: {description}")
            print(f"Category ID: {category_id}")
            print(f"Account ID: {account_id}")
            print(f"Date: {date}")
            print(f"Type: {transaction_type}")
            print(f"Notes: {notes}")
                
            result = self.transaction_db_service.add_transaction(
                date, description, amount, category_id, transaction_type, account_id, notes
            )
            
            if result == 1:
                QMessageBox.information(self, "Success", "Transaction added successfully!")
                
                # Refresh the main window's transaction table if callback provided
                if self.refresh_callback:
                    self.refresh_callback()
                
                self.accept()
            else:
                QMessageBox.warning(self, "Error", "Failed to add transaction.")
                
        except ValueError:
            QMessageBox.warning(self, "Invalid Input", "Please enter a valid amount.")
        except Exception as e:
            print(f"Error adding transaction: {e}")
            QMessageBox.warning(self, "Error", f"An error occurred: {str(e)}") 