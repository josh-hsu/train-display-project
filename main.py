import sys, os
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout,
    QPushButton
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

from osaka_metro.osaka_metro import *
from line_info import LineInfo
from osaka_metro_main import OsakaMetroTrainDisplay
from route_director import RouteDirector

class TrainDisplay(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("車廂顯示器模擬")
        self.setFixedSize(960, 512 + 50)
        self.setStyleSheet("background-color: #ffffff;")    
        self.initUI()

    def initLineInfo(self):
        line_file = MIDOSUJI_LINE_INFO
        self.line_info = LineInfo(line_file)

    def initUI(self):
        # 字體預設
        family = FONT_NAME
        debug_font = QFont(family, 14, QFont.Bold)
        
        # Osaka Metro Main view
        self.operator_main = OsakaMetroTrainDisplay(MIDOSUJI_LINE_INFO, 4)
        self.operator_main.operation_route_callback.connect(self.operation_callback)
        self.route_director = self.operator_main.director

        #
        # Debug 階段
        #
        debug_layout = QHBoxLayout()
        debug_layout.setContentsMargins(0, 0, 0, 0)
        debug_layout.setAlignment(Qt.AlignLeft)

        self.debug_text = QLabel("Debug message: testing ...")
        self.debug_text.setFont(debug_font)
        self.debug_text.setFixedSize(700, 50)
        self.debug_text.setStyleSheet(f"background-color: {WHITE_BACKGROUND_COLOR}; color: {GREY_COLOR};")

        self.debug_next_stage_button = QPushButton("Next stage")
        self.debug_next_stage_button.setFixedSize(100, 50)
        self.debug_next_stage_button.setStyleSheet("background-color: #ffffff; color: #000000;")
        self.debug_next_stage_button.clicked.connect(self.do_next_stage)

        self.debug_start_over_button = QPushButton("Start over")
        self.debug_start_over_button.setFixedSize(100, 50)
        self.debug_start_over_button.setStyleSheet("background-color: #ffffff; color: #000000;")
        self.debug_start_over_button.clicked.connect(self.do_start_over)
        
        debug_layout.addWidget(self.debug_text)
        debug_layout.addWidget(self.debug_next_stage_button)
        debug_layout.addWidget(self.debug_start_over_button)

        #
        # 主垂直布局
        #
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        main_layout.addWidget(self.operator_main)
        main_layout.addLayout(debug_layout)

        self.setLayout(main_layout)
    
    def operation_callback(self, object):
        station = object[0]
        state = object[1]
        elapsed_time = object[2]
        self.debug_text.setText(f"Route Director Callback: {station}, {state}, timestamp {elapsed_time}")

    def do_next_stage(self):
        self.route_director.elapsed_time += 40
    
    def do_start_over(self):
        self.route_director.elapsed_time = 0

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TrainDisplay()
    window.show()
    sys.exit(app.exec_())