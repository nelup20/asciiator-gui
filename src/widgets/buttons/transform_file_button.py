import subprocess

from PySide6 import QtCore

from src.widgets.buttons.base_button_widget import BaseButtonWidget

_DISABLED_BUTTON_BACKGROUND = "background-color: #a2a2a2"
_ENABLED_BUTTON_BACKGROUND = "background-color: #262626"


class TransformFilesButton(BaseButtonWidget):
    status_change = QtCore.Signal(str)

    def __init__(self):
        super().__init__("Transform Files")

    def transform_images(self, input_files: dict) -> None:
        self.status_change.emit("Transforming...")

        for image_path, options in input_files.items():
            inverted = "-inverted" if options["inverted"] else ""
            text_file = "-text_file" if options["text_file"] else ""
            reduction = f"--reduction={options['reduction']}"
            output_path = (
                f"--output_path=\"{options['output_path']}\""
                if len(options["output_path"].strip()) > 0
                else ""
            )

            subprocess.run(
                f'asciiator "{image_path}" {inverted} {text_file} {reduction} {output_path}'
            )

        self.status_change.emit("Done")

    def disable_transform_button(self) -> None:
        self.setDisabled(True)
        self.setStyleSheet(_DISABLED_BUTTON_BACKGROUND)

    def enable_transform_button(self) -> None:
        if not self.isEnabled():
            self.setEnabled(True)
            self.setStyleSheet(_ENABLED_BUTTON_BACKGROUND)
