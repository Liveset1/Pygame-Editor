import sys
import ctypes
import pygame as pg

from WidgetMod import *
from ctypes import wintypes
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

# Change Taskbar Icon using app_ids and AppUserModel
my_app_id = u'Indention.PyLight.Engine.1'  # arbitrary string
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(my_app_id)
lpBuffer = wintypes.LPWSTR()
AppUserModelID = ctypes.windll.shell32.GetCurrentProcessExplicitAppUserModelID
AppUserModelID(ctypes.cast(ctypes.byref(lpBuffer), wintypes.LPWSTR))
app_id = lpBuffer.value
ctypes.windll.kernel32.LocalFree(lpBuffer)


class ImageWidget(QWidget):
    def __init__(self, surface, parent=None):
        super(ImageWidget, self).__init__(parent)
        w = surface.get_width()
        h = surface.get_height()
        self.data = surface.get_buffer().raw
        self.image = QImage(self.data, w, h, QImage.Format_RGB32)
        
    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        qp.drawImage(100, 100, self.image)
        qp.end()


class MainWindow(QMainWindow):
    def __init__(self, surface, parent=None):
        super(MainWindow, self).__init__(parent)

        # Properties of Window
        self.__width__ = 1600
        self.__height__ = 1000

        # Width and Height for Dock
        self.DockMinWidth = 200
        self.DockMaxWidth = 300
        self.DockMinHeight = 100
        self.DockMaxHeight = self.__height__

        # Set Properties
        self.resize(self.__width__, self.__height__)
        self.showMaximized()

        # Tab Widget and GameWidget
        self.TabWidget = QTabWidget(self)
        self.resize(self.__width__, self.__height__)
        self.GameWidget = ImageWidget(surface)
        self.TabWidget.addTab(self.GameWidget, "Game")
        self.setCentralWidget(self.TabWidget)

        # creating a Hierarchy Widget Object
        self.HierarchyWidget = QWidget()
        self.HierarchyWidget.setEnabled(True)
        # create a Treeview Object
        self.HierarchyTreeView = TreeView(
            self.HierarchyWidget,
            [StandardItem("WorldSpace", 10, False, QColor(128, 128, 128),
                          QIcon(os.path.join(BASEDIR, "../Assets/Images/Icons/Window/WorldSpaceIcon.png")))]
        )

        self.HierarchyWidget.installEventFilter(self.HierarchyWidget)
        # Hierarchy Dock
        self.HierarchyDock = QDockWidget(self)
        self.HierarchyDock.setWindowTitle("Hierarchy")
        self.HierarchyDock.setMinimumSize(self.DockMinWidth, self.DockMinHeight)
        self.HierarchyDock.setMaximumSize(self.DockMaxWidth, self.DockMaxHeight)
        self.HierarchyDock.setAllowedAreas(Qt.DockWidgetArea.AllDockWidgetAreas)
        self.HierarchyDock.setFeatures(QDockWidget.AllDockWidgetFeatures)
        self.HierarchyDock.setWidget(self.HierarchyWidget)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.HierarchyDock)
        self.HierarchyDock.setFloating(False)

        # Layout
        self.HierarchyLayout = QHBoxLayout(self.HierarchyWidget)
        self.HierarchyLayout.addWidget(self.HierarchyTreeView)
        self.HierarchyWidget.setLayout(self.HierarchyLayout)

pg.init()
surface = pg.Surface((1600, 1000))
surface.fill((64, 128, 192, 224))
circle = pg.draw.circle(surface, (255, 255, 255, 255), (100, 100), 50)

app = QApplication(sys.argv)
w = MainWindow(surface)
w.show()
app.exec_()
