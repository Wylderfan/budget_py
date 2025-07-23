from PyQt6.QtWidgets import QCheckBox, QComboBox, QFormLayout, QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QMessageBox
from PyQt6.QtCore import Qt

from controllers.db.account_db_service import AccountDBService
from controllers.db.transaction_db_service import TransactionDBService
from views.popup_window import PopUpWindow

class DelAccountsWindow(PopUpWindow):
    def __init__(self, window_name: str, min_width: int, min_height: int, db, parent=None) -> None:
        super().__init__(window_name, min_width, min_height, db, parent)

        self.account_db_service = AccountDBService(self.get_db())
        self.transaction_db_service = TransactionDBService(self.get_db())

        self.setup_ui()

    def setup_ui(self):
        main_layout = QVBoxLayout()

        title_lable = QLabel("Delete Accounts")
        title_lable.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title_lable)

        form_layout = QFormLayout()

        self.select_account_combo = QComboBox()
        accounts = self.account_db_service.select_name_id_all_accounts() # name , id tuple
        self.account_names = [row[1] for row in accounts] # type: ignore
        self.account_ids = [row[0] for row in accounts] # type: ignore
        self.select_account_combo.addItems(self.account_names) # type: ignore
        form_layout.addRow("Select Account:", self.select_account_combo)

        self.transfer_checkbox = QCheckBox()
        form_layout.addRow("Transfer transactions to separate account:", self.transfer_checkbox)

        self.select_transfer_combo = QComboBox()
        self.select_transfer_combo.addItems(self.account_names) # type: ignore
        form_layout.addRow("Select account to transfer too:", self.select_transfer_combo)

        main_layout.addLayout(form_layout)

        button_layout = QHBoxLayout()
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setAutoDefault(False)
        cancel_btn.clicked.connect(self.reject)
        
        del_account_btn = QPushButton("Delete Account")
        del_account_btn.clicked.connect(self.del_account)
        
        button_layout.addWidget(cancel_btn)
        button_layout.addWidget(del_account_btn)
        
        main_layout.addLayout(button_layout)
        
        self.setLayout(main_layout)

    def id_from_name(self, name):
        id = self.account_db_service.search_account(name=name)
        if len(id) == 1: # type: ignore
            return id[0][0] # type: ignore
        else:
            print("Multiple entries of the same name")
            return None
        
    def del_account(self):
        selected_account = self.select_account_combo.currentText()
        is_transfer = True if self.transfer_checkbox.checkState() == Qt.CheckState.Checked else False
        transfer_account = self.select_transfer_combo.currentText() if is_transfer else None

        if not selected_account:
            QMessageBox.warning(self, "Error", "No account selected.")
            return

        # Create confirmation message
        confirmation_msg = f"Are you sure you want to delete this account?\n\nAccount: {selected_account}"
        if is_transfer and transfer_account and transfer_account != selected_account:
            confirmation_msg += f"\n\nAll transactions will be transferred to: {transfer_account}"
        elif is_transfer:
            QMessageBox.warning(self, "Error", "Cannot transfer to the same account being deleted.")
            return
        else:
            confirmation_msg += "\n\nWarning: All transactions in this account will be permanently deleted!"

        # Verification dialog
        reply = QMessageBox.question(
            self,
            "Confirm Account Deletion",
            confirmation_msg,
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )

        if reply != QMessageBox.StandardButton.Yes:
            return

        print(f"Deleting Account:")
        print(f"Name: {selected_account}")

        if is_transfer and transfer_account and transfer_account != selected_account:
            print(f"Transferring transactions to: {transfer_account}")
            transfer_result = self.account_db_service.transfer_transactions(self.id_from_name(selected_account), self.id_from_name(transfer_account))
            print(f"Transactions moved: {transfer_result}")
        else:
            print("Deleting transactions from selected account")
            try:
                del_transactions_result = self.transaction_db_service.del_account_transactions(self.account_db_service.search_account(name=selected_account))
                print(f"Result of Account wide deletion of transactions: {del_transactions_result}")
            except Exception as e:
                print(f"Error deleting transactions from {selected_account}")

        try:
            account_id = self.id_from_name(selected_account)
            if account_id is None:
                QMessageBox.warning(self, "Error", "Could not find account to delete.")
                return
                
            result = self.account_db_service.del_account(account_id)
            if result == 1:
                QMessageBox.information(self, "Success", "Account deleted successfully!")
            else:
                QMessageBox.warning(self, "Error", "Failed to delete account.")
        except Exception as e:
            print(f"Error Deleting Account:\n{e}")
            QMessageBox.warning(self, "Error", f"An error occurred while deleting: {str(e)}")

        self.accept()

