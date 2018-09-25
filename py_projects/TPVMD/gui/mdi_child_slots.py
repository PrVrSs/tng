from gui.mdi_child_window import MDIChildWindow
# from AmkDataReader import ServerDataReader
from data_processing.data_reader.reader import Reader
import configparser
from PyQt5.QtWidgets import QTableWidgetItem, QApplication, QFileDialog, QMessageBox
from gui.my_threading import Worker
from PyQt5.QtCore import QFile, QFileInfo, QTextStream, Qt


class MDIWindowSlots(MDIChildWindow):

    sequenceNumber = 0

    def create_table(self, data):
        self.isUntitled = True
        self.curFile = "document%d.txt" % MDIWindowSlots.sequenceNumber
        MDIWindowSlots.sequenceNumber += 1
        self.setWindowTitle(self.curFile + '[*]')
        '''
        self.setRowCount(len(data))
        self.setColumnCount(len(data[0][1])+1)
        for index_i, i in enumerate(data):
            time_ = ''
            for j in i[0]:
                time_ += str(j)
            self.setItem(index_i, 0,  QTableWidgetItem(time_))
            for index_j, j in enumerate(i[1]):
                self.setItem(index_i, index_j+1, QTableWidgetItem(str(j)))
        '''
        list_ = tuple([tuple(list(d[0])+list(d[1])) for d in data])
        header_ = ("Year", "month", "day", "hour", "minute", "second", "millisecond",
                   "123", "12", "123", "12", "123", "12", "123", "12", "123", "12", "123", "12", "123", "12", "123")
        self.ui.table_model.setDataList(list_, header_)

    def get_data(self):
        config_file = 'config.ini'
        config_file_ = configparser.ConfigParser()
        config_file_.read(config_file)
        url = config_file_['program_setting']['url']
        observation_start = config_file_['program_setting']['observation_start']
        observation_end = config_file_['program_setting']['observation_end']
        reader = Reader()
        reader.set_read_from(read_from='server')
        data = reader.read_file(path_or_server=url, time_of_observation=observation_start + observation_end)
        return data

    def thread_complete(self):
        print("THREAD COMPLETE!")

    def newFile(self):
        worker = Worker(self.get_data)
        worker.signals.result.connect(self.create_table)
        worker.signals.finished.connect(self.thread_complete)
        self.threadpool.start(worker)

    def loadFile(self, fileName):
        pass

    def save(self):
        if self.isUntitled:
            return self.saveAs()
        else:
            return self.saveFile(self.curFile)

    def saveAs(self):
        fileName, _ = QFileDialog.getSaveFileName(self, "Save As", self.curFile)
        if not fileName:
            return False

        return self.saveFile(fileName)

    def saveFile(self, fileName):
        pass

    def userFriendlyCurrentFile(self):
        return self.strippedName(self.curFile)

    def currentFile(self):
        return self.curFile

    def closeEvent(self, event):
        event.accept()
        # if self.maybeSave():
        #     event.accept()
        # else:
        #     event.ignore()

    # def documentWasModified(self):
    #     self.setWindowModified(self.document().isModified())

    def maybeSave(self):
        if self.isModified():
            ret = QMessageBox.warning(self, "MDI",
                                      "'%s' has been modified.\nDo you want to save your "
                                      "changes?" % self.userFriendlyCurrentFile(),
                                      QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel)

            if ret == QMessageBox.Save:
                return self.save()

            if ret == QMessageBox.Cancel:
                return False

        return True

    def setCurrentFile(self, fileName):
        self.curFile = QFileInfo(fileName).canonicalFilePath()
        self.isUntitled = False
        self.document().setModified(False)
        self.setWindowModified(False)
        self.setWindowTitle(self.userFriendlyCurrentFile() + "[*]")

    def strippedName(self, fullFileName):
        return QFileInfo(fullFileName).fileName()
