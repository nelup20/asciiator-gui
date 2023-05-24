import subprocess

from PySide6 import QtCore

from src.widgets.buttons.base_button_widget import BaseButtonWidget


class TransformFilesButton(BaseButtonWidget):
    changeStatus = QtCore.Signal(str)

    def __init__(self):
        super().__init__("Transform Files")

    def transform_images(self, input_files: dict) -> None:
        self.changeStatus.emit("Transforming...")

        for image_path, options in input_files.items():
            inverted = "-inverted" if options["inverted"] else ""
            text_file = "-text_file" if options["text_file"] else ""
            reduction = f"--reduction={options['reduction']}"

            subprocess.run(
                f'asciiator "{image_path}" {inverted} {text_file} {reduction}'
            )

        self.changeStatus.emit("Done")

    def disable_transform_button(self) -> None:
        self.setDisabled(True)
        # TODO: try via self#setProperty & QSS rule/selector
        self.setStyleSheet("background-color: #a2a2a2")

    def enable_transform_button(self) -> None:
        if not self.isEnabled():
            self.setEnabled(True)
            self.setStyleSheet("background-color: #262626")
