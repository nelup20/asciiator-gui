from typing import Union

from PySide6 import QtWidgets
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel

from src.widgets.buttons.select_file_button import SelectFilesButton
from src.widgets.buttons.transform_file_button import TransformFilesButton
from src.widgets.input_table import InputTable


class MainWindowWidget(QtWidgets.QWidget):
    def __init__(self) -> None:
        super().__init__()

        self.input: dict[str, dict] = {}
        self.error_messages: list[str] = []

        self.widget_layout = QtWidgets.QVBoxLayout(self)

        self.input_table = InputTable(self)
        self.error_label = QLabel()
        self.select_files_button = SelectFilesButton()
        self.transform_files_button = TransformFilesButton()

        self.error_label.setWordWrap(True)

        self.setup_input_table_signals()
        self.setup_select_files_button_signals()
        self.setup_transform_files_button_signals()

        self.add_widgets_to_layout()

    def change_file_options(
        self, file_path: str, option: str, option_value: Union[bool, int]
    ) -> None:
        self.input[file_path][option] = option_value

    def add_error_message(self, error_message: str) -> None:
        if error_message not in self.error_messages:
            self.error_messages.append(error_message)

        self.error_label.setText(error_message)

    def remove_error_message(self, cell: tuple[int, int]) -> None:
        for error in self.error_messages:
            if f"row {cell[0]}, column {cell[1]}" in error:
                self.error_messages.remove(error)
                break

        error_message = "" if len(self.error_messages) == 0 else self.error_messages[-1]

        self.error_label.setText(error_message)

    def setup_input_table_signals(self) -> None:
        self.input_table.optionsChanged.connect(self.change_file_options)
        self.input_table.errorOccurred.connect(self.add_error_message)
        self.input_table.errorOccurred.connect(
            self.transform_files_button.disable_transform_button
        )
        self.input_table.errorRemoved.connect(self.remove_error_message)
        self.input_table.enableTransform.connect(
            self.transform_files_button.enable_transform_button
        )

    def setup_select_files_button_signals(self) -> None:
        self.select_files_button.clicked.connect(
            lambda: self.select_files_button.select_image_files(self.input)
        )
        self.select_files_button.filesSelected.connect(
            lambda: self.input_table.display_files(self.input)
        )

    def setup_transform_files_button_signals(self) -> None:
        self.transform_files_button.changeStatus.connect(self.input_table.change_status)
        self.transform_files_button.clicked.connect(
            lambda: self.transform_files_button.transform_images(self.input)
        )

    def add_widgets_to_layout(self) -> None:
        self.widget_layout.addWidget(
            self.input_table, alignment=Qt.AlignmentFlag.AlignCenter
        )
        self.widget_layout.addWidget(
            self.error_label, alignment=Qt.AlignmentFlag.AlignCenter
        )
        self.widget_layout.addWidget(
            self.select_files_button, alignment=Qt.AlignmentFlag.AlignHCenter
        )
        self.widget_layout.addWidget(
            self.transform_files_button, alignment=Qt.AlignmentFlag.AlignHCenter
        )
