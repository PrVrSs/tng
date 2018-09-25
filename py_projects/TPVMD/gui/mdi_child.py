from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QTextEdit, QTabWidget, QTableWidget, QWidget
from PyQt5.QtCore import QThreadPool, QAbstractTableModel, Qt, pyqtSignal
from PyQt5 import QtCore, QtGui
from gui.mdi_child_window import MDIChildWindow
from gui.mdi_child_slots import MDIWindowSlots
import operator

"""
class MdiChild(QTableWidget,  MDIWindowSlots):
    sequenceNumber = 1

    def __init__(self):
        QTableWidget.__init__(self)
        # super(MdiChild, self).__init__()
        self.ui = MDIChildWindow()
        self.ui.setup_ui(self)
        self.threadpool = QThreadPool()
        # self.document().contentsChanged.connect(self.documentWasModified)

        # self.setAttribute(Qt.WA_DeleteOnClose)
        # self.isUntitled = True
"""


class MdiChild(QWidget,  MDIWindowSlots):
    sequenceNumber = 1

    def __init__(self):
        QWidget.__init__(self)
        # super(MdiChild, self).__init__()
        self.ui = MDIChildWindow()
        self.ui.setup_ui(self)
        self.threadpool = QThreadPool()
        # self.document().contentsChanged.connect(self.documentWasModified)

        # self.setAttribute(Qt.WA_DeleteOnClose)
        # self.isUntitled = True