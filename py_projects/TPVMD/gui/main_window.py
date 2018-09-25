from PyQt5 import QtCore
from PyQt5.QtGui import QIcon, QPalette, QColor
from PyQt5.QtWidgets import (QAction, QSizePolicy,
                             QHBoxLayout, qApp, QWidget, QTabWidget, QPushButton)
from PyQt5.QtCore import (QFile, QFileInfo, QPoint, QSettings, QSignalMapper,
        QSize, QTextStream, Qt)
from PyQt5.QtGui import QIcon, QKeySequence
from PyQt5.QtWidgets import (QAction, QApplication, QFileDialog, QMainWindow,
        QMdiArea, QMessageBox, QTextEdit, QWidget)


class MainWindow(object):

    def __init__(self):
        self.main_window_tab_table = QTabWidget()
        self.hbox = QHBoxLayout()
        self.but = QPushButton('Add')
        self.file_menu = None
        self.help_menu = None
        self.about_qt = None
        self.exit_action = None
        self.choice_interface = None

    def setup_ui(self, main_window):
        self.main_window = main_window
        main_window.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        red, green, blue = 11, 7, 11
        main_window.setPalette(QPalette(QColor(red, green, blue)))
        self.mdiArea = QMdiArea()
        self.mdiArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.mdiArea.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.create_menu(main_window)
        self.create_tool_bars(main_window)
        main_window.setCentralWidget(self.mdiArea)
        self.windowMapper = QSignalMapper(main_window)

    def file_menu_action(self):

        self.exit_action = QAction(QIcon('../resources/icons/fileclose.png'), "&Exit", self.file_menu)
        self.exit_action.setShortcut('Ctrl+Q')
        self.exit_action.setStatusTip('Exit application')
        # self.exitAct = QAction("E&xit", self, shortcut=QKeySequence.Quit,
        #                       statusTip="Exit the application",
        #                       triggered=QApplication.instance().closeAllWindows)
        self.choice_interface = QAction(QIcon('../resources/icons/ethernet_card_vista.png'), '&New Table', self.file_menu)
        self.choice_interface.setShortcut('Ctrl+A')
        self.choice_interface.setStatusTip('Exit application')
        # create new table
        self.new_act = QAction(QIcon(':/images/new.png'), "&New", self.file_menu)
        self.new_act.setShortcut('Ctrl+Q')
        self.new_act.setStatusTip('Create a new file')
        # triggered=self.open
        self.open_act = QAction(QIcon(':/images/open.png'), "&Open", self.file_menu)
        self.open_act.setShortcut(QKeySequence.Open)
        self.open_act.setStatusTip('Open an existing file')
        # triggered=self.save
        self.save_act = QAction(QIcon(':/images/save.png'), "&Save", self.file_menu)
        self.save_act.setShortcut(QKeySequence.Save)
        self.save_act.setStatusTip('Save the table to disk')
        # triggered=self.saveAs
        self.save_as_act = QAction(QIcon(':/images/save.png'), "&Save &As", self.file_menu)
        self.save_as_act.setShortcut(QKeySequence.SaveAs)
        self.save_as_act.setStatusTip('Save the document under a new name')
        # triggered=self.cut
        self.cut_act = QAction(QIcon(':/images/save.png'), "&Cut", self.file_menu)
        self.cut_act.setShortcut(QKeySequence.Cut)
        self.cut_act.setStatusTip('Cut the current selections contents to the clipboard')
        # triggered=self.copy
        self.copy_act = QAction(QIcon(':/images/save.png'), "&Copy", self.file_menu)
        self.copy_act.setShortcut(QKeySequence.Copy)
        self.copy_act.setStatusTip('Copy the current selections contents to the clipboard')
        # triggered=self.paste
        self.paste_act = QAction(QIcon(':/images/save.png'), "&Paste", self.file_menu)
        self.paste_act.setShortcut(QKeySequence.Paste)
        self.paste_act.setStatusTip('Paste the clipboards contents into the current selection')
        self.close_act = QAction(QIcon(':/images/save.png'), "&Close", self.file_menu)
        self.close_act.setStatusTip('Close the active window')
        self.close_act.triggered.connect(self.mdiArea.closeActiveSubWindow)
        self.close_all_act = QAction(QIcon(':/images/save.png'), "&Close &All", self.file_menu)
        self.close_all_act.setStatusTip('Close all the windows')
        self.close_all_act.triggered.connect(self.mdiArea.closeAllSubWindows)
        self.tile_act = QAction(QIcon(':/images/save.png'), "&Tile", self.file_menu)
        self.tile_act.setStatusTip('Tile the windows')
        self.tile_act.triggered.connect(self.mdiArea.tileSubWindows)
        self.cascade_act = QAction(QIcon(':/images/save.png'), "&Cascade", self.file_menu)
        self.cascade_act.setStatusTip('Cascade the windows')
        self.cascade_act.triggered.connect(self.mdiArea.cascadeSubWindows)
        self.next_act = QAction(QIcon(':/images/save.png'), "&Next", self.file_menu)
        self.next_act.setShortcut(QKeySequence.NextChild)
        self.next_act.setStatusTip('Move the focus to the next window')
        self.next_act.triggered.connect(self.mdiArea.activateNextSubWindow)
        self.previous_act = QAction(QIcon(':/images/save.png'), "&Previous", self.file_menu)
        self.previous_act.setShortcut(QKeySequence.PreviousChild)
        self.previous_act.setStatusTip('Move the focus to the previous window')
        self.previous_act.triggered.connect(self.mdiArea.activatePreviousSubWindow)
        # triggered=self.about

        # self.separatorAct = QAction(self)
        # self.separatorAct.setSeparator(True)

    def help_menu_action(self):
        self.about_qt = QAction(QIcon('../resources/icons/info.png'), '&About Qt', self.help_menu)
        self.about_qt.setShortcut('Ctrl+L')
        self.about_qt.setStatusTip('Show the Qt librarys About box')
        self.about_qt.triggered.connect(qApp.aboutQt)
        # self.aboutQtAct = QAction("About &Qt", self,
        #                           statusTip="Show the Qt library's About box",
        #                           triggered=QApplication.instance().aboutQt)
        self.about_program_act = QAction(QIcon(':/images/save.png'), "&About Program", self.file_menu)
        self.about_program_act.setStatusTip('Show the applications About box')

    def create_menu(self, main_window):
        self.file_menu = main_window.menuBar().addMenu("&File")
        self.file_menu_action()
        self.file_menu.addAction(self.choice_interface)
        self.file_menu.addAction(self.exit_action)
        self.file_menu.addAction(self.new_act)
        self.file_menu.addAction(self.open_act)
        self.file_menu.addAction(self.save_act)
        self.file_menu.addAction(self.save_as_act)
        # self.fileMenu.addSeparator()
        self.help_menu = main_window.menuBar().addMenu("&Help")
        self.help_menu_action()
        self.help_menu.addAction(self.about_qt)
        self.help_menu.addAction(self.about_program_act)

        self.editMenu = main_window.menuBar().addMenu("&Edit")
        self.editMenu.addAction(self.cut_act)
        self.editMenu.addAction(self.copy_act)
        self.editMenu.addAction(self.paste_act)

        self.windowMenu = main_window.menuBar().addMenu("&Window")
        self.updateWindowMenu()
        self.windowMenu.aboutToShow.connect(self.updateWindowMenu)

        # self.menuBar().addSeparator()

    def about(self):
        QMessageBox.about(self, "About MDI",
                          "The <b>MDI</b> example demonstrates how to write multiple "
                          "document interface applications using Qt.")

    def updateMenus(self):
        hasMdiChild = (self.activeMdiChild() is not None)
        self.save_act.setEnabled(hasMdiChild)
        self.save_as_act.setEnabled(hasMdiChild)
        self.paste_act.setEnabled(hasMdiChild)
        self.close_act.setEnabled(hasMdiChild)
        self.close_all_act.setEnabled(hasMdiChild)
        self.tile_act.setEnabled(hasMdiChild)
        self.cascade_act.setEnabled(hasMdiChild)
        self.next_act.setEnabled(hasMdiChild)
        self.previous_act.setEnabled(hasMdiChild)
        # self.separator_act.setVisible(hasMdiChild)

        hasSelection = (self.activeMdiChild() is not None and
                        self.activeMdiChild().textCursor().hasSelection())
        self.cut_act.setEnabled(hasSelection)
        self.copy_act.setEnabled(hasSelection)

    def updateWindowMenu(self):
        self.windowMenu.clear()
        self.windowMenu.addAction(self.close_act)
        self.windowMenu.addAction(self.close_all_act)
        self.windowMenu.addSeparator()
        self.windowMenu.addAction(self.tile_act)
        self.windowMenu.addAction(self.cascade_act)
        self.windowMenu.addSeparator()
        self.windowMenu.addAction(self.next_act)
        self.windowMenu.addAction(self.previous_act)
        # self.windowMenu.addAction(self.separator_act)

        windows = self.mdiArea.subWindowList()
        # self.separator_act.setVisible(len(windows) != 0)

        for i, window in enumerate(windows):
            child = window.widget()

            text = "%d %s" % (i + 1, child.userFriendlyCurrentFile())
            if i < 9:
                text = '&' + text

            action = self.windowMenu.addAction(text)
            action.setCheckable(True)
            action.setChecked(child is self.main_window.activeMdiChild())
            action.triggered.connect(self.windowMapper.map)
            self.windowMapper.setMapping(action, window)

    # def switchLayoutDirection(self):
    #    if self.layoutDirection() == Qt.LeftToRight:
    #        QApplication.setLayoutDirection(Qt.RightToLeft)
    #    else:
    #        QApplication.setLayoutDirection(Qt.LeftToRight)
    '''
    def createMenus(self):
        self.fileMenu = self.menuBar().addMenu("&File")
        self.fileMenu.addAction(self.newAct)
        self.fileMenu.addAction(self.openAct)
        self.fileMenu.addAction(self.saveAct)
        self.fileMenu.addAction(self.saveAsAct)
        self.fileMenu.addSeparator()
        action = self.fileMenu.addAction("Switch layout direction")
        action.triggered.connect(self.switchLayoutDirection)
        self.fileMenu.addAction(self.exitAct)

        self.editMenu = self.menuBar().addMenu("&Edit")
        self.editMenu.addAction(self.cutAct)
        self.editMenu.addAction(self.copyAct)
        self.editMenu.addAction(self.pasteAct)

        self.windowMenu = self.menuBar().addMenu("&Window")
        self.updateWindowMenu()
        self.windowMenu.aboutToShow.connect(self.updateWindowMenu)

        self.menuBar().addSeparator()

        self.helpMenu = self.menuBar().addMenu("&Help")
        self.helpMenu.addAction(self.aboutAct)
        self.helpMenu.addAction(self.aboutQtAct)
    '''

    def create_tool_bars(self, main_window):
        self.file_tool_bar = main_window.addToolBar("File")
        self.file_tool_bar.addAction(self.new_act)
        self.file_tool_bar.addAction(self.open_act)
        self.file_tool_bar.addAction(self.save_act)

        self.edit_tool_bar = main_window.addToolBar("Edit")
        self.edit_tool_bar.addAction(self.cut_act)
        self.edit_tool_bar.addAction(self.copy_act)
        self.edit_tool_bar.addAction(self.paste_act)

    # def createStatusBar(self):
    #     self.statusBar().showMessage("Ready")

    # def readSettings(self):
    #     settings = QSettings('Trolltech', 'MDI Example')
    #    pos = settings.value('pos', QPoint(200, 200))
    #    size = settings.value('size', QSize(400, 400))
    #    self.move(pos)
    #    self.resize(size)

    #def writeSettings(self):
    #    settings = QSettings('Trolltech', 'MDI Example')
    #    settings.setValue('pos', self.pos())
    #    settings.setValue('size', self.size())



