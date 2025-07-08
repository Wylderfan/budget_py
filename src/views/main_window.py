from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QTableWidget, QTableWidgetItem,
    QTabWidget, QMessageBox
)

from views.add_accounts_window import AddAccountsWindow
from views.del_accounts_window import DelAccountsWindow

from .window_manager import WindowManager
from .modify_categories import ModifyCategoriesWindow
from .del_transactions_window import DelTransactionsWindow
from .add_transactions_window import AddTransactionsWindow

from controllers.db.transaction_db_service import TransactionDBService
from controllers.db.account_db_service import AccountDBService

class MainWindow(QMainWindow):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.popup_window = WindowManager()
        
        # Initialize database services
        self.transaction_db_service = TransactionDBService(self.db)
        self.account_db_service = AccountDBService(self.db)
        
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
        self.refresh_accounts()
        
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
        
        # Summary table
        self.account_summary_table = QTableWidget()
        self.account_summary_table.setColumnCount(3)
        self.account_summary_table.setHorizontalHeaderLabels(["Name", "Amount", "Type"])
        layout.addWidget(self.account_summary_table)

        button_layout = QHBoxLayout()

        # Refresh button
        refresh_btn = QPushButton("Refresh")
        refresh_btn.clicked.connect(self.refresh_accounts)
        button_layout.addWidget(refresh_btn)
 
        # Add account button
        add_account_btn = QPushButton("Add")
        add_account_btn.clicked.connect(lambda: self.popup_window.open_window(AddAccountsWindow("Add Accounts", 300, 400, self.db)))
        layout.addWidget(add_account_btn)

        # Delete account button
        delete_account_btn = QPushButton("Delete")
        delete_account_btn.clicked.connect(lambda: self.popup_window.open_window(DelAccountsWindow("Delete Accounts", 300, 400, self.db)))
        layout.addWidget(delete_account_btn)

        layout.addLayout(button_layout)
        
        widget.setLayout(layout)
        return widget
 
    def create_view_transactions_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Summary table
        self.transaction_summary_table = QTableWidget()
        self.transaction_summary_table.setColumnCount(6)
        self.transaction_summary_table.setHorizontalHeaderLabels(["Date", "Description", "Amount", "Category", "Account", "Type"])
        layout.addWidget(self.transaction_summary_table)
        
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
                self.transaction_summary_table.setRowCount(len(results))
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
                        self.transaction_summary_table.setItem(i, j, item)
                        
                self.transaction_summary_table.resizeColumnsToContents()
            else:
                self.transaction_summary_table.setRowCount(0)
        except Exception as e:
            print(f"Error refreshing transactions: {e}")
            QMessageBox.warning(self, "Error", "Could not refresh transactions.") 

    def refresh_accounts(self):
        try:
            accounts = self.account_db_service.search_all()
        except Exception as e:
            print("Error while refreshing accounts:")
            print(e)
            return
        
        self.account_summary_table.setRowCount(len(accounts)) # type: ignore

        for i, account in enumerate(accounts): # type: ignore
            name = QTableWidgetItem(str(account[1]))
            amount = QTableWidgetItem(f"${account[3]:.2f}")
            account_type = QTableWidgetItem(str(account[4]))

            self.account_summary_table.setItem(i, 0, name)
            self.account_summary_table.setItem(i, 1, amount)
            self.account_summary_table.setItem(i, 2, account_type)

        self.account_summary_table.resizeColumnsToContents()

