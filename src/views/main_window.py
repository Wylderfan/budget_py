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

class MainWindow(QMainWindow):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.popup_window = WindowManager()
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
        self.category_combo.addItems(["Income", "Food", "Transportation", "Entertainment", "Bills", "Other"])
        
        self.date_input = QDateEdit()
        self.date_input.setDate(QDate.currentDate())
        
        self.type_combo = QComboBox()
        self.type_combo.addItems(["Expense", "Income"])
        
        # Add form fields
        layout.addRow("Amount:", self.amount_input)
        layout.addRow("Description:", self.description_input)
        layout.addRow("Category:", self.category_combo)
        layout.addRow("Date:", self.date_input)
        layout.addRow("Type:", self.type_combo)
        
        # Add submit button
        submit_btn = QPushButton("Add Transaction")
        #submit_btn.clicked.connect(self.add_transaction)
        layout.addRow(submit_btn)
        
        widget.setLayout(layout)
        return widget
        
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
        self.summary_table.setColumnCount(4)
        self.summary_table.setHorizontalHeaderLabels(["Date", "Description", "Amount", "Category"])
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
            category = self.category_combo.currentText()
            date = self.date_input.date().toPyDate()
            transaction_type = self.type_combo.currentText()
            
            if not description or amount <= 0:
                QMessageBox.warning(self, "Error", "Please fill in all fields correctly.")
                return
                
            query = """
            INSERT INTO transactions (date, description, amount, category, type)
            VALUES (%s, %s, %s, %s, %s)
            """
            self.db.execute_query(query, (date, description, amount, category, transaction_type))
            
            # Clear inputs
            self.amount_input.clear()
            self.description_input.clear()
            
            QMessageBox.information(self, "Success", "Transaction added successfully!")
            
        except ValueError:
            QMessageBox.warning(self, "Error", "Please enter a valid amount.")
            
    def refresh_summary(self):
        query = "SELECT date, description, amount, category FROM transactions ORDER BY date DESC"
        results = self.db.execute_query(query)
        
        self.summary_table.setRowCount(len(results))
        for i, row in enumerate(results):
            for j, value in enumerate(row):
                item = QTableWidgetItem(str(value))
                self.summary_table.setItem(i, j, item) 

