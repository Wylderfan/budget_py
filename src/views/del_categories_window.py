from PyQt6.QtWidgets import QCheckBox, QComboBox, QFormLayout, QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QMessageBox
from PyQt6.QtCore import Qt

from views.popup_window import PopUpWindow

from controllers.db.categories_db_service import CategoriesDBService

class DelCategoriesWindow(PopUpWindow):
    def __init__(self, window_name: str, min_width: int, min_height: int, db, parent=None) -> None:
        super().__init__(window_name, min_width, min_height, db, parent)

        self.categories_db_service = CategoriesDBService(self.get_db())

        self.setup_ui()

    def setup_ui(self):
        main_layout = QVBoxLayout()

        title_lable = QLabel("Delete Categories")
        title_lable.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title_lable)

        form_layout = QFormLayout()

        self.select_category_combo = QComboBox()
        self.category_names = [row[0] for row in self.categories_db_service.select_category_names()] #type: ignore

        self.select_category_combo.addItems(self.category_names) # type: ignore

        form_layout.addRow("Select Category:", self.select_category_combo)
        
        self.transfer_checkbox = QCheckBox()
        form_layout.addRow("Transfer transactions to separate category:", self.transfer_checkbox)

        self.select_transfer_combo = QComboBox()
        self.select_transfer_combo.addItems(self.category_names) # type: ignore
        form_layout.addRow("Select category to transfer to:", self.select_transfer_combo)

        main_layout.addLayout(form_layout)

        button_layout = QHBoxLayout()
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setAutoDefault(False)
        cancel_btn.clicked.connect(self.reject)
        
        del_category_btn = QPushButton("Delete Category")
        del_category_btn.clicked.connect(self.del_category)
        
        button_layout.addWidget(cancel_btn)
        button_layout.addWidget(del_category_btn)
        
        main_layout.addLayout(button_layout)
        
        self.setLayout(main_layout)

    def id_from_name(self, name):
        id = self.categories_db_service.search_categories(name=name)
        if len(id) == 1: # type: ignore
            return id[0][0] # type: ignore
        else:
            print("Multiple entries of the same name")
            return None
 
        
    def del_category(self):
        selected_category = self.select_category_combo.currentText()
        is_transfer = True if self.transfer_checkbox.checkState() == Qt.CheckState.Checked else False
        transfer_category = self.select_transfer_combo.currentText() if is_transfer else None

        if not selected_category:
            QMessageBox.warning(self, "Error", "No category selected.")
            return

        # Create confirmation message
        confirmation_msg = f"Are you sure you want to delete this category?\n\nCategory: {selected_category}"
        if is_transfer and transfer_category and transfer_category != selected_category:
            confirmation_msg += f"\n\nAll transactions will be transferred to: {transfer_category}"
        elif is_transfer:
            QMessageBox.warning(self, "Error", "Cannot transfer to the same category being deleted.")
            return
        else:
            confirmation_msg += "\n\nWarning: All transactions in this category will be permanently deleted!"

        # Verification dialog
        reply = QMessageBox.question(
            self,
            "Confirm Category Deletion",
            confirmation_msg,
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )

        if reply != QMessageBox.StandardButton.Yes:
            return

        print(f"Deleting Category:")
        print(f"Name: {selected_category}")

        if is_transfer and transfer_category and transfer_category != selected_category:
            print(f"Transferring transactions to: {transfer_category}")
            # TODO: Implement transaction transfer logic here
            # transfer_category_id = self.id_from_name(transfer_category)
            # self.categories_db_service.transfer_transactions(category_id, transfer_category_id)

        try:
            category_id = self.id_from_name(selected_category)
            if category_id is None:
                QMessageBox.warning(self, "Error", "Could not find category to delete.")
                return
                
            result = self.categories_db_service.del_category(category_id)
            if result == 1:
                QMessageBox.information(self, "Success", "Category deleted successfully!")
            else:
                QMessageBox.warning(self, "Error", "Failed to delete category.")
        except Exception as e:
            print(f"Error deleting category:\n{e}")
            QMessageBox.warning(self, "Error", f"An error occurred while deleting: {str(e)}")

        self.accept()

