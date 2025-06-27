from PyQt6.QtWidgets import (
    QLineEdit, QVBoxLayout, QPushButton, QFormLayout, 
    QComboBox, QHBoxLayout, QMessageBox, QLabel
)
from PyQt6.QtCore import Qt
from views.popup_window import PopUpWindow

class AddAccountsWindow(PopUpWindow):
    def __init__(self, window_name: str, min_width: int, min_height: int, db, parent=None) -> None:
        super().__init__(window_name, min_width, min_height, parent)

        self.db = db

        self.setup_ui()

    def setup_ui(self):
        # Main layout
        main_layout = QVBoxLayout()
        
        # Title
        title_label = QLabel("Add New Account")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title_label)
        
        # Form layout for inputs
        form_layout = QFormLayout()
        
        # Account name input
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Enter account name")
        form_layout.addRow("Account Name:", self.name_input)
        
        # Starting balance input
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
        
        # Cancel button
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setAutoDefault(False)
        cancel_btn.clicked.connect(self.reject)
        
        # Add account button
        add_account_btn = QPushButton("Add Account")
        add_account_btn.clicked.connect(self.add_account)
        
        button_layout.addWidget(cancel_btn)
        button_layout.addWidget(add_account_btn)
        
        main_layout.addLayout(button_layout)
        
        self.setLayout(main_layout)
    
    def add_account(self):
        """Handle adding the account"""
        # Get the form data
        account_name = self.name_input.text().strip()
        balance_text = self.balance_input.text().strip()
        account_type = self.account_type_combo.currentText()
        
        # Basic validation
        if not account_name:
            QMessageBox.warning(self, "Invalid Input", "Please enter an account name.")
            return
        
        # Validate balance
        try:
            starting_balance = float(balance_text) if balance_text else 0.0
        except ValueError:
            QMessageBox.warning(self, "Invalid Input", "Please enter a valid number for starting balance.")
            return
        
        # Print the collected data
        print(f"Adding Account:")
        print(f"  Name: {account_name}")
        print(f"  Starting Balance: ${starting_balance:.2f}")
        print(f"  Account Type: {account_type}")
        
        # Close the dialog
        self.accept()
