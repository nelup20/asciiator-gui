from typing import List

from PySide6 import QtCore
from PySide6.QtCore import QSize, Qt
from PySide6.QtWidgets import QTableWidget, QTableWidgetItem, QWidget

from src.widgets.util.file import File

_TABLE_COLUMN_HEADERS = [
    "Name",
    "Path",
    "Status",
    "Output",
    "Invert?",
    "Text file?",
    "Reduction",
    "Actions",
]


class InputTable(QTableWidget):
    optionsChanged = QtCore.Signal(str, str, object)
    errorOccurred = QtCore.Signal(str)
    errorRemoved = QtCore.Signal(tuple)
    enableTransform = QtCore.Signal()

    def __init__(self, parent: QWidget):
        super().__init__(0, 8, parent)

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

            output = QTableWidgetItem("")

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

            actions = QTableWidgetItem("R D")
            actions.setFlags(Qt.ItemFlag.ItemIsEnabled)
            actions.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

            new_row = self.rowCount()
            self.insertRow(new_row)

            self.setItem(new_row, 0, file_name)
            self.setItem(new_row, 1, path)
            self.setItem(new_row, 2, status)
            self.setItem(new_row, 3, output)
            self.setItem(new_row, 4, inverted_checkbox)
            self.setItem(new_row, 5, text_file_checkbox)
            self.setItem(new_row, 6, reduction_factor)
            self.setItem(new_row, 7, actions)

        self.itemChanged.connect(self.cell_value_changed)

    def cell_value_changed(self, cell: QTableWidgetItem) -> None:
        file_path = self.get_file_path(cell.row())

        if cell.column() == 3:
            self.optionsChanged.emit(file_path, "output_path", cell.text())

        if cell.column() == 4:
            is_inverted = self.is_checked(cell)

            self.optionsChanged.emit(file_path, "inverted", is_inverted)

        if cell.column() == 5:
            text_file = self.is_checked(cell)

            self.optionsChanged.emit(file_path, "text_file", text_file)

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
                    self.errorRemoved.emit(cell_coords)

                self.optionsChanged.emit(file_path, "reduction", reduction)

                if len(self.cells_with_errors) == 0:
                    self.enableTransform.emit()
            except ValueError:
                cell.setBackground(Qt.GlobalColor.red)

                if (
                    cell_coords := (cell.row(), cell.column())
                ) not in self.cells_with_errors:
                    self.cells_with_errors.append(cell_coords)

                self.errorOccurred.emit(
                    f"Error for cell at row {cell.row()}, column {cell.column()}. "
                    f"The reduction factor needs to be a number between 1 and 25."
                )

    def change_status(self, new_status: str) -> None:
        for row in range(self.rowCount()):
            self.item(row, 2).setText(new_status)

    def get_file_path(self, row: int) -> str:
        return self.item(row, 1).text()

    def is_checked(self, cell: QTableWidgetItem) -> bool:
        return True if cell.checkState() is Qt.CheckState.Checked else False
