from PyQt6.QtWidgets import QCheckBox, QComboBox, QFormLayout, QHBoxLayout, QLabel, QPushButton, QVBoxLayout
from PyQt6.QtCore import Qt

from controllers.db.account_db_service import AccountDBService
from views.popup_window import PopUpWindow

class DelAccountsWindow(PopUpWindow):
    def __init__(self, window_name: str, min_width: int, min_height: int, db, parent=None) -> None:
        super().__init__(window_name, min_width, min_height, db, parent)

        self.account_db_service = AccountDBService(self.get_db())

        self.setup_ui()

    def setup_ui(self):
        main_layout = QVBoxLayout()

        title_lable = QLabel("Delete Accounts")
        title_lable.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title_lable)

        form_layout = QFormLayout()

        self.select_account_combo = QComboBox()
        accounts = self.account_db_service.select_name_id_all_accounts() # name , id tuple
        self.account_names = [row[0] for row in accounts] # type: ignore
        self.account_ids = [row[1] for row in accounts] # type: ignore
        self.select_account_combo.addItems(self.account_names) # type: ignore
        form_layout.addRow("Select Account:", self.select_account_combo)

        self.transfer_checkbox = QCheckBox()
        form_layout.addRow("Transfer transactions to separate account:", self.transfer_checkbox)

        self.select_transfer_combo = QComboBox()
        self.select_transfer_combo.addItems(self.account_names) # type: ignore
        form_layout.addRow("Select account to transfer too:", self.select_transfer_combo)

        main_layout.addLayout(form_layout)

        button_layout = QHBoxLayout()
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setAutoDefault(False)
        cancel_btn.clicked.connect(self.reject)
        
        add_account_btn = QPushButton("Delete Account")
        add_account_btn.clicked.connect(self.del_account)
        
        button_layout.addWidget(cancel_btn)
        button_layout.addWidget(add_account_btn)
        
        main_layout.addLayout(button_layout)
        
        self.setLayout(main_layout)

    def id_from_combo(self, name):
        id = self.account_db_service.search_account(name=name)
        if len(id) == 1: # type: ignore
            return id[0][0] # type: ignore
        else:
            print("Multiple entries of the same name")
            return None
        
    def del_account(self):
        selected_account = self.select_account_combo.currentText()
        is_transfer = True if self.transfer_checkbox.checkState() == Qt.CheckState.Checked else False
        transfer_account = None

        if is_transfer:
            transfer_account = self.select_transfer_combo.currentText()

        # TODO add in a verification popup_window

        print(f"Deleting Account:")
        print(f"Name: {selected_account}")

        if is_transfer:
            print(f"Transferring transactions to: {transfer_account}")

        if transfer_account is not None:
            # TODO transfer transactions to transfer_account
            print("Transferring account")

        try:
            self.account_db_service.del_account(self.id_from_combo(selected_account))
        except Exception as e:
            print(f"Error Deleting Account:\n{e}")

        self.accept()

