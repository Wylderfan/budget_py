from datetime import datetime

from PyQt6.QtWidgets import (
    QApplication, QComboBox, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QTableWidget, QTableWidgetItem,
    QTabWidget, QMessageBox
)

from views.add_accounts_window import AddAccountsWindow
from views.del_accounts_window import DelAccountsWindow

from .window_manager import WindowManager
from .settings_window import SettingsWindow
from .modify_categories import ModifyCategoriesWindow
from .del_transactions_window import DelTransactionsWindow
from .add_transactions_window import AddTransactionsWindow

from controllers.db.budget_db_service import BudgetDBService
from controllers.db.transaction_db_service import TransactionDBService
from controllers.db.account_db_service import AccountDBService

class MainWindow(QMainWindow):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.popup_window = WindowManager()

        # Initialize database services
        self.budget_db_service = BudgetDBService(self.db)
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

        button_layout = QHBoxLayout(central_widget)
        settings_button = QPushButton("Settings")
        settings_button.clicked.connect(self.handle_settings)
        button_layout.addWidget(settings_button)

        quit_button = QPushButton("Quit")
        quit_button.clicked.connect(QApplication.quit)
        button_layout.addWidget(quit_button)
        
        layout.addLayout(button_layout)

        # Load initial data
        self.refresh_summary()
        self.refresh_accounts()

    # Close the application
    def closeEvent(self, a0):
        if self.db:
            self.db.close()
        
        super().closeEvent(a0)
        
        QApplication.quit()       

    # Create Tabs for the main window
    def create_budget_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()
        
        date_layout = QHBoxLayout()

        self.select_date_label = QLabel("Select Month:")
        date_layout.addWidget(self.select_date_label)

        self.select_month_combo = QComboBox()
        date_layout.addWidget(self.select_month_combo)

        self.select_year_combo = QComboBox()
        date_layout.addWidget(self.select_year_combo)

        layout.addLayout(date_layout)

        budget_summary_layout = QHBoxLayout()

        self.budget_summary_table = QTableWidget()
        self.budget_summary_table.setColumnCount(4)
        self.budget_summary_table.setHorizontalHeaderLabels(["Category Name", "Type", "Current Balance", "Goal"])

        budget_summary_layout.addWidget(self.budget_summary_table)

        layout.addLayout(budget_summary_layout)

        button_layout = QHBoxLayout()

        refresh_budget_btn = QPushButton("Refresh Budget")
        refresh_budget_btn.clicked.connect(self.refresh_budget)
        button_layout.addWidget(refresh_budget_btn)       

        modify_categories = QPushButton("Modify Categories")
        modify_categories.clicked.connect(self.handle_modify_categories)
        button_layout.addWidget(modify_categories)       

        layout.addLayout(button_layout)

        widget.setLayout(layout)

        self.fetch_budget_date_combos()
        self.refresh_budget()

        return widget
        
    def create_summary_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()
        
        self.account_summary_table = QTableWidget()
        self.account_summary_table.setColumnCount(3)
        self.account_summary_table.setHorizontalHeaderLabels(["Name", "Amount", "Type"])
        layout.addWidget(self.account_summary_table)

        button_layout = QHBoxLayout()

        refresh_btn = QPushButton("Refresh")
        refresh_btn.clicked.connect(self.refresh_accounts)
        button_layout.addWidget(refresh_btn)
 
        add_account_btn = QPushButton("Add")
        add_account_btn.clicked.connect(self.handle_add_account)
        button_layout.addWidget(add_account_btn)

        delete_account_btn = QPushButton("Delete")
        delete_account_btn.clicked.connect(self.handle_delete_account)
        button_layout.addWidget(delete_account_btn)

        layout.addLayout(button_layout)
        
        widget.setLayout(layout)
        return widget
 
    def create_view_transactions_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()
        
        self.transaction_summary_table = QTableWidget()
        self.transaction_summary_table.setColumnCount(6)
        self.transaction_summary_table.setHorizontalHeaderLabels(["Date", "Description", "Amount", "Category", "Account", "Type"])
        layout.addWidget(self.transaction_summary_table)
        
        button_layout = QHBoxLayout()
        
        add_btn = QPushButton("Add Transaction")
        add_btn.clicked.connect(self.handle_add_transaction)
        button_layout.addWidget(add_btn)
        
        refresh_btn = QPushButton("Refresh")
        refresh_btn.clicked.connect(self.refresh_summary)
        button_layout.addWidget(refresh_btn)
        
        delete_btn = QPushButton("Delete Transaction")
        delete_btn.clicked.connect(self.handle_delete_transaction)
        button_layout.addWidget(delete_btn)
        
        layout.addLayout(button_layout)
        
        widget.setLayout(layout)
        return widget
        
    def create_reports_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()
        
        layout.addWidget(QLabel("Summary coming soon"))
        
        widget.setLayout(layout)
        return widget
       
    # Handle buttons
    def handle_add_account(self):
        self.popup_window.open_window(AddAccountsWindow("Add Accounts", 300, 400, self.db))
        self.refresh_accounts()

    def handle_settings(self):
        self.popup_window.open_window(SettingsWindow("Modify Settings", 300, 400, self.db))

    def handle_modify_categories(self):
        self.popup_window.open_window(ModifyCategoriesWindow("Modify Categories", 300, 400, self.db))
        self.refresh_summary()

    def handle_delete_account(self):
        self.popup_window.open_window(DelAccountsWindow("Delete Accounts", 300, 400, self.db))
        self.refresh_accounts()

    def handle_add_transaction(self):
        self.popup_window.open_window(AddTransactionsWindow("Add Transaction", 400, 500, self.db))
        self.refresh_summary()

    def handle_delete_transaction(self):
        self.popup_window.open_window(DelTransactionsWindow("Delete Transactions", 400, 500, self.db))
        self.refresh_summary()

    # Refresh the summary tables
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

    def refresh_budget(self):
        try:
            selected_month_name = self.select_month_combo.currentText()
            selected_year = self.select_year_combo.currentText()
            
            month_int_mapping = {
                "January": 1, "February": 2, "March": 3, "April": 4,
                "May": 5, "June": 6, "July": 7, "August": 8,
                "September": 9, "October": 10, "November": 11, "December": 12
            }
            
            if selected_month_name and selected_year:
                selected_month = month_int_mapping.get(selected_month_name)
                budgets = self.budget_db_service.search_all(year=int(selected_year), month=selected_month)
            else:
                budgets = self.budget_db_service.search_all()
                
        except Exception as e:
            print("Error while refreshing Budget:")
            print(e)
            return
        
        self.budget_summary_table.setRowCount(len(budgets))

        for i, budget in enumerate(budgets):
            name = QTableWidgetItem(str(budget[0]))
            category_type = QTableWidgetItem(str(budget[1]))
            balance = QTableWidgetItem(str(budget[2]))
            goal = QTableWidgetItem(str(budget[3]))

            self.budget_summary_table.setItem(i, 0, name)
            self.budget_summary_table.setItem(i, 1, category_type)
            self.budget_summary_table.setItem(i, 2, balance)
            self.budget_summary_table.setItem(i, 3, goal)

        self.budget_summary_table.resizeColumnsToContents()

    def fetch_budget_date_combos(self):
        months = ["January", "February", "March", "April", "May", "June",
                  "July", "August", "September", "October", "November", "December"]
        
        self.select_month_combo.addItems(months)
        
        current_year = datetime.today().strftime('%Y')
        current_month = datetime.today().strftime('%B')  # Full month name
        
        years_to_date = []
        for year in range(int(current_year), 2019, -1):
            years_to_date.append(str(year))
        self.select_year_combo.addItems(years_to_date)
        
        self.select_month_combo.setCurrentText(current_month)
        self.select_year_combo.setCurrentText(current_year)


