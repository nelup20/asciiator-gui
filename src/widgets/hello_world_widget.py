from PySide6 import QtCore, QtWidgets


class HelloWorldWidget(QtWidgets.QWidget):
    def __init__(self) -> None:
        super().__init__()

        self.button = QtWidgets.QPushButton("Click to increment")
        self.text = QtWidgets.QLabel(
            "Hello World! Count: 0", alignment=QtCore.Qt.AlignCenter
        )
        self.count = 0

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.button)

        self.button.clicked.connect(self.increment)

    def increment(self):
        self.count += 1
        self.text.setText(f"Hello World! Count: {self.count}")
