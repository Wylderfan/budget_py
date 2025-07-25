from PyQt6.QtWidgets import (
    QLineEdit, QVBoxLayout, QPushButton, QFormLayout, 
    QComboBox, QHBoxLayout, QMessageBox, QLabel
)
from PyQt6.QtCore import Qt
from views.popup_window import PopUpWindow

from controllers.db.account_db_service import AccountDBService
from config.config_loader import ConfigLoader

class AddAccountsWindow(PopUpWindow):
    def __init__(self, window_name: str, min_width: int, min_height: int, db, parent=None) -> None:
        super().__init__(window_name, min_width, min_height, db, parent)

        self.account_db_service = AccountDBService(self.get_db())
        self.json_config_loader = ConfigLoader()

        self.setup_ui()

    def setup_ui(self):
        main_layout = QVBoxLayout()
        
        title_label = QLabel("Add New Account")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title_label)
        
        # Form layout for inputs
        form_layout = QFormLayout()
        
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Enter account name")
        form_layout.addRow("Account Name:", self.name_input)
        
        self.balance_input = QLineEdit()
        self.balance_input.setPlaceholderText("0.00")
        form_layout.addRow("Starting Balance ($):", self.balance_input)
        
        # Account type dropdown
        self.account_type_combo = QComboBox()
        account_types = self.json_config_loader.get_account_types()
        self.account_type_combo.addItems(account_types)
        form_layout.addRow("Account Type:", self.account_type_combo)
        
        main_layout.addLayout(form_layout)
        
        # Buttons layout
        button_layout = QHBoxLayout()
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setAutoDefault(False) # Needed for highlighting the submit button instead
        cancel_btn.clicked.connect(self.reject)
        
        add_account_btn = QPushButton("Add Account")
        add_account_btn.clicked.connect(self.add_account)
        
        button_layout.addWidget(cancel_btn)
        button_layout.addWidget(add_account_btn)
        
        main_layout.addLayout(button_layout)
        
        self.setLayout(main_layout)
    
    def add_account(self):
        account_name = self.name_input.text().strip()
        balance_text = self.balance_input.text().strip()
        account_type = self.account_type_combo.currentText()

        # Validate account name
        if not account_name:
            QMessageBox.warning(self, "Invalid Input", "Please enter an account name.")
            return
        
        if len(account_name) > 45:
            QMessageBox.warning(self, "Invalid Input", "Account name must be 45 characters or less.")
            return
        
        # Validate and convert balance
        try:
            if not balance_text:
                balance = 0.0
            else:
                balance = round(float(balance_text), 2)
        except ValueError:
            QMessageBox.warning(self, "Invalid Input", "Please enter a valid number for starting balance.")
            return
        
        print(f"Adding Account:")
        print(f"Name: {account_name}")
        print(f"Starting Balance: ${balance:.2f}")
        print(f"Account Type: {account_type}")

        try:
            result = self.account_db_service.add_account(account_name, balance, account_type)
            if result == 1:
                QMessageBox.information(self, "Success", "Account added successfully!")
                self.accept()
            else:
                QMessageBox.warning(self, "Error", "Failed to add account.")
        except Exception as e:
            print(f"Error adding account: {e}")
            QMessageBox.warning(self, "Error", f"An error occurred: {str(e)}")
