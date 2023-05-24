import sys

from PySide6 import QtWidgets

from src.widgets.custom_styles.checkbox_style import CheckBoxStyle
from src.widgets.main_window_widget import MainWindowWidget


def main():
    app = QtWidgets.QApplication([])

    main_window = MainWindowWidget()
    main_window.resize(800, 600)
    main_window.setWindowTitle("Asciiator GUI")
    main_window.show()

    with open("./assets/stylesheets/main.qss", "r") as main_stylesheet:
        _style = main_stylesheet.read()
        app.setStyleSheet(_style)

    app.setStyle(CheckBoxStyle(app.style()))

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
