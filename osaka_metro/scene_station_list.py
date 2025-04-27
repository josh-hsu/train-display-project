# scene_station_list.py
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtGui import QPainter, QColor, QPainterPath
from auto_stretch_label import AutoStretchLabel
from vertical_label import VerticalText

class SideArrow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

    def paintEvent(self, event):
        painter = QPainter(self)
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

        painter.setBrush(QColor(227, 57, 55))
        painter.drawPath(complete_path)

        painter.end()

class SceneStationList(QWidget):
    def __init__(self):
        super().__init__()
        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        self.setStyleSheet("background-color: #F61826; 2px solid gray; ")
        self.setFixedSize(960, 342)
        self.sta_font = QFont("Noto Sans JP", 32, QFont.Bold)
        self.min_font = QFont("Noto Sans JP", 24, QFont.Bold)

        # top layout
        self.top_layout = QHBoxLayout()
        self.top_layout.setContentsMargins(0, 0, 0, 0)
        self.top_layout.setSpacing(0)
        self.sta_leftmost = QLabel("")
        self.sta_leftmost.setFixedSize(90, 150)
        self.sta_leftmost.setStyleSheet("background-color: #FFFFFF; border: 1px solid gray; color: #FFFFFF;")
        self.top_layout.addWidget(self.sta_leftmost)
        self.sta = []
        for i in range(13):
            label = VerticalText(f"")
            label.setStyleSheet("background-color: #FFFFFF; border: 1px solid gray; color: #000000;")
            label.setFixedSize(60, 150)
            label.setFont(self.sta_font)
            self.top_layout.addWidget(label)
            self.sta.append(label)
        self.sta_rightmost = QLabel("")
        self.sta_rightmost.setFixedSize(90, 150)
        self.sta_rightmost.setStyleSheet("background-color: #FFFFFF; border: 1px solid gray; color: #FFFFFF;")
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
        self.second_layout.addWidget(self.progress_leftmost)
        self.progress = []
        for i in range(13):
            label = AutoStretchLabel("")
            label.setAlignment(Qt.AlignCenter)
            label.setFixedSize(60, 36)
            label.setStyleSheet("background-color: #DD3636; border: 1px solid gray;")   
            self.progress.append(label)
            self.second_layout.addWidget(label)
        self.progress_rightmost = QLabel()
        self.progress_rightmost.setFixedSize(90, 36)
        self.progress_rightmost.setStyleSheet("background-color: #838383; border: 1px solid gray;")
        self.second_layout.addWidget(self.progress_rightmost)
        self.main_layout.addLayout(self.second_layout)

        # 3rd layout: minute time
        self.third_layout = QHBoxLayout()
        self.third_layout.setContentsMargins(0, 0, 0, 0)
        self.third_layout.setSpacing(0)
        self.min_leftmost = QLabel("約")
        self.min_leftmost.setAlignment(Qt.AlignCenter)
        self.min_leftmost.setFont(self.sta_font)
        self.min_leftmost.setFixedSize(90, 30)
        self.third_layout.addWidget(self.min_leftmost)
        self.min = []
        for i in range(12):
            label = QLabel("")
            label.setAlignment(Qt.AlignCenter)
            label.setFixedSize(60, 30)
            label.setFont(self.min_font)
            label.setStyleSheet("background-color: #FFFFFF; border: 1px solid gray; color: #000000;")   
            self.min.append(label)
            self.third_layout.addWidget(label)
        self.min_rightmost = QLabel("")
        self.min_rightmost.setAlignment(Qt.AlignRight)
        self.min_rightmost.setFixedSize(150, 30)
        self.min_rightmost.setStyleSheet("background-color: #FFFFFF; border: 1px solid gray; color: #000000;")
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
        self.bottom_layout.addWidget(self.transfer_leftmost)
        self.transfer = []
        for i in range(6):
            label = QLabel("轉乘")
            label.setAlignment(Qt.AlignCenter)
            label.setFixedSize(120, 124)
            label.setStyleSheet("background-color: #FFFFFF; border: 1px solid gray; color: #000000;")   
            self.transfer.append(label)
            self.bottom_layout.addWidget(label)
        self.transfer_rightmost = QLabel("")
        self.transfer_rightmost.setAlignment(Qt.AlignRight)
        self.transfer_rightmost.setFixedSize(180, 124)
        self.transfer_rightmost.setStyleSheet("background-color: #FFFFFF; border: 1px solid gray; color: #000000;")
        self.bottom_layout.addWidget(self.transfer_rightmost)
        self.main_layout.addLayout(self.bottom_layout)
        
        self.setLayout(self.main_layout)