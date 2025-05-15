import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout
)
from PyQt5.QtGui import QPainter, QPen, QColor, QFont
from PyQt5.QtCore import Qt, QPropertyAnimation, QRect

from train_common.line_info import *
from osaka_metro.osaka_metro import *

# 單一車廂
class SingleCabWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(130, 50)
        self.text = None  # 初始不顯示文字

    def setLabel(self, text):
        self.text = text
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        pen = QPen(Qt.black, 2)
        painter.setPen(pen)
        if self.text and self.text == "5":
            painter.setBrush(Qt.red)
        else:
            painter.setBrush(Qt.transparent)
        painter.drawRect(1, 1, self.width() - 2, self.height() - 2)

        # 畫上文字（如有）
        if self.text:
            if self.text == "5":
                painter.setPen(QPen(Qt.white))
            else:
                painter.setPen(QPen(Qt.black))
            font = QFont(FONT_NAME, 28, QFont.Bold)
            painter.setFont(font)
            painter.drawText(self.rect(), Qt.AlignCenter, self.text)


# 十節車廂列車
class TrainCabWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.cabs = []
        layout = QHBoxLayout()
        layout.setSpacing(2)
        layout.setContentsMargins(0, 0, 0, 0)

        for i in range(10):
            cab = SingleCabWidget()
            self.cabs.append(cab)
            layout.addWidget(cab)
            if i == 4:
                layout.addSpacing(8)

        self.setLayout(layout)
        total_width = 10 * 130 + 9 * 2 + 8
        self.setFixedSize(total_width, 50)

    def labelRearFiveCabs(self, reset=False):
        for i in range(5):
            label = str(i + 1)
            if reset:
                self.cabs[9 - i].setLabel("")  # 從最右邊開始標 5→1
            else:
                self.cabs[9 - i].setLabel(label)


# 動畫容器：TrainMovingWidget
class TrainMovingWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(960, 80)
        self.setStyleSheet("background-color: white;")

        self.train_widget = TrainCabWidget()
        self.train_widget.setParent(self)

        self._setup_animation()

    def _setup_animation(self):
        # 動畫初始與結束位置
        self.start_x = self.width() - 130
        cab_full_width = 130 + 2
        self.end_x = -5 * cab_full_width

        self.animation = QPropertyAnimation(self.train_widget, b"geometry")
        self.animation.setDuration(1000)
        self.animation.setStartValue(QRect(self.start_x, 15, self.train_widget.width(), self.train_widget.height()))
        self.animation.setEndValue(QRect(self.end_x, 15, self.train_widget.width(), self.train_widget.height()))
        self.animation.finished.connect(self.onAnimationFinished)

        # 初始位置設定
        self.reset()

    def animate(self):
        self.animation.start()

    def reset(self):
        self.train_widget.setGeometry(self.start_x, 15, self.train_widget.width(), self.train_widget.height())
        self.train_widget.labelRearFiveCabs(reset=True)

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        painter.fillRect(self.rect(), QColor("#FFFFFF"))

        pen = QPen(Qt.black, 4)
        painter.setPen(pen)
        x_start = 0
        y_pos = 65
        line_len = 720
        painter.drawLine(x_start, y_pos, x_start + line_len, y_pos)

        pen = QPen(Qt.red, 4)
        painter.setPen(pen)
        y_pos = 69
        painter.drawLine(x_start, y_pos, x_start + line_len, y_pos)

    def onAnimationFinished(self):
        self.train_widget.labelRearFiveCabs()
        

