from PyQt6.QtWidgets import QPushButton, QTableWidget, QVBoxLayout, QTableWidgetItem

from views.popup_window import PopUpWindow
from views.window_manager import WindowManager

from controllers.db.categories_db_service import CategoriesDBService

from .add_categories_window import AddCategoriesWindow
from .del_categories_window import DelCategoriesWindow

class ModifyCategoriesWindow(PopUpWindow):
    def __init__(self, window_name: str, min_width: int, min_height: int, db, parent=None) -> None:
        super().__init__(window_name, min_width, min_height, db, parent)

        self.db = db
        self.categories_db_service = CategoriesDBService(self.db)

        self.popup_window = WindowManager()

        self.setup_ui()

        self.refresh_categories()

    def setup_ui(self):
        layout = QVBoxLayout()

        self.summary_table = QTableWidget()
        self.summary_table.setColumnCount(2)
        self.summary_table.setHorizontalHeaderLabels(["Name", "Type"])
        layout.addWidget(self.summary_table)

        add_category_btn = QPushButton("Add")
        add_category_btn.clicked.connect(lambda: self.popup_window.open_window(AddCategoriesWindow("Add Categories", 300, 400, self.db)))
        layout.addWidget(add_category_btn)

        del_category_btn = QPushButton("Delete")
        del_category_btn.clicked.connect(lambda: self.popup_window.open_window(DelCategoriesWindow("Delete Categories", 300, 400, self.db)))
        layout.addWidget(del_category_btn)

        self.setLayout(layout)

    def refresh_categories(self):
        try:
            categories = self.categories_db_service.search_all()
        except Exception as e:
            print("Error while refreshing categories:")
            print(e)
            return
        
        self.summary_table.setRowCount(len(categories)) # type: ignore

        for i, category in enumerate(categories): # type: ignore
            name = QTableWidgetItem(str(category[1]))
            category_type = QTableWidgetItem(str(category[3]))

            self.summary_table.setItem(i, 0, name)
            self.summary_table.setItem(i, 1, category_type)

        self.summary_table.resizeColumnsToContents()

