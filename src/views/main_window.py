from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QTableWidget, QTableWidgetItem,
    QTabWidget, QMessageBox
)
from PyQt6.QtCore import Qt

from .window_manager import WindowManager
from .modify_accounts import ModifyAccountsWindow
from .modify_categories import ModifyCategoriesWindow
from .del_transactions_window import DelTransactionsWindow
from .add_transactions_window import AddTransactionsWindow

from controllers.db.transaction_db_service import TransactionDBService

class MainWindow(QMainWindow):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.popup_window = WindowManager()
        
        # Initialize database services
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
        tabs.addTab(self.create_view_transactions_tab(), "View Transactions")
        tabs.addTab(self.create_summary_tab(), "Summary")
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
        
        # Button layout for add, refresh and delete
        button_layout = QHBoxLayout()
        
        # Add Transaction button
        add_btn = QPushButton("Add Transaction")
        add_btn.clicked.connect(lambda: self.popup_window.open_window(AddTransactionsWindow("Add Transaction", 400, 500, self.db, refresh_callback=self.refresh_summary)))
        button_layout.addWidget(add_btn)
        
        # Refresh button
        refresh_btn = QPushButton("Refresh")
        refresh_btn.clicked.connect(self.refresh_summary)
        button_layout.addWidget(refresh_btn)
        
        # Delete button
        delete_btn = QPushButton("Delete Transaction")
        delete_btn.clicked.connect(lambda: self.popup_window.open_window(DelTransactionsWindow("Delete Transactions", 400, 500, self.db, refresh_callback=self.refresh_summary)))
        button_layout.addWidget(delete_btn)
        
        layout.addLayout(button_layout)
        
        widget.setLayout(layout)
        return widget
        
    def create_reports_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Summary will be implemented here
        layout.addWidget(QLabel("Summary coming soon"))
        
        widget.setLayout(layout)
        return widget
       

            
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