class ExitInfoHeader(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedWidth(300)
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        font_title = QFont(FONT_NAME, 16, QFont.Bold)
        font_subtitle = QFont(FONT_NAME, 12, QFont.Bold)
        font_exit_number = QFont(FONT_NAME, 28, QFont.Bold)
        self.setStyleSheet("color: #000000; background-color: transparent;")
        
        self.should_present = False

        # 第一欄：南改札 / Ticket Gate
        col1 = QVBoxLayout()
        col1.setContentsMargins(0, 0, 0, 0)
        col1.setSpacing(0)
        self.gate_name_label = QLabel("")
        self.gate_name_label.setFont(font_title)
        self.gate_name_label.setAlignment(Qt.AlignCenter)
        self.gate_en_name_label = QLabel("")
        self.gate_en_name_label.setFont(font_subtitle)
        self.gate_en_name_label.setAlignment(Qt.AlignCenter)
        col1.addWidget(self.gate_name_label)
        col1.addWidget(self.gate_en_name_label)

        # 第二欄：出口 / Exit
        col2 = QVBoxLayout()
        col2.setContentsMargins(5, 0, 5, 0)
        self.exit_label = QLabel("")
        self.exit_label.setFont(font_title)
        self.exit_label.setAlignment(Qt.AlignCenter)
        self.exit_en_label = QLabel("")
        self.exit_en_label.setFont(font_subtitle)
        self.exit_en_label.setAlignment(Qt.AlignCenter)
        col2.addWidget(self.exit_label)
        col2.addWidget(self.exit_en_label)

        # 第三欄：數字（3 - 10）
        col3 = QVBoxLayout()
        col3.setContentsMargins(5, 0, 5, 0)
        self.exit_num_label = QLabel("")
        self.exit_num_label.setFont(font_exit_number)
        self.exit_num_label.setAlignment(Qt.AlignCenter)
        col3.addWidget(self.exit_num_label)

        layout.addLayout(col1)
        layout.addLayout(col2)
        layout.addLayout(col3)
        self.setLayout(layout)
    
    def set_info_header(self, gate_name="", number_text=""):
        gate_label="Ticket Gate"
        exit_text="出口"
        exit_label="Exit"
        if len(gate_name) > 0:
            self.gate_name_label.setText(gate_name)
            self.gate_en_name_label.setText(gate_label)
            self.exit_num_label.setText(number_text)
            self.exit_label.setText(exit_text)
            self.exit_en_label.setText(exit_label)
            self.should_present = True
            self.setStyleSheet("color: #000000; background-color: transparent;")
        else:
            self.gate_name_label.setText("")
            self.gate_en_name_label.setText("")
            self.exit_num_label.setText("")
            self.exit_label.setText("")
            self.exit_en_label.setText("")
            self.should_present = False
        self.paintEvent(None)
    
    def paintEvent(self, event):
        painter = QPainter(self)
        if self.should_present:
            painter.fillRect(self.rect(), QColor("#F2B73F"))
        else:
            painter.fillRect(self.rect(), QColor("#D9DBDC"))

class ExitInfoItem(QLabel):
    def __init__(self, text):
        super().__init__(text)
        font_title = QFont(FONT_NAME, 20, QFont.Bold)
        
        # 自動偵測是否有兩行（用 \n 判斷）
        if '\n' in text:
            self.setFixedSize(300, 68)
        else:
            self.setFixedSize(300, 32)
            
        self.setFont(font_title)
        self.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.setStyleSheet("color: #000000;  padding-left: 2px; background-color: transparent;")

class ExitInfo(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedWidth(300)

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(2)

        self.header = ExitInfoHeader()
        layout.addWidget(self.header)

        self.exit_info_col_1 = ExitInfoItem("")
        self.exit_info_col_2 = ExitInfoItem("")
        self.exit_info_col_3 = ExitInfoItem("")
        self.exit_info = [self.exit_info_col_1, self.exit_info_col_2, self.exit_info_col_3]

        layout.addWidget(self.exit_info_col_1)
        layout.addWidget(self.exit_info_col_2)
        layout.addWidget(self.exit_info_col_3)

        layout.addStretch()
        self.setLayout(layout)
    
    def set_exit_header(self, name, exit_num):
        self.header.set_info_header(name, exit_num)
    
    def set_exit_info(self, list):
        for i in range(len(list)):
            if i < 3:
                self.exit_info[i].setText(list[i])
            


# 出口資訊（保留白底）
class GateLayoutWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(960, 210)
        self.setStyleSheet("background-color: white;")

        layout = QHBoxLayout()
        layout.setContentsMargins(20, 10, 20, 10)
        layout.setSpacing(5)

        # 建立三個 ExitInfo
        self.exit_left = ExitInfo()
        self.exit_center = ExitInfo()
        self.exit_right = ExitInfo()

        layout.addWidget(self.exit_left)
        layout.addWidget(self.exit_center)
        layout.addWidget(self.exit_right)

        self.setLayout(layout)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), QColor("#D9DBDC"))


# 黑色訊息欄
class MessageInfoWidget(QLabel):
    def __init__(self):
        super().__init__()
        self.setFixedSize(960, 50)
        self.setFont(QFont(FONT_NAME, 28, QFont.Bold))
        self.setText("こちら側のドアが開きます")
        self.setStyleSheet("background-color: black; color: red;")
        self.setAlignment(Qt.AlignCenter)

# 主組合視圖
class GateInfoWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(960, 340)

        layout = QVBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)

        self.gate_info = GateLayoutWidget()
        self.train_view = TrainMovingWidget()
        self.message_info = MessageInfoWidget()

        layout.addWidget(self.gate_info)
        layout.addWidget(self.train_view)
        layout.addWidget(self.message_info)

        self.setLayout(layout)

    def on_scene_present(self):
        self.train_view.animate()

    def clean_all(self):
        left_panel = self.gate_info.exit_left
        left_panel.set_exit_header("", "")
        left_panel.set_exit_info(["", "", ""])
        right_panel = self.gate_info.exit_right
        right_panel.set_exit_header("", "")
        right_panel.set_exit_info(["", "", ""])


    def update_scene(self):
        exit_info = self.station.gate_info
        exit_info_detail = self.station.gate_info_detail

        self.clean_all()
        
        for gate_item in exit_info:
            gate_name = gate_item[0]
            gate_exit = str(gate_item[1])
            gate_detail = exit_info_detail[gate_name]
            print(f"name {gate_name}, exit {gate_exit}, detail {gate_detail}")
            
            if gate_name == "center" or gate_name == "central":
                left_panel = self.gate_info.exit_left
                left_panel.set_exit_header(GATE_NAME_MAP[gate_name], gate_exit)
                left_panel.set_exit_info(gate_detail)
            elif gate_name == "south" or gate_name == "east":
                right_panel = self.gate_info.exit_right
                right_panel.set_exit_header(GATE_NAME_MAP[gate_name], gate_exit)
                right_panel.set_exit_info(gate_detail)
            
        pass

    def on_scene_disappear(self):
        self.train_view.reset()

    def receive_notify(self, line_info, display_station, station_state):
        self.line_info = line_info
        self.station = display_station
        self.station_state = station_state
        self.update_scene()

# 執行主視窗
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GateInfoWidget()
    exit_info = window.gate_info.exit_center
    exit_info.set_exit_header("Test Gate", "3 ~ 7")
    exit_info.set_exit_info(["123", "456", "789"])
    window.on_scene_present()
    
    window.show()
    sys.exit(app.exec_())
