# scene_station_list.py
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout
from PyQt5.QtCore import Qt, QPoint, QTimer
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtGui import QPainter, QColor, QPainterPath
from PyQt5.QtGui import QBrush, QPolygon
from auto_stretch_label import AutoStretchLabel
from vertical_label import VerticalText
import os
from osaka_metro.osaka_metro import *

class SideArrow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(Qt.NoPen)
        w = self.width()
        h = self.height()
        leftside_arrow_offset = 40

        # 紅色進度條參數
        arrow_w = 20

        complete_path = QPainterPath()
        # Add left arrow
        complete_path.moveTo(leftside_arrow_offset, 0)
        complete_path.lineTo(leftside_arrow_offset - arrow_w, h/2)
        complete_path.lineTo(leftside_arrow_offset, h)
        # Add rectangle (continuing from arrow's last point)
        complete_path.lineTo(w, h)
        complete_path.lineTo(w, 0)
        complete_path.lineTo(leftside_arrow_offset, 0)
        complete_path.closeSubpath()

        painter.setBrush(QColor(MIDOSUJI_RED_COLOR))
        painter.drawPath(complete_path)

        painter.end()

class MovingArrow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(120, 40)  # 預設尺寸，可自己調整
        self.blue_is_red = False  # 目前藍色部分是不是變紅色

        # Timer
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.toggleBluePart)
        self.timer.start(1000)

    def toggleBluePart(self):
        self.blue_is_red = not self.blue_is_red
        self.update()  # 重新觸發 paintEvent

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(Qt.NoPen)

        # 紅色部分
        red_brush = QBrush(QColor(MIDOSUJI_RED_COLOR))
        painter.setBrush(red_brush)
        
        red1 = QPolygon([QPoint(0,0), QPoint(20,0), QPoint(0,18)])
        red2 = QPolygon([QPoint(0,18), QPoint(20,36), QPoint(0,36)])
        painter.drawPolygon(red1)
        painter.drawPolygon(red2)

        # 藍色部分
        if self.blue_is_red:
            painter.setBrush(QColor(MIDOSUJI_RED_COLOR))  # 當作紅色
        else:
            painter.setBrush(QColor(BLUE_COLOR))  # 正常藍色
    
        blue1 = QPolygon([
            QPoint(22,0), QPoint(2,18), QPoint(22,36),
            QPoint(33,36), QPoint(13,18), QPoint(33,0)
        ])
        blue2 = QPolygon([
            QPoint(35,0), QPoint(15,18), QPoint(35,36),
            QPoint(46,36), QPoint(26,18), QPoint(46,0)
        ])
        blue3 = QPolygon([
            QPoint(48,0), QPoint(28,18), QPoint(48,36),
            QPoint(59,36), QPoint(41,18), QPoint(59,0)
        ])
        painter.drawPolygon(blue1)
        painter.drawPolygon(blue2)
        painter.drawPolygon(blue3)

        # 灰色部分
        grey_brush = QBrush(QColor(GREY_COLOR))
        painter.setBrush(grey_brush)
        grey = QPolygon([
            QPoint(60,2), QPoint(43,18), QPoint(60,34)
        ])
        painter.drawPolygon(grey)

