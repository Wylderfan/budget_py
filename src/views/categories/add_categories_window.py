from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QComboBox, QFormLayout, QHBoxLayout, QLabel, QLineEdit, QMessageBox, QPushButton, QVBoxLayout
from views.common.popup_window import PopUpWindow

from controllers.db.categories_db_service import CategoriesDBService

class AddCategoriesWindow(PopUpWindow):
    def __init__(self, window_name: str, min_width: int, min_height: int, db, parent=None) -> None:
        super().__init__(window_name, min_width, min_height, db, parent)

        self.categies_db_service = CategoriesDBService(self.get_db())

        self.setup_ui()

    def setup_ui(self):
        main_layout = QVBoxLayout()
        
        title_label = QLabel("Add New Category")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title_label)
        
        form_layout = QFormLayout()
        
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Enter category name")
        form_layout.addRow("Account Name:", self.name_input)
        
        self.category_type_combo = QComboBox()
        self.category_type_combo.addItems([
            "Expense",
            "Income", 
            "Debt" 
        ]) # TODO change to json format
        form_layout.addRow("Category Type:", self.category_type_combo)

        self.budget_goal_input = QLineEdit()
        self.budget_goal_input.setPlaceholderText("Enter budget goal")
        form_layout.addRow("Budget Goal:", self.budget_goal_input)
        
        main_layout.addLayout(form_layout)
        
        button_layout = QHBoxLayout()
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setAutoDefault(False) # Needed for highlighting the submit button instead
        cancel_btn.clicked.connect(self.reject)
        
        add_category_btn = QPushButton("Add Category")
        add_category_btn.clicked.connect(self.add_category)
        
        button_layout.addWidget(cancel_btn)
        button_layout.addWidget(add_category_btn)
        
        main_layout.addLayout(button_layout)
        
        self.setLayout(main_layout)

    def add_category(self):
        category_name = self.name_input.text().strip()
        category_type = self.category_type_combo.currentText()
        budget_goal_text = self.budget_goal_input.text().strip()

        if not budget_goal_text:
            QMessageBox.warning(self, "Invalid Input", "Please enter an amount.")
            return
            
        try:
            amount = round(float(budget_goal_text), 2)
            if amount <= 0:
                QMessageBox.warning(self, "Invalid Input", "Amount must be greater than 0.")
                return
        except ValueError:
            QMessageBox.warning(self, "Invalid Input", "Please enter a valid number for goal amount.")
            return
        if not category_name:
            QMessageBox.warning(self, "Invalid Input", "Please enter a category name.")
            return
            
        if len(category_name) > 45:
            QMessageBox.warning(self, "Invalid Input", "Category name must be 45 characters or less.")
            return
        
        print(f"Adding Category:")
        print(f"Name: {category_name}")
        print(f"Category type: {category_type}")
        print(f"Goal amount: ${amount:.2f}")

        try:
            category_result = self.categies_db_service.add_category(category_name, category_type)
            goal_result = self.categies_db_service.add_goal(category_name, amount)
            if category_result == 1 and goal_result == 1:
                QMessageBox.information(self, "Success", "Category and Goal added successfully!")
                self.accept()
            else:
                QMessageBox.warning(self, "Error", "Failed to add category or goal.")
            
        except Exception as e:
            print(f"Error adding category: {e}")
            QMessageBox.warning(self, "Error", f"An error occurred: {str(e)}")

