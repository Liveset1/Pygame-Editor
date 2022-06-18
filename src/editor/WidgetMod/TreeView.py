from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class StandardItem(QStandardItem):
    def __init__(self, text, font_size, bold, color: QColor = QColor(0, 0, 0), icon: QIcon = None):
        super(StandardItem, self).__init__()
        font = QFont("Open Sans", font_size)
        font.setBold(bold)
        self.setForeground(color)
        self.setText(text)
        self.setIcon(icon)
        self.setFont(font)


class TreeView(QTreeView):
    def __init__(self, parent: QWidget = None, items: list = None):
        # Init Outer Class
        super().__init__(parent)

        # Set Properties
        self.setHeaderHidden(True)
        self.setRootIsDecorated(True)
        self.setObjectName(parent.objectName())
        self.setGeometry(0, 0, 0, 0)
        self.resize(parent.width(), parent.height())
        self.Scroll = QScrollBar(self)
        self.addScrollBarWidget(self.Scroll, Qt.AlignmentFlag.AlignRight)
        self.horizontalScrollBar().setEnabled(True)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.setHorizontalScrollMode(True)

        # Tree Model
        self.TreeModel = QStandardItemModel()
        self.rootNode = self.TreeModel.invisibleRootItem()

        self.installEventFilter(self)
        self.setModel(self.TreeModel)

        for i in items:
            self.rootNode.appendRow(i)

    def contextMenuEvent(self, event: QContextMenuEvent) -> None:
        cmenu = QMenu(self)
        # Deslect Option
        try:
            if len(self.selectedIndexes()) > 0:
                deselect = cmenu.addAction("Deselect")

                def deselect_func():
                    self.clearSelection()

                deselect.triggered.connect(deselect_func)
        except Exception as e:
            print(e)
        cmenu.exec_(self.viewport().mapToGlobal(event.pos()))
