from typing import List

from PySide6 import QtCore
from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QCursor
from PySide6.QtWidgets import (
    QApplication,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QWidget,
)

from src.widgets.util.file import File

_TABLE_COLUMN_HEADERS = [
    "Name",
    "Path",
    "Status",
    "Output",
    "Invert?",
    "Text file?",
    "Reduction",
    "Redo",
    "Remove",
]


class InputTable(QTableWidget):
    options_changed = QtCore.Signal(str, str, object)
    error_occurred = QtCore.Signal(str)
    error_removed = QtCore.Signal(tuple)
    enable_transform = QtCore.Signal()
    redo_transform = QtCore.Signal(str)
    remove_file = QtCore.Signal(str)

    def __init__(self, parent: QWidget):
        super().__init__(0, 9, parent)

        self.displayed_files: List[str] = []
        self.cells_with_errors: List[tuple[int, int]] = []

        self.setHorizontalHeaderLabels(_TABLE_COLUMN_HEADERS)
        self.setMinimumSize(QSize(700, 300))

    def display_files(self, input_files: dict) -> None:
        for file_path, options in input_files.items():
            if file_path in self.displayed_files:
                continue

            self.displayed_files.append(file_path)

            file_name = QTableWidgetItem(file_path.split("/")[-1])
            file_name.setFlags(Qt.ItemFlag.ItemIsEnabled)

            path = QTableWidgetItem(file_path)
            path.setFlags(Qt.ItemFlag.ItemIsEnabled)

            status = QTableWidgetItem("Pending")
            status.setFlags(Qt.ItemFlag.ItemIsEnabled)
            status.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

            output = QTableWidgetItem(options["output_path"])

            inverted_checkbox = QTableWidgetItem()
            inverted_checkbox.setFlags(
                Qt.ItemFlag.ItemIsUserCheckable | Qt.ItemFlag.ItemIsEnabled
            )
            inverted_checkbox.setCheckState(Qt.CheckState.Unchecked)

            text_file_checkbox = QTableWidgetItem()
            text_file_checkbox.setFlags(
                Qt.ItemFlag.ItemIsUserCheckable | Qt.ItemFlag.ItemIsEnabled
            )
            if File.is_image_file(file_path):
                text_file_checkbox.setCheckState(Qt.CheckState.Unchecked)

            reduction_factor = QTableWidgetItem("4")
            reduction_factor.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

            redo_button = QPushButton("🔄")
            redo_button.setProperty("cssClass", "tableButton")
            redo_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
            redo_button.clicked.connect(self.redo_transformation)

            remove_button = QPushButton("❌")
            remove_button.setProperty("cssClass", "tableButton")
            remove_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
            remove_button.clicked.connect(self.remove_file_from_table)

            new_row = self.rowCount()
            self.insertRow(new_row)

            self.setItem(new_row, 0, file_name)
            self.setItem(new_row, 1, path)
            self.setItem(new_row, 2, status)
            self.setItem(new_row, 3, output)
            self.setItem(new_row, 4, inverted_checkbox)
            self.setItem(new_row, 5, text_file_checkbox)
            self.setItem(new_row, 6, reduction_factor)
            self.setCellWidget(new_row, 7, redo_button)
            self.setCellWidget(new_row, 8, remove_button)

        self.itemChanged.connect(self.cell_value_changed)

    def cell_value_changed(self, cell: QTableWidgetItem) -> None:
        file_path = self.get_file_path(cell.row())

        if cell.column() == 3:
            self.options_changed.emit(file_path, "output_path", cell.text())

        if cell.column() == 4:
            is_inverted = self.is_checked(cell)

            self.options_changed.emit(file_path, "inverted", is_inverted)

        if cell.column() == 5:
            text_file = self.is_checked(cell)

            self.options_changed.emit(file_path, "text_file", text_file)

        if cell.column() == 6:
            try:
                reduction = int(cell.text())

                if reduction < 1 or reduction > 25:
                    raise ValueError()

                cell.setBackground(Qt.GlobalColor.white)

                if (
                    cell_coords := (cell.row(), cell.column())
                ) in self.cells_with_errors:
                    self.cells_with_errors.remove(cell_coords)
                    self.error_removed.emit(cell_coords)

                self.options_changed.emit(file_path, "reduction", reduction)

                if len(self.cells_with_errors) == 0:
                    self.enable_transform.emit()
            except ValueError:
                cell.setBackground(Qt.GlobalColor.red)

                if (
                    cell_coords := (cell.row(), cell.column())
                ) not in self.cells_with_errors:
                    self.cells_with_errors.append(cell_coords)

                self.error_occurred.emit(
                    f"Error for file nr. {cell.row() + 1}'s reduction factor. "
                    f"The reduction factor needs to be a number between 1 and 25."
                )

    def redo_transformation(self) -> None:
        clicked_button = QApplication.focusWidget()

        row = self.indexAt(clicked_button.pos()).row()
        file_path = self.get_file_path(row)

        self.redo_transform.emit(file_path)

    def remove_file_from_table(self) -> None:
        clicked_button = QApplication.focusWidget()

        row = self.indexAt(clicked_button.pos()).row()
        file_path = self.get_file_path(row)

        self.displayed_files.remove(file_path)
        self.removeRow(row)
        self.remove_file.emit(file_path)

    def change_status(self, new_status: str) -> None:
        for row in range(self.rowCount()):
            self.item(row, 2).setText(new_status)

    def get_file_path(self, row: int) -> str:
        return self.item(row, 1).text()

    def is_checked(self, cell: QTableWidgetItem) -> bool:
        return True if cell.checkState() is Qt.CheckState.Checked else False
