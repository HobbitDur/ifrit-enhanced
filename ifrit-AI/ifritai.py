import copy
import os

from PyQt6 import sip
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon, QFont
from PyQt6.QtWidgets import QWidget, QPushButton, QVBoxLayout, QLabel, QFrame, QComboBox, QHBoxLayout, QFileDialog, \
    QSpinBox, QGridLayout, QScrollArea, QSizePolicy, QStyle, QStyleFactory

from ifritmanager import IfritManager


class IfritAI(QWidget):
    ADD_LINE_SELECTOR_ITEMS = ["Condition", "Command"]
    MAX_COMMAND_PARAM = 7
    MAX_OP_ID = 61
    MAX_OP_CODE_VALUE = 255
    MIN_OP_CODE_VALUE = 0

    def __init__(self, icon_path='Resources'):

        QWidget.__init__(self)

        self.if_column_index = 0
        self.window_layout = QVBoxLayout()
        self.scroll_widget = QWidget()
        self.scroll_area = QScrollArea()
        self.window_layout.addWidget(self.scroll_area)
        # self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        # self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.scroll_widget)
        self.ifrit_manager = IfritManager()
        self.file_path = ""
        # Main window
        self.setWindowTitle("IfritAI")
        self.setMinimumSize(1280, 720)
        # self.setWindowIcon(QIcon(os.path.join(icon_path, 'icon.png')))

        self.save_button = QPushButton()
        self.save_button.setIcon(QIcon(os.path.join(icon_path, 'save.svg')))
        self.save_button.setFixedSize(30, 30)
        self.save_button.clicked.connect(self.__save_file)
        self.layout_main = QVBoxLayout()

        self.file_dialog = QFileDialog()
        self.file_dialog_button = QPushButton()
        self.file_dialog_button.setIcon(QIcon(os.path.join(icon_path, 'folder.png')))
        self.file_dialog_button.setFixedSize(30, 30)
        self.file_dialog_button.clicked.connect(self.__load_file)

        self.layout_top = QHBoxLayout()
        self.layout_top.addWidget(self.file_dialog_button)
        self.layout_top.addWidget(self.save_button)
        self.layout_top.addStretch(1)

        self.ai_layout = QVBoxLayout()
        self.all_lines_layout = []

        self.layout_title = QHBoxLayout()


        self.add_line_button = [QPushButton()]
        self.add_line_selector = [QComboBox()]
        #self.__init_add_line()
        self.add_line_layout = QHBoxLayout()
        # self.add_line_layout.addWidget(self.add_line_button)
        # self.add_line_layout.addWidget(self.add_line_selector)

        self.scroll_widget.setLayout(self.layout_main)
        self.layout_main.addLayout(self.layout_top)
        self.layout_main.addLayout(self.layout_title)
        self.layout_main.addLayout(self.ai_layout)
        # self.layout_main.addLayout(self.add_line_layout)

        self.setLayout(self.window_layout)

        self.__load_file()
        self.show()

    def __save_file(self):
        print("Save file")

    def __init_add_line(self):
        for i in range(len(self.add_line_button)):
            self.add_line_button[i].setText("+")
            #self.add_line_button[i].clicked.connect(lambda: self.__add_line(i))
            self.add_line_selector[i].addItems(self.ADD_LINE_SELECTOR_ITEMS)

    def __add_line(self, command):
        # First move the text if we got an END
        if command.get_id() == 35:
            self.if_column_index -= 1

        # If the line doesn't exist (so we are adding a new line not modifying one), create the layout
        if len(self.all_lines_layout) <= command.line_index:
            for i in range(command.line_index + 1 - len(self.all_lines_layout)):
                self.all_lines_layout.append(QHBoxLayout())
                self.layout_main.addLayout(self.all_lines_layout[-1])

        # Add the op_id widget
        command.op_id_widget = QSpinBox()
        command.op_id_widget.setFixedSize(50, 30)
        command.op_id_widget.setValue(command.get_id())
        command.op_id_widget.setMaximum(self.MAX_OP_ID)
        command.op_id_widget.valueChanged.connect(lambda: self.__op_id_change(command))

        # Line for cool gui
        frame = QFrame()
        frame.setFrameStyle(0x05)
        frame.setLineWidth(2)
        layout_id = QHBoxLayout()
        layout_id.addWidget(command.op_id_widget)
        layout_id.addWidget(frame)

        # Add the op_id to the line layout
        self.all_lines_layout[command.line_index].addLayout(layout_id)
        # Create the op_code widgets
        self.__reset_op_code_widget(command)

        # Create the text widget
        frame_text = QFrame()
        frame_text.setFrameStyle(0x05)
        frame_text.setLineWidth(2)
        command.text_widget = QLabel(command.get_text())
        layout_text = QHBoxLayout()
        layout_text.addWidget(frame_text)
        layout_text.addSpacing(20 * self.if_column_index)
        layout_text.addWidget(command.text_widget)
        self.all_lines_layout[command.line_index].addLayout(layout_text)

        # If an IF command, then move next text line a bit
        if command.get_id() == 2:  # IF
            self.if_column_index += 1

    def __reset_op_code_widget(self, command):
        command.op_code_widget = []
        for i in range(self.MAX_COMMAND_PARAM):
            command.op_code_widget.append(QSpinBox())
            command.op_code_widget[i].setFixedSize(50, 30)
            command.op_code_widget[i].setMaximum(self.MAX_OP_CODE_VALUE)
            command.op_code_widget[i].setMinimum(self.MIN_OP_CODE_VALUE)
            if i < len(command.get_op_code()):
                command.op_code_widget[i].setValue(command.get_op_code()[i])
            else:
                command.op_code_widget[i].setValue(0)
                retain_policy = QSizePolicy()
                retain_policy.setRetainSizeWhenHidden(True)
                command.op_code_widget[i].setSizePolicy(retain_policy)
                command.op_code_widget[i].hide()

            command.op_code_widget[i].valueChanged.connect(lambda: self.__op_code_change(command))
            self.all_lines_layout[command.line_index].addWidget(command.op_code_widget[i])

    def __op_id_change(self, command):
        command.set_op_id(command.op_id_widget.value())
        self.__clear_layout(self.all_lines_layout[command.line_index])
        self.__add_line(command)
        command.text_widget.setText(command.get_text())

    def __op_code_change(self, command):
        op_code = []
        for widget in command.op_code_widget:
            op_code.append(widget.value())
        command.set_op_code(op_code)
        command.text_widget.setText(command.get_text())

    def __load_file(self):
        # file_name = self.file_dialog.getOpenFileName(parent=self, caption="Search dat file", filter="*.dat", directory=os.getcwd())[0]
        # if file_name:
        #    self.file_path = file_name
        # self.ifrit_manager.init_from_file(file_name)
        self.ifrit_manager.init_from_file(os.path.join("OriginalFiles", "c0m028.dat"))
        line_index = 1
        self.__clear_lines()
        for code_section in self.ifrit_manager.ai_data:
            for command in code_section:
                command.line_index = line_index
                self.__add_line(command)
                line_index += 1

    def __clear_lines(self):
        for line_layout in self.all_lines_layout:
            self.__clear_layout(line_layout)

    def __clear_layout(self, layout):
        if layout:
            for i in reversed(range(layout.count())):
                item = layout.itemAt(i)
                widget = item.widget()
                sub_layout = item.layout()
                if sub_layout:
                    self.__clear_layout(sub_layout)
                    layout.removeItem(sub_layout)
                elif widget:
                    widget.setParent(None)
                    widget.deleteLater()


    def __set_title(self):
        font = QFont()
        font.setBold(True)
        label = QLabel("Command ID")
        label.setFont(font)
        self.layout_title.addWidget(label)
        label = QLabel("Op code")
        label.setFont(font)
        self.layout_title.addWidget(label)
        label = QLabel("Text")
        label.setFont(font)
        self.layout_title.addWidget(label)