class TransferInfo(QWidget):
    def __init__(self, icon_names, station_names, icon_dir=ICON_PATH, parent=None):
        super().__init__(parent)

        self.icon_names = icon_names
        self.station_names = station_names
        self.icon_dir = icon_dir

        layout = QVBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setAlignment(Qt.AlignTop)

        self.line_font = QFont(FONT_NAME, 12)

        for icon_name, station_name in zip(icon_names, station_names):
            row = QHBoxLayout()
            row.setSpacing(0)
            row.setAlignment(Qt.AlignLeft)

            icon_path = os.path.join(self.icon_dir, ICON_MAP.get(icon_name, ""))
            print(f"Load path: {icon_path}")
            icon_label = QLabel()
            if os.path.exists(icon_path):
                pixmap = QPixmap(icon_path)
                icon_label.setPixmap(pixmap.scaled(24, 24, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            icon_label.setFixedSize(24, 24)
            icon_label.setScaledContents(True)

            text_label = AutoStretchLabel(station_name)
            text_label.setFont(self.line_font)
            text_label.setFixedSize(96, 24)
            text_label.setStyleSheet(f"background-color: {MIDOSUJI_BACKGROUND_COLOR}; color: #000000;")

            row.addWidget(icon_label)
            row.addWidget(text_label)
            layout.addLayout(row)

        self.setLayout(layout)

class SceneStationList(QWidget):
    def __init__(self):
        super().__init__()

        if (os.name == "posix"):
            family = "Noto Sans JP"
            self.sta_font = QFont(family, 32, QFont.Bold)
            self.min_font = QFont(family, 24, QFont.Bold)
        else:
            family = "Noto Sans JP SemiBold"
            self.sta_font = QFont(family, 28, QFont.Bold)
            self.min_font = QFont(family, 20, QFont.Bold)
        
        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        self.setStyleSheet(f"background-color: {MIDOSUJI_RED_COLOR};")
        self.setFixedSize(960, 342)
        
        # station names layout
        self.top_layout = QHBoxLayout()
        self.top_layout.setContentsMargins(0, 0, 0, 0)
        self.top_layout.setSpacing(0)
        self.sta_leftmost = QLabel("")
        self.sta_leftmost.setFixedSize(90, 150)
        self.sta_leftmost.setStyleSheet(f"background-color: {MIDOSUJI_BACKGROUND_COLOR}; color: {MIDOSUJI_BACKGROUND_COLOR};")
        self.top_layout.addWidget(self.sta_leftmost)
        self.sta = []
        for i in range(13):
            label = VerticalText(f"")
            label.setStyleSheet(f"background-color: {MIDOSUJI_BACKGROUND_COLOR}; color: {BLACK_COLOR};")
            label.setFixedSize(60, 150)
            label.setFont(self.sta_font)
            self.top_layout.addWidget(label)
            self.sta.append(label)
        self.sta_rightmost = QLabel("")
        self.sta_rightmost.setFixedSize(90, 150)
        self.sta_rightmost.setStyleSheet(f"background-color: {MIDOSUJI_BACKGROUND_COLOR}; color: {MIDOSUJI_BACKGROUND_COLOR};")
        self.top_layout.addWidget(self.sta_rightmost)
        self.main_layout.addLayout(self.top_layout)

        #######
        self.sta[0].setText("西中島南方")
        self.sta[2].setText("　中　津")
        self.sta[4].setText("　梅　田")
        self.sta[6].setText("　淀屋橋")
        self.sta[8].setText("　本　町")
        self.sta[10].setText("　心斎橋")
        self.sta[12].setText("　なんば")
        #######

        # 2nd layout: progress bar
        self.second_layout = QHBoxLayout()
        self.second_layout.setContentsMargins(0, 0, 0, 0)
        self.second_layout.setSpacing(0)
        self.progress_leftmost = SideArrow()
        self.progress_leftmost.setFixedSize(90, 36)
        self.progress_leftmost.setStyleSheet(f"background-color: {MIDOSUJI_RED_COLOR}; color: {MIDOSUJI_BACKGROUND_COLOR};")
        self.second_layout.addWidget(self.progress_leftmost)
        self.progress = []
        self.progress_index = 11
        for i in range(13):
            if i < self.progress_index:
                label = AutoStretchLabel("")
                label.setFont(self.min_font)
                label.setAlignment(Qt.AlignCenter)
                label.setFixedSize(60, 36)
                label.setStyleSheet(f"background-color: {MIDOSUJI_RED_COLOR}; color: {MIDOSUJI_BACKGROUND_COLOR};")
            elif i == self.progress_index:
                label = MovingArrow()
                label.setFixedSize(60, 36)
            else:
                label = QLabel("")
                label.setFont(self.min_font)
                label.setAlignment(Qt.AlignCenter)
                label.setFixedSize(60, 36)
                label.setStyleSheet(f"background-color: {GREY_COLOR}; color: {MIDOSUJI_BACKGROUND_COLOR};")

            self.progress.append(label)
            self.second_layout.addWidget(label)
        self.progress_rightmost = QLabel()
        self.progress_rightmost.setFixedSize(90, 36)
        self.progress_rightmost.setStyleSheet(f"background-color: {GREY_COLOR};")
        self.second_layout.addWidget(self.progress_rightmost)
        self.main_layout.addLayout(self.second_layout)

        #######
        self.progress[0].setText("M14")
        self.progress[2].setText("M15")
        self.progress[4].setText("M16")
        self.progress[6].setText("M17")
        self.progress[8].setText("M18")
        self.progress[10].setText("M19")
        self.progress[self.progress_index+1].setText("M20")
        #######

        # 3rd layout: minute time
        self.third_layout = QHBoxLayout()
        self.third_layout.setContentsMargins(0, 0, 0, 0)
        self.third_layout.setSpacing(0)
        self.min_leftmost = QLabel("約")
        self.min_leftmost.setAlignment(Qt.AlignCenter)
        self.min_leftmost.setFont(self.min_font)
        self.min_leftmost.setFixedSize(90, 30)
        self.min_leftmost.setStyleSheet(f"background-color: {MIDOSUJI_BACKGROUND_COLOR}; color: {BLACK_COLOR};")  
        self.third_layout.addWidget(self.min_leftmost)
        self.min = []
        for i in range(12):
            label = QLabel("")
            label.setAlignment(Qt.AlignCenter)
            label.setFixedSize(60, 30)
            label.setFont(self.min_font)
            label.setStyleSheet(f"background-color: {MIDOSUJI_BACKGROUND_COLOR}; color: {BLACK_COLOR};")   
            self.min.append(label)
            self.third_layout.addWidget(label)
        self.min_rightmost = QLabel("")
        self.min_rightmost.setAlignment(Qt.AlignRight)
        self.min_rightmost.setFixedSize(150, 30)
        self.min_rightmost.setFont(self.min_font)
        self.min_rightmost.setStyleSheet(f"background-color: {MIDOSUJI_BACKGROUND_COLOR}; color: {BLACK_COLOR};")
        self.third_layout.addWidget(self.min_rightmost)
        self.main_layout.addLayout(self.third_layout)

        ########
        self.min[0].setText("14")
        self.min[2].setText("11")
        self.min[4].setText("9")
        self.min[6].setText("6")
        self.min[8].setText("4")
        self.min[10].setText("2")
        self.min[11].setText("分")
        ########

        # 4th layout
        self.bottom_layout = QHBoxLayout()
        self.bottom_layout.setContentsMargins(0, 0, 0, 0)
        self.bottom_layout.setSpacing(0)
        self.transfer_leftmost = QLabel("")
        self.transfer_leftmost.setAlignment(Qt.AlignCenter)
        self.transfer_leftmost.setFont(self.sta_font)
        self.transfer_leftmost.setFixedSize(60, 124)
        self.transfer_leftmost.setStyleSheet(f"background-color: {MIDOSUJI_BACKGROUND_COLOR}; color: {BLACK_COLOR};")
        self.bottom_layout.addWidget(self.transfer_leftmost)
        self.transfer = []
        for i in range(6):
            icon_keys = ["Sennichimae", "Kintetsu", "Nankai"]
            station_names = ["Sennichimae Line  ", "近鐵線", "南海線"]
            transfer_info_widget = TransferInfo(icon_keys, station_names)
            transfer_info_widget.setFixedSize(120, 124)
            self.transfer.append(transfer_info_widget)
            self.bottom_layout.addWidget(transfer_info_widget)
        self.transfer_rightmost = QLabel("")
        self.transfer_rightmost.setAlignment(Qt.AlignRight)
        self.transfer_rightmost.setFixedSize(180, 124)
        self.transfer_rightmost.setStyleSheet(f"background-color: {MIDOSUJI_BACKGROUND_COLOR}; color: {BLACK_COLOR};")
        self.bottom_layout.addWidget(self.transfer_rightmost)
        self.main_layout.addLayout(self.bottom_layout)

        self.setLayout(self.main_layout)