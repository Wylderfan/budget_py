from PyQt6.QtWidgets import (
    QLineEdit, QVBoxLayout, QPushButton, QFormLayout, 
    QComboBox, QHBoxLayout, QMessageBox, QLabel, QDateEdit
)
from PyQt6.QtCore import Qt, QDate
from views.common.popup_window import PopUpWindow

from controllers.db.categories_db_service import CategoriesDBService
from controllers.db.account_db_service import AccountDBService
from controllers.db.transaction_db_service import TransactionDBService

class AddTransactionsWindow(PopUpWindow):
    def __init__(self, window_name: str, min_width: int, min_height: int, db, parent=None) -> None:
        super().__init__(window_name, min_width, min_height, db, parent)

        self.categories_db_service = CategoriesDBService(self.get_db())
        self.accounts_db_service = AccountDBService(self.get_db())
        self.transaction_db_service = TransactionDBService(self.get_db())

        self.setup_ui()

    def setup_ui(self):
        main_layout = QVBoxLayout()
        
        title_label = QLabel("Add New Transaction")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title_label)
        
        form_layout = QFormLayout()
        
        self.amount_input = QLineEdit()
        self.amount_input.setPlaceholderText("0.00")
        form_layout.addRow("Amount ($):", self.amount_input)
        
        self.description_input = QLineEdit()
        self.description_input.setPlaceholderText("Description")
        form_layout.addRow("Description:", self.description_input)
        
        self.category_combo = QComboBox()
        self.load_categories()
        form_layout.addRow("Category:", self.category_combo)
        
        self.account_combo = QComboBox()
        self.load_accounts()
        form_layout.addRow("Account:", self.account_combo)
        
        self.date_input = QDateEdit()
        self.date_input.setDate(QDate.currentDate())
        form_layout.addRow("Date:", self.date_input)
        
        self.type_combo = QComboBox()
        self.type_combo.addItems(["Expense", "Income",])
        form_layout.addRow("Type:", self.type_combo)
        
        self.notes_input = QLineEdit()
        self.notes_input.setPlaceholderText("Notes (optional)")
        form_layout.addRow("Notes:", self.notes_input)
        
        main_layout.addLayout(form_layout)
        
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
                    self.category_combo.addItem(str(category[1]), category[0])
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
                    self.account_combo.addItem(str(account[1]), account[0])
        except Exception as e:
            print(f"Error loading accounts: {e}")
            QMessageBox.warning(self, "Error", "Could not load accounts from database.")
    
    def add_transaction(self):
        amount_text = self.amount_input.text().strip()
        description = self.description_input.text().strip()
        category_id = self.category_combo.currentData()
        account_id = self.account_combo.currentData()
        date = self.date_input.date().toPyDate()
        transaction_type = self.type_combo.currentText()
        notes = self.notes_input.text().strip()
        
        if not amount_text:
            QMessageBox.warning(self, "Invalid Input", "Please enter an amount.")
            return
            
        try:
            amount = round(float(amount_text), 2)
            if amount <= 0:
                QMessageBox.warning(self, "Invalid Input", "Amount must be greater than 0.")
                return
        except ValueError:
            QMessageBox.warning(self, "Invalid Input", "Please enter a valid number for amount.")
            return
        
        if not description:
            QMessageBox.warning(self, "Invalid Input", "Please enter a description.")
            return
            
        if len(description) > 255:
            QMessageBox.warning(self, "Invalid Input", "Description must be 255 characters or less.")
            return
        
        if len(notes) > 1000:
            QMessageBox.warning(self, "Invalid Input", "Notes must be 1000 characters or less.")
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
        
        try:
            transaction_result = self.transaction_db_service.add_transaction(
                date, description, amount, category_id, transaction_type, account_id, notes
            )
            account_result = self.accounts_db_service.add_transaction(account_id, amount if transaction_type == "Income" else -amount)
            
            if transaction_result == 1 and account_result == 1:
                QMessageBox.information(self, "Success", "Transaction added successfully and account was updated.")
                self.accept()
            elif transaction_result == 1:
                QMessageBox.warning(self, "Warning", "Transaction added successfully but account was not updated")
                self.accept()
            else:
                QMessageBox.warning(self, "Error", "Failed to add transaction.")

                
        except Exception as e:
            print(f"Error adding transaction: {e}")
            QMessageBox.warning(self, "Error", f"An error occurred: {str(e)}") 

