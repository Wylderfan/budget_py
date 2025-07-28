from PyQt6.QtWidgets import QComboBox, QFormLayout, QHBoxLayout, QLabel, QLineEdit, QMessageBox, QPushButton, QVBoxLayout
from controllers.db.account_db_service import AccountDBService
from controllers.db.categories_db_service import CategoriesDBService
from views.common.popup_window import PopUpWindow


class SettingsWindow(PopUpWindow):
    def __init__(self, window_name: str, min_width: int, min_height: int, db, parent=None) -> None:
        super().__init__(window_name, min_width, min_height, db, parent)

        self.db = db
        self.accounts_db_service = AccountDBService(self.db)
        self.categories_db_service = CategoriesDBService(self.db)

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

        budget_layout = QHBoxLayout()

        budget_goal_label = QLabel("Change Budget goal:")

        self.category_combo = QComboBox()
        self.load_categories()
        
        self.new_goal_input = QLineEdit()
        self.new_goal_input.setPlaceholderText("$")

        self.modify_goal_btn = QPushButton("Modify Goal")
        self.modify_goal_btn.clicked.connect(self.modify_goal)

        budget_layout.addWidget(budget_goal_label)
        budget_layout.addWidget(self.category_combo)
        budget_layout.addWidget(self.new_goal_input)
        budget_layout.addWidget(self.modify_goal_btn)

        layout.addLayout(account_layout)
        layout.addLayout(budget_layout)

        self.setLayout(layout)

    def modify_account_value(self):
        selected_account_name = self.account_value_combo.currentText()
        amount_text = self.account_value_input.text().strip()
        
        # Validate account selection
        if not selected_account_name:
            QMessageBox.warning(self, "Invalid Input", "Please select an account.")
            return
            
        # Validate amount input
        if not amount_text:
            QMessageBox.warning(self, "Invalid Input", "Please enter an amount.")
            return
            
        try:
            amount = round(float(amount_text), 2)
        except ValueError:
            QMessageBox.warning(self, "Invalid Input", "Please enter a valid number for the amount.")
            return
        
        try:
            account = self.accounts_db_service.search_account(name=selected_account_name)
            if not account or not isinstance(account, list) or len(account) == 0:
                QMessageBox.warning(self, "Error", "Account not found.")
                return
                
            account_id = account[0][0]
            print(f"Modifying account ID: {account_id} with amount: ${amount:.2f}")
            
            result = self.accounts_db_service.modify_balance(account_id, amount)
            if result == 1:
                QMessageBox.information(self, "Success", "Account balance updated successfully!")
                self.account_value_input.clear()
            else:
                QMessageBox.warning(self, "Error", "Failed to update account balance.")
                
        except Exception as e:
            print(f"Error modifying account: {e}")
            QMessageBox.warning(self, "Error", f"An error occurred: {str(e)}")

    def load_accounts(self):
        self.account_value_combo.clear()
        try:
            accounts = self.accounts_db_service.select_name_id_all_accounts()
            if accounts and isinstance(accounts, list):
                for account in accounts:
                    self.account_value_combo.addItem(str(account[1]), account[0])
        except Exception as e:
            print(f"Error loading accounts: {e}")
            QMessageBox.warning(self, "Error", "Could not load accounts from database.")

    def load_categories(self):
        self.category_combo.clear()
        try:
            categories = self.categories_db_service.select_category_names()
            if categories and isinstance(categories, list):
                for category in categories:
                    self.category_combo.addItem(str(category[1]), category[0])
        except Exception as e:
            print(f"Error loading categories: {e}")
            QMessageBox.warning(self, "Error", "Could not load categories from database.")

    def modify_goal(self):
        category_id = self.category_combo.currentData()
        new_goal = self.new_goal_input.text().strip()

        try:
            amount = round(float(new_goal), 2)
            if amount <= 0:
                QMessageBox.warning(self, "Invalid input", "Amount must be greater than 0")
                return
        except ValueError as e:
            print(f"Error modifying goal: {e}")
            return

        if not category_id:
            print("Error: No category_id")
            return

        try:
            new_goal_result = self.categories_db_service.modify_goal(category_id, amount)
            if new_goal_result == 1:
                QMessageBox.information(self, "Success", "New goal updated")
                self.accept()
            else:
                QMessageBox.warning(self, "Error", "Failed to update goal")
        except Exception as e:
            print(f"Error modifying goal: {e}")

