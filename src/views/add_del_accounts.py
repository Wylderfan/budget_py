from PyQt6.QtWidgets import (
    QDialog, QWidget, QTableWidget, QVBoxLayout, QHBoxLayout, QFormLayout, 
    QLineEdit, QPushButton, QComboBox, QDateEdit, QLabel
)
from PyQt6.QtCore import QDate
from .add_del_window import AddDelWindow

class AddDelAccountsWindow(AddDelWindow):
    def __init__(self, window_name: str, min_width: int, min_height: int, parent=None) -> None:
        super().__init__(window_name, min_width, min_height, parent)

        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()
        
        # Form fields
        form_layout = QFormLayout()
        
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
        
        # Add to form
        form_layout.addRow("Amount:", self.amount_input)
        form_layout.addRow("Description:", self.description_input)
        form_layout.addRow("Category:", self.category_combo)
        form_layout.addRow("Date:", self.date_input)
        form_layout.addRow("Type:", self.type_combo)
        
        layout.addLayout(form_layout)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        save_btn = QPushButton("Save")
        save_btn.clicked.connect(self.accept)  # This closes dialog and returns Accepted
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)  # This closes dialog and returns Rejected
        
        button_layout.addWidget(save_btn)
        button_layout.addWidget(cancel_btn)
        
        layout.addLayout(button_layout)
        self.setLayout(layout)

    def testsetup_ui(self):
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Summary table
        self.summary_table = QTableWidget()
        self.summary_table.setColumnCount(4)
        self.summary_table.setHorizontalHeaderLabels(["Name", "Amount", "Category"])
        layout.addWidget(self.summary_table)
    
        # Refresh button
        refresh_btn = QPushButton("Refresh")
        refresh_btn.clicked.connect(self.refresh_accounts)
        layout.addWidget(refresh_btn)
        
        widget.setLayout(layout)

    def refresh_accounts(self):
        print("Refreshing Accounts")
 
