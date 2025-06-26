from PyQt6.QtWidgets import (
    QDialog, QWidget, QTableWidget, QVBoxLayout, QHBoxLayout, QFormLayout, 
    QLineEdit, QPushButton, QComboBox, QDateEdit, QLabel
)
from PyQt6.QtCore import QDate
from .popup_window import PopUpWindow

class AddDelAccountsWindow(PopUpWindow):
    def __init__(self, window_name: str, min_width: int, min_height: int, db, parent=None) -> None:
        super().__init__(window_name, min_width, min_height, parent)

        self.db = db

        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        self.summary_table = QTableWidget()
        self.summary_table.setColumnCount(4)
        self.summary_table.setHorizontalHeaderLabels(["Name", "Amount", "Category"])
        layout.addWidget(self.summary_table)

        # Add account button
        refresh_btn = QPushButton("Add")
        refresh_btn.clicked.connect(self.refresh_accounts)
        layout.addWidget(refresh_btn)

        # Delete account button
        refresh_btn = QPushButton("Delete")
        refresh_btn.clicked.connect(self.refresh_accounts)
        layout.addWidget(refresh_btn)
    
        # Refresh button
        refresh_btn = QPushButton("Refresh")
        refresh_btn.clicked.connect(self.refresh_accounts)
        layout.addWidget(refresh_btn)
       
        self.setLayout(layout)

    def refresh_accounts(self, db):
        print("Refreshing Accounts")

    def add_account(self, db):
        print("Adding an account")

    def delete_account(self, db):
        print("Delete an account")
 
