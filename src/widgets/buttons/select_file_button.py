from pathlib import Path

from PySide6 import QtCore
from PySide6.QtWidgets import QFileDialog

from src.widgets.buttons.base_button_widget import BaseButtonWidget


class SelectFilesButton(BaseButtonWidget):
    filesSelected = QtCore.Signal()

    def __init__(self):
        super().__init__("Select Image Files")
        self.clicked.connect(self.select_image_files)

    def select_image_files(self) -> None:
        initial_path = f"{Path.home()}"

        selected_files = QFileDialog.getOpenFileNames(
            self, "Select Images", initial_path, "Image Files (*.png *.jpg *.bmp)"
        )

        for file in selected_files[0]:
            self.parent().input[file] = {
                "reduction": 4,
                "inverted": False,
                "text_file": False,
            }

        self.filesSelected.emit()
