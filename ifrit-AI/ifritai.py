import os
import sys

from PyQt6 import sip
from PyQt6.QtCore import Qt, QCoreApplication, QThreadPool, QRunnable, QObject, pyqtSignal, pyqtSlot, QThread, QSignalBlocker
from PyQt6.QtGui import QIcon, QFont, QAction
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QCheckBox, QMessageBox, QProgressDialog, \
    QMainWindow, QProgressBar, QRadioButton, \
    QLabel, QFrame, QStyle, QSizePolicy, QButtonGroup, QComboBox, QHBoxLayout, QFileDialog, QToolBar

from ifritmanager import IfritManager


class IfritAI(QWidget):
    ADD_LINE_SELECTOR_ITEMS = ["Condition", "Command"]
    def __init__(self, icon_path='Resources'):

        QWidget.__init__(self)
        self.ifrit_manager = IfritManager()
        self.file_path = ""
        # Main window
        self.setWindowTitle("IfritAI")
        #self.setWindowIcon(QIcon(os.path.join(icon_path, 'icon.png')))

        self.layout_main = QVBoxLayout()

        self.file_dialog = QFileDialog()
        self.file_dialog_button = QPushButton()
        self.file_dialog_button.setIcon(QIcon(os.path.join(icon_path, 'folder.png')))
        self.file_dialog_button.setFixedSize(30, 30)
        self.file_dialog_button.clicked.connect(self.__load_file)


        self.ai_lines_layout = []


        self.add_line_button = [QPushButton()]
        self.add_line_selector = [QComboBox()]
        self.__init_add_line()

        self.add_line_layout = QHBoxLayout()
        #self.add_line_layout.addWidget(self.add_line_button)
        #self.add_line_layout.addWidget(self.add_line_selector)

        self.layout_main.addLayout(self.add_line_layout)

        self.setLayout(self.layout_main)

        self.ifrit_manager.init_from_file(os.path.join("OriginalFiles", "c0m028.dat"))
        self.show()



    def __init_add_line(self):
        for i in range(len(self.add_line_button)):
            self.add_line_button[i].setText("+")
            self.add_line_button[i].clicked.connect(lambda: self.__add_line(i))
            self.add_line_selector[i].addItems(self.ADD_LINE_SELECTOR_ITEMS)

    def __add_line(self, index):
        pass


    def __load_file(self):
        file_name = self.file_dialog.getOpenFileName(parent=self, caption="Search dat file", filter="*.dat", directory=os.getcwd())[0]
        if file_name:
            self.file_path = file_name

        self.ifrit_manager.init_from_file(file_name)

        print(self.ifrit_manager.ai_data)
