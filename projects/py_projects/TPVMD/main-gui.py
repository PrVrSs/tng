from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, qApp
from gui.main_window import MainWindow
from gui.main_window_slots import MainWindowSlots
from PyQt5.QtCore import QThreadPool


class Main(QtWidgets.QMainWindow, MainWindowSlots):

    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent=parent)
        self.ui = MainWindow()
        self.ui.setup_ui(self)
        # self.ui.mdiArea.subWindowActivated.connect(self.updateMenus)
        self.ui.windowMapper.mapped[QWidget].connect(self.setActiveSubWindow)
        self.ui.choice_interface.triggered.connect(self.newFile)
        self.ui.exit_action.triggered.connect(qApp.quit)
        self.threadpool = QThreadPool()
        self.ui.open_act.triggered.connect(self.open)
        self.ui.save_act.triggered.connect(self.save)
        self.ui.save_as_act.triggered.connect(self.saveAs)
        # self.ui.new_act.triggered.connect()
        self.ui.cut_act.triggered.connect(self.cut)
        self.ui.copy_act.triggered.connect(self.copy)
        self.ui.paste_act.triggered.connect(self.paste)
        # self.ui.about_program_act.triggered.connect(self)


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    mainWin = Main()
    mainWin.show()
    sys.exit(app.exec_())
