from PyQt6.QtWidgets import QComboBox, QFormLayout, QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QDateEdit, QMessageBox
from PyQt6.QtCore import Qt, QDate

from views.common.popup_window import PopUpWindow
from controllers.db.transaction_db_service import TransactionDBService
from utils.number_formatter import NumberFormatter

class DelTransactionsWindow(PopUpWindow):
    def __init__(self, window_name: str, min_width: int, min_height: int, db, parent=None, refresh_callback=None) -> None:
        super().__init__(window_name, min_width, min_height, db, parent)
        self.refresh_callback = refresh_callback

        self.transaction_db_service = TransactionDBService(self.get_db())

        self.setup_ui()
        self.load_transactions()

    def setup_ui(self):
        main_layout = QVBoxLayout()

        title_label = QLabel("Delete Transactions")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title_label)

        form_layout = QFormLayout()

        # Date range selection
        self.start_date_input = QDateEdit()
        self.start_date_input.setDate(QDate.currentDate().addDays(-30))  # Default to last 30 days
        self.start_date_input.setCurrentSection(QDateEdit.Section.DaySection)
        form_layout.addRow("Start Date:", self.start_date_input)

        self.end_date_input = QDateEdit()
        self.end_date_input.setDate(QDate.currentDate())
        self.end_date_input.setCurrentSection(QDateEdit.Section.DaySection)
        form_layout.addRow("End Date:", self.end_date_input)

        # Update button
        update_btn = QPushButton("Update Transactions")
        update_btn.clicked.connect(self.load_transactions)
        form_layout.addRow("", update_btn)

        # Transaction selection
        self.select_transaction_combo = QComboBox()
        form_layout.addRow("Select Transaction:", self.select_transaction_combo)

        main_layout.addLayout(form_layout)

        button_layout = QHBoxLayout()
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setAutoDefault(False)
        cancel_btn.clicked.connect(self.reject)
        
        del_transaction_btn = QPushButton("Delete Transaction")
        del_transaction_btn.clicked.connect(self.del_transaction)
        
        button_layout.addWidget(cancel_btn)
        button_layout.addWidget(del_transaction_btn)
        
        main_layout.addLayout(button_layout)
        
        self.setLayout(main_layout)

    def load_transactions(self):
        """Load transactions based on date range"""
        try:
            start_date = self.start_date_input.date().toPyDate()
            end_date = self.end_date_input.date().toPyDate()
            
            self.select_transaction_combo.clear()
            
            transactions = self.transaction_db_service.search_for_deletion(start_date, end_date)
            
            if transactions and isinstance(transactions, list):
                for transaction in transactions:
                    # transaction format: [id, date, description, amount, category_name, account_name, type]
                    transaction_id = transaction[0]
                    date = transaction[1]
                    description = transaction[2]
                    amount = transaction[3]
                    category = transaction[4]
                    account = transaction[5]
                    transaction_type = transaction[6]
                    
                    # Create display text for combo box
                    amount_str = NumberFormatter.safe_format_table_amount(amount)
                    display_text = f"{date} - {description} - {amount_str} ({category} - {account})"
                    
                    # Add item with transaction ID as data
                    self.select_transaction_combo.addItem(display_text, transaction_id)
            
            if self.select_transaction_combo.count() == 0:
                self.select_transaction_combo.addItem("No transactions found for this date range")
                
        except Exception as e:
            print(f"Error loading transactions: {e}")
            QMessageBox.warning(self, "Error", "Could not load transactions.")

    def del_transaction(self):
        if self.select_transaction_combo.count() == 0 or self.select_transaction_combo.currentData() is None:
            QMessageBox.warning(self, "Error", "No transaction selected or no transactions available.")
            return

        selected_transaction_text = self.select_transaction_combo.currentText()
        transaction_id = self.select_transaction_combo.currentData()

        # Confirmation dialog
        reply = QMessageBox.question(
            self, 
            "Confirm Deletion", 
            f"Are you sure you want to delete this transaction?\n\n{selected_transaction_text}",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )

        if reply != QMessageBox.StandardButton.Yes:
            return

        try:
            result = self.transaction_db_service.del_transaction(transaction_id)
            if result == 1:
                QMessageBox.information(self, "Success", "Transaction deleted successfully!")
                self.load_transactions()  # Refresh the list
                if self.refresh_callback:
                    self.refresh_callback()  # Refresh the main window's table
            else:
                QMessageBox.warning(self, "Error", "Failed to delete transaction.")
        except Exception as e:
            print(f"Error deleting transaction: {e}")
            QMessageBox.warning(self, "Error", f"An error occurred while deleting: {str(e)}")

        self.accept() 