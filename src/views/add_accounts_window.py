from PyQt6.QtWidgets import (
    QLineEdit, QVBoxLayout, QPushButton, QFormLayout, 
    QComboBox, QHBoxLayout, QMessageBox, QLabel
)
from PyQt6.QtCore import Qt
from views.popup_window import PopUpWindow

from controllers.db.account_db_service import AccountDBService

class AddAccountsWindow(PopUpWindow):
    def __init__(self, window_name: str, min_width: int, min_height: int, db, parent=None) -> None:
        super().__init__(window_name, min_width, min_height, parent)

        self.account_db_service = AccountDBService(db)

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
        self.account_type_combo.addItems([
            "Chequing",
            "Savings", 
            "Credit Card",
            "Line of Credit"
        ])
        form_layout.addRow("Account Type:", self.account_type_combo)
        
        main_layout.addLayout(form_layout)
        
        # Buttons layout
        button_layout = QHBoxLayout()
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setAutoDefault(False)
        cancel_btn.clicked.connect(self.reject)
        
        add_account_btn = QPushButton("Add Account")
        add_account_btn.clicked.connect(self.add_account)
        
        button_layout.addWidget(cancel_btn)
        button_layout.addWidget(add_account_btn)
        
        main_layout.addLayout(button_layout)
        
        self.setLayout(main_layout)
    
    def add_account(self):
        account_name = self.name_input.text()
        balance = round(float(self.balance_input.text()), 2)
        account_type = self.account_type_combo.currentText()
        
        # Basic validation
        if not account_name:
            QMessageBox.warning(self, "Invalid Input", "Please enter an account name.")
            return
        
        try:
            starting_balance = float(balance) if balance else 0.0
        except ValueError:
            QMessageBox.warning(self, "Invalid Input", "Please enter a valid number for starting balance.")
            return
        
        print(f"Adding Account:")
        print(f"  Name: {account_name}")
        print(f"  Starting Balance: ${starting_balance:.2f}")
        print(f"  Account Type: {account_type}")

        self.account_db_service.add_account(account_name, balance, account_type)

        self.accept()
