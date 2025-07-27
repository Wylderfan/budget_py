from PyQt6.QtWidgets import QDialog


class WindowManager():
    def __init__(self) -> None:
        pass

    def open_window(self, window):
        if window.exec() == QDialog.DialogCode.Accepted:
            # User Accepted
            print("Accepted")
        else:
            # User Cancelled
            print("Cancelled")

