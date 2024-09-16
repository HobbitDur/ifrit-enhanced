import copy
import os

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon, QFont
from PyQt6.QtWidgets import QWidget, QPushButton, QVBoxLayout, QLabel, QFrame, QComboBox, QHBoxLayout, QFileDialog, QSpinBox, QGridLayout, QScrollArea

from ifritmanager import IfritManager


class IfritAI(QWidget):
    ADD_LINE_SELECTOR_ITEMS = ["Condition", "Command"]
    MAX_COMMAND_PARAM = 7

    def __init__(self, icon_path='Resources'):

        QWidget.__init__(self)
        self.if_column_index = 0
        self.window_layout = QVBoxLayout()
        self.scroll_widget = QWidget()
        self.scroll_area = QScrollArea()
        self.window_layout.addWidget(self.scroll_area)
        #self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        #self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.scroll_widget)
        self.ifrit_manager = IfritManager()
        self.file_path = ""
        # Main window
        self.setWindowTitle("IfritAI")
        self.setMinimumSize(1280, 720)
        # self.setWindowIcon(QIcon(os.path.join(icon_path, 'icon.png')))

        self.layout_main = QVBoxLayout()

        self.file_dialog = QFileDialog()
        self.file_dialog_button = QPushButton()
        self.file_dialog_button.setIcon(QIcon(os.path.join(icon_path, 'folder.png')))
        self.file_dialog_button.setFixedSize(30, 30)
        self.file_dialog_button.clicked.connect(self.__load_file)

        self.ai_lines_layout = QGridLayout()

        self.__clear_layout(self.ai_lines_layout)


        self.add_line_button = [QPushButton()]
        self.add_line_selector = [QComboBox()]
        self.__init_add_line()
        self.add_line_layout = QHBoxLayout()
        # self.add_line_layout.addWidget(self.add_line_button)
        # self.add_line_layout.addWidget(self.add_line_selector)

        self.scroll_widget.setLayout(self.layout_main)
        self.layout_main.addWidget(self.file_dialog_button)
        self.layout_main.addLayout(self.ai_lines_layout)
        # self.layout_main.addLayout(self.add_line_layout)

        self.setLayout(self.window_layout)

        self.__load_file()
        self.show()

    def __init_add_line(self):
        for i in range(len(self.add_line_button)):
            self.add_line_button[i].setText("+")
            self.add_line_button[i].clicked.connect(lambda: self.__add_line(i))
            self.add_line_selector[i].addItems(self.ADD_LINE_SELECTOR_ITEMS)

    def __add_line(self, line_index, command):
        if command.get_id() == 35:
            self.if_column_index -= 1
        op_id_widget = QSpinBox()
        op_id_widget.setValue(command.get_id())
        op_id_widget.setMaximumWidth(40)
        frame = QFrame()
        frame.setFrameStyle(0x05)
        frame.setLineWidth(2)
        layout_id = QHBoxLayout()
        layout_id.addWidget(op_id_widget)
        layout_id.addWidget(frame)
        self.ai_lines_layout.addLayout(layout_id, line_index, 0)

        #self.ai_lines_layout.addWidget(op_id_widget, line_index, 0)
        column_index =1
        print(len(command.get_op_code()))
        for code in command.get_op_code():
            op_code_widget = QSpinBox()
            op_code_widget.setValue(code)
            op_code_widget.setMaximumWidth(40)
            op_code_widget.setMaximum(255)
            op_code_widget.setMinimum(0)
            op_code_widget.valueChanged.connect(lambda: self.__op_code_change(column_index-1))
            self.ai_lines_layout.addWidget(op_code_widget, line_index, column_index)
            column_index += 1

        frame_text = QFrame()
        frame_text.setFrameStyle(0x05)
        frame_text.setLineWidth(2)
        column_index = self.MAX_COMMAND_PARAM + 1
        text_widget = QLabel(command.get_text())
        layout_text = QHBoxLayout()
        layout_text.addWidget(frame_text)
        layout_text.addSpacing(20*self.if_column_index)
        layout_text.addWidget(text_widget)
        self.ai_lines_layout.addLayout(layout_text, line_index, column_index)
        if command.get_id() == 2: #IF
            self.if_column_index+=1

    def __op_code_change(self, index_op_code):
        print(index_op_code)

    def __load_file(self):
        # file_name = self.file_dialog.getOpenFileName(parent=self, caption="Search dat file", filter="*.dat", directory=os.getcwd())[0]
        # if file_name:
        #    self.file_path = file_name
        # self.ifrit_manager.init_from_file(file_name)

        self.ifrit_manager.init_from_file(os.path.join("OriginalFiles", "c0m028.dat"))

        print(self.ifrit_manager.ai_data)

        line_index = 1
        self.__clear_layout(self.ai_lines_layout)
        for code_section in self.ifrit_manager.ai_data:
            for command in code_section:
                print(command)
                self.__add_line(line_index, command)
                line_index+=1
        print(self.ai_lines_layout.count())

    def __clear_layout(self, layout):
        for i in reversed(range(layout.count())):
            layout.itemAt(i).widget().setParent(None)

        font = QFont()
        font.setBold(True)
        label = QLabel("Command ID")
        label.setFont(font)
        layout.addWidget(label, 0, 0, alignment=Qt.AlignmentFlag.AlignCenter)
        label = QLabel("Op code")
        label.setFont(font)
        layout.addWidget(label, 0, 1, 1, self.MAX_COMMAND_PARAM, alignment=Qt.AlignmentFlag.AlignCenter)
        label = QLabel("Text")
        label.setFont(font)
        layout.addWidget(label, 0, self.MAX_COMMAND_PARAM+1, alignment=Qt.AlignmentFlag.AlignCenter)
