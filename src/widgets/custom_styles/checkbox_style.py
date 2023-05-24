from PySide6 import QtWidgets


# TODO: would've preferred to fix it via QSS/stylesheet but couldn't get it working
# the QTableWidget::indicator selector works if you set width, height and margin, but then the whole cell is clickable
class CheckBoxStyle(QtWidgets.QProxyStyle):
    def subElementRect(
        self,
        element,
        option,
        widget,
    ):
        rectangle = super().subElementRect(element, option, widget)

        if element == QtWidgets.QStyle.SE_ItemViewItemCheckIndicator:
            rectangle.moveCenter(option.rect.center())

        return rectangle
