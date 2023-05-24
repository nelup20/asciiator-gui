from PySide6 import QtWidgets
from PySide6.QtCore import Qt
from PySide6.QtGui import QCursor


class BaseButtonWidget(QtWidgets.QPushButton):
    def __init__(self, button_text=""):
        super().__init__(button_text)
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
