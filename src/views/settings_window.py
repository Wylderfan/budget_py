from PyQt6.QtWidgets import QComboBox, QFormLayout, QLabel, QLineEdit, QMessageBox, QPushButton, QVBoxLayout
from controllers.db.account_db_service import AccountDBService
from views.popup_window import PopUpWindow


class SettingsWindow(PopUpWindow):
    def __init__(self, window_name: str, min_width: int, min_height: int, db, parent=None) -> None:
        super().__init__(window_name, min_width, min_height, db, parent)

        self.db = db
        self.accounts_db_service = AccountDBService(self.db)

        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        change_account_label = QLabel("Modify Accounts")
        layout.addWidget(change_account_label)

        account_layout = QFormLayout()

        self.account_value_combo = QComboBox()
        self.load_accounts()

        self.account_value_input = QLineEdit()
        self.account_value_input.setPlaceholderText("0.00")

        account_layout.addRow("Modify Hardcoded Account", self.account_value_combo) # type: ignore

        account_layout.addRow("Value:", self.account_value_input)

        self.modify_value_button = QPushButton("Modify Account Value")
        self.modify_value_button.clicked.connect(self.modify_account_value) # type: ignore
        account_layout.addRow(self.modify_value_button)

        layout.addLayout(account_layout)

        self.setLayout(layout)

    def modify_account_value(self):
        account = self.accounts_db_service.search_account(name=self.account_value_combo.currentText())
        id = account[0][0] # type: ignore
        print(f"this is the id: {id}")
        amount = self.account_value_input.text()

        return self.accounts_db_service.modify_balance(id, amount)

    def load_accounts(self):
        self.account_value_combo.clear()
        try:
            accounts = self.accounts_db_service.select_name_id_all_accounts()
            if accounts and isinstance(accounts, list):
                for account in accounts:
                    # account is (name, id)
                    self.account_value_combo.addItem(str(account[0]), account[1])
        except Exception as e:
            print(f"Error loading accounts: {e}")
            QMessageBox.warning(self, "Error", "Could not load accounts from database.")

