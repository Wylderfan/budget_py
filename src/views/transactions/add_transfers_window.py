from PyQt6.QtWidgets import (
    QLineEdit, QVBoxLayout, QPushButton, QFormLayout, 
    QComboBox, QHBoxLayout, QMessageBox, QLabel, QDateEdit
)
from PyQt6.QtCore import Qt, QDate
from views.common.popup_window import PopUpWindow

from controllers.db.categories_db_service import CategoriesDBService
from controllers.db.account_db_service import AccountDBService
from controllers.db.transaction_db_service import TransactionDBService

class AddTransfersWindow(PopUpWindow):
    def __init__(self, window_name: str, min_width: int, min_height: int, db, parent=None) -> None:
        super().__init__(window_name, min_width, min_height, db, parent)
        
        self.categories_db_service = CategoriesDBService(self.get_db())
        self.accounts_db_service = AccountDBService(self.get_db())
        self.transaction_db_service = TransactionDBService(self.get_db())

        self.setup_ui()

    def setup_ui(self):
        main_layout = QVBoxLayout()
        
        title_label = QLabel("Add New Transfer")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title_label)
        
        form_layout = QFormLayout()
        
        self.amount_input = QLineEdit()
        self.amount_input.setPlaceholderText("0.00")
        form_layout.addRow("Amount ($):", self.amount_input)
        
        self.from_account_combo = QComboBox()
        self.to_account_combo = QComboBox()
        self.load_accounts()
        form_layout.addRow("From:", self.from_account_combo)
        form_layout.addRow("To:", self.to_account_combo)

        self.date_input = QDateEdit()
        self.date_input.setDate(QDate.currentDate())
        form_layout.addRow("Date:", self.date_input)

        self.notes_input = QLineEdit()
        self.notes_input.setPlaceholderText("Notes (optional)")
        form_layout.addRow("Notes:", self.notes_input)
        
        main_layout.addLayout(form_layout)
        
        # Buttons layout
        button_layout = QHBoxLayout()
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setAutoDefault(False)
        cancel_btn.clicked.connect(self.reject)
        
        add_transfer_btn = QPushButton("Add Transfer")
        add_transfer_btn.clicked.connect(self.add_transfer)
        
        button_layout.addWidget(cancel_btn)
        button_layout.addWidget(add_transfer_btn)
        
        main_layout.addLayout(button_layout)
        
        self.setLayout(main_layout)

    def load_accounts(self):
        """Load accounts from database into combo box"""
        self.to_account_combo.clear()
        self.from_account_combo.clear()
        try:
            accounts = self.accounts_db_service.select_name_id_all_accounts()
            if accounts and isinstance(accounts, list):
                for account in accounts:
                    # account is (name, id)
                    self.to_account_combo.addItem(str(account[1]), account[0])
                offset_accounts = accounts[1:] + accounts[0:1]
                for account in offset_accounts:    
                    self.from_account_combo.addItem(str(account[1]), account[0])
        except Exception as e:
            print(f"Error loading accounts: {e}")
            QMessageBox.warning(self, "Error", "Could not load accounts from database.")

    def add_transfer(self):
        amount_text = self.amount_input.text().strip()
        from_account_id = self.from_account_combo.currentData()
        to_account_id = self.to_account_combo.currentData()
        date = self.date_input.date().toPyDate()
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
        
        if len(notes) > 1000:
            QMessageBox.warning(self, "Invalid Input", "Notes must be 1000 characters or less.")
            return
        
        if from_account_id is None:
            QMessageBox.warning(self, "Invalid Input", "Please select a 'To:' account.")
            return

        if to_account_id is None:
            QMessageBox.warning(self, "Invalid Input", "Please select a 'From:' account.")
            return

        if to_account_id == from_account_id:
            QMessageBox.warning(self, "Invalid Input", "Please select a 'To:' account that is not the same as the 'From' account.")
            return
            
        print(f"Adding Transfer:")
        print(f"Amount: ${amount:.2f}")
        print(f"From Account ID: {from_account_id}")
        print(f"To Account ID: {to_account_id}")
        print(f"Date: {date}")
        print(f"Notes: {notes}")
        
        try:
            transfer_result = self.transaction_db_service.add_transfer(
                date,  amount, from_account_id, to_account_id, notes
            )
            account_result = self.accounts_db_service.add_transfer(from_account_id, to_account_id, amount)
            
            if transfer_result == 1 and account_result == 2:
                QMessageBox.information(self, "Success", "Transfer added successfully and both accounts were updated.")
                self.accept()
            elif transfer_result == 1:
                QMessageBox.warning(self, "Warning", "Transfer added successfully but accounts were not updated")
                self.accept()
            else:
                QMessageBox.warning(self, "Error", "Failed to add transfer.")

                
        except Exception as e:
            print(f"Error adding transfer: {e}")
            QMessageBox.warning(self, "Error", f"An error occurred: {str(e)}") 

