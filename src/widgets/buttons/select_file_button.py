from pathlib import Path

from PySide6 import QtCore
from PySide6.QtWidgets import QFileDialog

from src.widgets.buttons.base_button_widget import BaseButtonWidget
from src.widgets.util.file import File


class SelectFilesButton(BaseButtonWidget):
    filesSelected = QtCore.Signal()

    def __init__(self):
        super().__init__("Select Files")

    def select_image_files(self, input_files: dict) -> None:
        initial_path = f"{Path.home()}"

        selected_files = QFileDialog.getOpenFileNames(
            self,
            "Select Files",
            initial_path,
            f"Images & Videos ({File.get_file_dialog_filter()})",
        )

        for file in selected_files[0]:
            input_files[file] = {
                "reduction": 4,
                "inverted": False,
                "text_file": False,
                "output_path": ""
            }

        self.filesSelected.emit()
