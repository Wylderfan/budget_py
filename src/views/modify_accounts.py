from PyQt6.QtWidgets import (
    QDialog, QWidget, QTableWidget, QVBoxLayout, QHBoxLayout, QFormLayout, 
    QLineEdit, QPushButton, QComboBox, QDateEdit, QTableWidgetItem
)
from PyQt6.QtCore import QDate, Qt

from .popup_window import PopUpWindow
from .window_manager import WindowManager

from controllers.db.account_db_service import AccountDBService

from .add_accounts_window import AddAccountsWindow
from .del_accounts_window import DelAccountsWindow

class ModifyAccountsWindow(PopUpWindow):
    def __init__(self, window_name: str, min_width: int, min_height: int, db, parent=None) -> None:
        super().__init__(window_name, min_width, min_height, parent)

        self.db = db
        self.account_db_service = AccountDBService(self.db)

        self.popup_window = WindowManager()

        self.setup_ui()

        self.refresh_accounts()

    def setup_ui(self):
        layout = QVBoxLayout()

        self.summary_table = QTableWidget()
        self.summary_table.setColumnCount(3)
        self.summary_table.setHorizontalHeaderLabels(["Name", "Amount", "Category"])
        layout.addWidget(self.summary_table)

        # Add account button
        add_account_btn = QPushButton("Add")
        add_account_btn.clicked.connect(lambda: self.popup_window.open_window(AddAccountsWindow("Add Accounts", 300, 400, self.db)))
        layout.addWidget(add_account_btn)

        # Delete account button
        delete_account_btn = QPushButton("Delete")
        delete_account_btn.clicked.connect(lambda: self.popup_window.open_window(DelAccountsWindow("Delete Accounts", 300, 400, self.db)))
        layout.addWidget(delete_account_btn)
    
        # Refresh button
        refresh_btn = QPushButton("Refresh")
        refresh_btn.clicked.connect(self.refresh_accounts)
        layout.addWidget(refresh_btn)
       
        self.setLayout(layout)

    def refresh_accounts(self):
        try:
            accounts = self.account_db_service.search_all()
        except Exception as e:
            print("Error while refreshing accounts:")
            print(e)
            return
        
        self.summary_table.setRowCount(len(accounts)) # type: ignore

        for i, account in enumerate(accounts): # type: ignore
            name = QTableWidgetItem(str(account[1]))
            amount = QTableWidgetItem(f"${account[3]:.2f}")
            account_type = QTableWidgetItem(str(account[4]))

            self.summary_table.setItem(i, 0, name)
            self.summary_table.setItem(i, 1, amount)
            self.summary_table.setItem(i, 2, account_type)

        self.summary_table.resizeColumnsToContents()


