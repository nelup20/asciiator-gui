import sys

from PySide6 import QtWidgets

from src.widgets.hello_world_widget import HelloWorldWidget


def main():
    app = QtWidgets.QApplication([])

    hello_world_widget = HelloWorldWidget()
    hello_world_widget.resize(800, 600)
    hello_world_widget.show()
    hello_world_widget.setWindowTitle("Asciiator GUI")

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
