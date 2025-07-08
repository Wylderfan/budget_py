from PyQt6.QtWidgets import (
    QApplication, QDialog, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QTableWidget, QTableWidgetItem,
    QTabWidget, QLineEdit, QComboBox, QDateEdit,
    QMessageBox, QFormLayout
)
from PyQt6.QtCore import Qt, QDate
from datetime import datetime

from .window_manager import WindowManager
from .modify_accounts import ModifyAccountsWindow
from .modify_categories import ModifyCategoriesWindow

from controllers.db.categories_db_service import CategoriesDBService
from controllers.db.account_db_service import AccountDBService
from controllers.db.transaction_db_service import TransactionDBService

class MainWindow(QMainWindow):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.popup_window = WindowManager()
        
        # Initialize database services
        self.categories_db_service = CategoriesDBService(self.db)
        self.accounts_db_service = AccountDBService(self.db)
        self.transaction_db_service = TransactionDBService(self.db)
        
        self.setWindowTitle("Budget Tracker")
        self.setMinimumSize(800, 600)
        
        # Create central widget and main layout
        central_widget = QWidget()
        self.central_widget = central_widget
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Create tab widget
        tabs = QTabWidget()
        layout.addWidget(tabs)
        
        # Add tabs
        tabs.addTab(self.create_budget_tab(), "Budget")
        tabs.addTab(self.create_transaction_tab(), "Add Transaction")
        tabs.addTab(self.create_summary_tab(), "Summary")
        tabs.addTab(self.create_view_transactions_tab(), "View Transactions")
        tabs.addTab(self.create_reports_tab(), "Reports")

        # Add a quit button
        quit_button = QPushButton("Quit")
        quit_button.clicked.connect(QApplication.quit)
        layout.addWidget(quit_button)
        
        # Load initial data
        self.refresh_summary()
        
    def closeEvent(self, a0):
        if self.db:
            self.db.close()
        
        super().closeEvent(a0)
        
        # Make sure application exits
        QApplication.quit()       

    def create_budget_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Budget will be implemented here
        layout.addWidget(QLabel("Budget coming soon..."))

        modify_categories = QPushButton("Modify Categories")
        modify_categories.clicked.connect(lambda: self.popup_window.open_window(ModifyCategoriesWindow("Modify Categories", 300, 400, self.db)))
        layout.addWidget(modify_categories)       

        widget.setLayout(layout)
        return widget

    def create_transaction_tab(self):
        widget = QWidget()
        layout = QFormLayout()
        
        # Transaction form
        self.amount_input = QLineEdit()
        self.amount_input.setPlaceholderText("0.00")
        
        self.description_input = QLineEdit()
        self.description_input.setPlaceholderText("Description")
        
        self.category_combo = QComboBox()
        self.load_categories()
        
        self.account_combo = QComboBox()
        self.load_accounts()
        
        self.date_input = QDateEdit()
        self.date_input.setDate(QDate.currentDate())
        
        self.type_combo = QComboBox()
        self.type_combo.addItems(["Expense", "Income"])
        
        self.notes_input = QLineEdit()
        self.notes_input.setPlaceholderText("Notes (optional)")
        
        # Add form fields
        layout.addRow("Amount:", self.amount_input)
        layout.addRow("Description:", self.description_input)
        layout.addRow("Category:", self.category_combo)
        layout.addRow("Account:", self.account_combo)
        layout.addRow("Date:", self.date_input)
        layout.addRow("Type:", self.type_combo)
        layout.addRow("Notes:", self.notes_input)
        
        # Add submit button
        submit_btn = QPushButton("Add Transaction")
        submit_btn.clicked.connect(self.add_transaction)
        layout.addRow(submit_btn)
        
        widget.setLayout(layout)
        return widget

    def load_categories(self):
        """Load categories from database into combo box"""
        self.category_combo.clear()
        try:
            categories = self.categories_db_service.select_category_names()
            if categories and isinstance(categories, list):
                for category in categories:
                    # category is (name, id)
                    self.category_combo.addItem(str(category[0]), category[1])
        except Exception as e:
            print(f"Error loading categories: {e}")
            QMessageBox.warning(self, "Error", "Could not load categories from database.")

    def load_accounts(self):
        """Load accounts from database into combo box"""
        self.account_combo.clear()
        try:
            accounts = self.accounts_db_service.select_name_id_all_accounts()
            if accounts and isinstance(accounts, list):
                for account in accounts:
                    # account is (name, id)
                    self.account_combo.addItem(str(account[0]), account[1])
        except Exception as e:
            print(f"Error loading accounts: {e}")
            QMessageBox.warning(self, "Error", "Could not load accounts from database.")
        
    def create_summary_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()
        
        modify_accounts = QPushButton("Modify Accounts")
        modify_accounts.clicked.connect(lambda: self.popup_window.open_window(ModifyAccountsWindow("Modify Accounts", 300, 400, self.db)))
        layout.addWidget(modify_accounts)
        
        widget.setLayout(layout)
        return widget
 
    def create_view_transactions_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Summary table
        self.summary_table = QTableWidget()
        self.summary_table.setColumnCount(6)
        self.summary_table.setHorizontalHeaderLabels(["Date", "Description", "Amount", "Category", "Account", "Type"])
        layout.addWidget(self.summary_table)
        
        # Refresh button
        refresh_btn = QPushButton("Refresh")
        refresh_btn.clicked.connect(self.refresh_summary)
        layout.addWidget(refresh_btn)
        
        widget.setLayout(layout)
        return widget
        
    def create_reports_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Summary will be implemented here
        layout.addWidget(QLabel("Summary coming soon"))
        
        widget.setLayout(layout)
        return widget
       
    def add_transaction(self):
        try:
            amount = float(self.amount_input.text())
            description = self.description_input.text()
            category_id = self.category_combo.currentData()
            account_id = self.account_combo.currentData()
            date = self.date_input.date().toPyDate()
            transaction_type = self.type_combo.currentText()
            notes = self.notes_input.text()
            
            if not description or amount <= 0:
                QMessageBox.warning(self, "Error", "Please fill in all required fields correctly.")
                return
            
            if category_id is None:
                QMessageBox.warning(self, "Error", "Please select a category.")
                return
                
            if account_id is None:
                QMessageBox.warning(self, "Error", "Please select an account.")
                return
                
            result = self.transaction_db_service.add_transaction(
                date, description, amount, category_id, transaction_type, account_id, notes
            )
            
            if result == 1:
                # Clear inputs
                self.amount_input.clear()
                self.description_input.clear()
                self.notes_input.clear()
                self.date_input.setDate(QDate.currentDate())
                
                QMessageBox.information(self, "Success", "Transaction added successfully!")
                # Refresh the view transactions table
                self.refresh_summary()
            else:
                QMessageBox.warning(self, "Error", "Failed to add transaction.")
                
        except ValueError:
            QMessageBox.warning(self, "Error", "Please enter a valid amount.")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"An error occurred: {str(e)}")
            
    def refresh_summary(self):
        try:
            results = self.transaction_db_service.search_all()
            
            if results and isinstance(results, list):
                self.summary_table.setRowCount(len(results))
                for i, row in enumerate(results):
                    for j, value in enumerate(row):
                        # Format amount with currency symbol
                        if j == 2 and isinstance(value, (int, float, str)):  # Amount column
                            try:
                                item = QTableWidgetItem(f"${float(value):.2f}")
                            except (ValueError, TypeError):
                                item = QTableWidgetItem(str(value))
                        else:
                            item = QTableWidgetItem(str(value))
                        self.summary_table.setItem(i, j, item)
                        
                self.summary_table.resizeColumnsToContents()
            else:
                self.summary_table.setRowCount(0)
        except Exception as e:
            print(f"Error refreshing transactions: {e}")
            QMessageBox.warning(self, "Error", "Could not refresh transactions.") 

