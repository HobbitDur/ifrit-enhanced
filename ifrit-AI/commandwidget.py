from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QPushButton, QSpinBox, QFrame, QSizePolicy, QLabel

from command import Command

class OpIdChangedEmmiter(QObject):
    op_id_signal = pyqtSignal()

class CommandWidget(QWidget):
    MAX_COMMAND_PARAM = 7
    MAX_OP_ID = 61
    MAX_OP_CODE_VALUE = 255
    MIN_OP_CODE_VALUE = 0
    def __init__(self, command:Command):
        QWidget.__init__(self)
        # signal
        self.op_id_changed_signal_emitter = OpIdChangedEmmiter()

        self.main_layout = QHBoxLayout()
        self.setLayout(self.main_layout)
        self.command = command

        # op_id widget
        self.op_id_widget = QSpinBox()
        self.op_id_widget.setFixedSize(50, 30)
        self.op_id_widget.setValue(command.get_id())
        self.op_id_widget.setMaximum(self.MAX_OP_ID)
        self.op_id_widget.valueChanged.connect(self.__op_id_change)
        self.op_id_widget.wheelEvent = lambda event: None

        # Line for cool gui
        frame = QFrame()
        frame.setFrameStyle(0x05)
        frame.setLineWidth(2)
        self.layout_id = QHBoxLayout()
        self.layout_id.addWidget(self.op_id_widget)
        self.layout_id.addWidget(frame)

        # Create the op_code widgets
        self.layout_op_code = QHBoxLayout()
        self.widget_op_code = []
        self.__reset_op_code_widget()

        #And the cool line with it
        self.frame_text = QFrame()
        self.frame_text.setFrameStyle(0x05)
        self.frame_text.setLineWidth(2)



        # Now the text
        self.layout_text = QHBoxLayout()
        self.widget_text = QLabel(command.get_text())
        self.layout_text_spacing = QHBoxLayout()
        self.layout_text.addLayout(self.layout_text_spacing)
        self.layout_text.addWidget(self.widget_text)

        self.layout_stretch = QHBoxLayout()
        self.layout_stretch.addStretch(1)

        self.main_layout.addLayout(self.layout_id)
        self.main_layout.addLayout(self.layout_op_code)
        self.main_layout.addWidget(self.frame_text)
        self.main_layout.addLayout(self.layout_text)
        self.main_layout.addLayout(self.layout_stretch)

    def set_text(self):
        self.widget_text.setText(self.command.get_text())


    def set_if_index(self, if_index):
        self.command.set_if_index(if_index)
        self.layout_text_spacing.takeAt(0)
        self.layout_text_spacing.addSpacing(if_index*20)

    def __op_id_change(self):
        self.command.set_op_id(self.op_id_widget.value())
        size = [x for x in self.command.game_data.ai_data_json["op_code_info"] if x['op_code'] == self.command.get_id()]
        if size:
            size = size[0]['size']
        else:
            size = [x for x in self.command.game_data.ai_data_json["op_code_info"] if x['op_code'] == 255][0]['size']
        self.command.set_op_code([0] * size)
        self.__reset_op_code_widget()
        self.widget_text.setText(self.command.get_text())
        self.op_id_changed_signal_emitter.op_id_signal.emit()


    def __op_code_change(self):
        op_code = []
        for widget in self.widget_op_code:
            op_code.append(widget.value())
        self.command.set_op_code(op_code)
        self.widget_text.setText(self.command.get_text())

    def __reset_op_code_widget(self):
        for widget in self.widget_op_code:
            widget.setParent(None)
            widget.deleteLater()
        self.widget_op_code = []
        for i in range(self.MAX_COMMAND_PARAM):
            self.widget_op_code.append(QSpinBox())
            self.widget_op_code[i].setFixedSize(50, 30)
            self.widget_op_code[i].setMaximum(self.MAX_OP_CODE_VALUE)
            self.widget_op_code[i].setMinimum(self.MIN_OP_CODE_VALUE)
            self.widget_op_code[i].wheelEvent = lambda event: None
            if i < len(self.command.get_op_code()):
                self.widget_op_code[i].setValue(self.command.get_op_code()[i])
            else:
                self.widget_op_code[i].setValue(0)
                retain_policy = QSizePolicy()
                retain_policy.setRetainSizeWhenHidden(True)
                self.widget_op_code[i].setSizePolicy(retain_policy)
                self.widget_op_code[i].hide()
            self.widget_op_code[i].valueChanged.connect(lambda: self.__op_code_change())

        for widget in self.widget_op_code:
            self.layout_op_code.addWidget(widget)
