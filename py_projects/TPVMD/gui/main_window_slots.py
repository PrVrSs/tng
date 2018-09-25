from gui.main_window import MainWindow
from PyQt5.QtWidgets import QWidget, QTableWidget, QHBoxLayout, QFileDialog
from PyQt5.QtCore import QFileInfo
from gui.mdi_child import MdiChild


class MainWindowSlots(MainWindow):

    def newFile(self):
        child = self.createMdiChild()
        child.newFile()
        child.show()

    def createMdiChild(self):
        child = MdiChild()
        self.ui.mdiArea.addSubWindow(child)
        #child.copyAvailable.connect(self.ui.cut_act.setEnabled)
        #child.copyAvailable.connect(self.ui.copy_act.setEnabled)
        return child

    def setActiveSubWindow(self, window):
        if window:
            self.ui.mdiArea.setActiveSubWindow(window)



    def open(self):
        fileName, _ = QFileDialog.getOpenFileName(self)
        if fileName:
            existing = self.findMdiChild(fileName)
            if existing:
                self.mdiArea.setActiveSubWindow(existing)
                return

            child = self.createMdiChild()
            if child.loadFile(fileName):
                self.statusBar().showMessage("File loaded", 2000)
                child.show()
            else:
                child.close()

    def save(self):
        if self.ui.activeMdiChild() and self.ui.activeMdiChild().save():
            self.ui.statusBar().showMessage("File saved", 2000)

    def saveAs(self):
        if self.activeMdiChild() and self.activeMdiChild().saveAs():
            self.ui.statusBar().showMessage("File saved", 2000)

    def cut(self):
        if self.ui.activeMdiChild():
            self.ui.activeMdiChild().cut()

    def copy(self):
        if self.ui.activeMdiChild():
            self.ui.activeMdiChild().copy()

    def paste(self):
        if self.ui.activeMdiChild():
            self.ui.activeMdiChild().paste()

    def activeMdiChild(self):
        activeSubWindow = self.ui.mdiArea.activeSubWindow()
        if activeSubWindow:
            return activeSubWindow.widget()
        return None

    def findMdiChild(self, fileName):
        canonicalFilePath = QFileInfo(fileName).canonicalFilePath()
        for window in self.ui.mdiArea.subWindowList():
            if window.widget().currentFile() == canonicalFilePath:
                return window
        return None

