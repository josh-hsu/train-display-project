import sys, os
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout,
    QPushButton, QComboBox
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

from osaka_metro.osaka_metro import *
from train_common.line_info import LineInfo
from osaka_metro_main import OsakaMetroTrainDisplay
from train_common.route_director import RouteDirector

class TrainDisplay(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("車廂顯示器模擬")
        self.setFixedSize(960, 512 + 80)
        self.setStyleSheet("background-color: #ffffff;")    
        self.initUI()

    def initUI(self):
        # 字體預設
        family = FONT_NAME
        debug_font = QFont(family, 14, QFont.Bold)
        
        # Osaka Metro Main view
        line_select = "Midosuji"
        self.line_file = f"{LINE_INFO_FILE_FOLDER}{LINE_INFO_FILE_PATH_MAP[line_select]}"
        self.line_info = LineInfo(self.line_file)
        self.line_route = 0
        self.operator_main = OsakaMetroTrainDisplay(self.line_file, self.line_route)
        self.operator_main.operation_route_callback.connect(self.operation_callback)
        self.operator_main.setFixedHeight(512)
        self.route_director = self.operator_main.director

        #
        # Debug 階段
        #
        control_panel = QWidget()
        control_layout = QVBoxLayout(control_panel)
        control_layout.setContentsMargins(0, 0, 0, 0)
        control_layout.setSpacing(0)
        
        debug_layout = QHBoxLayout()
        debug_layout.setContentsMargins(0, 0, 0, 0)
        debug_layout.setAlignment(Qt.AlignLeft)

        self.debug_text = QLabel("Debug message: testing ...")
        self.debug_text.setFont(debug_font)
        self.debug_text.setFixedSize(700, 30)
        self.debug_text.setStyleSheet(f"background-color: {WHITE_BACKGROUND_COLOR}; color: {GREY_COLOR};")

        self.debug_next_stage_button = QPushButton("+40秒")
        self.debug_next_stage_button.setFixedSize(100, 30)
        self.debug_next_stage_button.setStyleSheet("background-color: #ffffff; color: #000000;")
        self.debug_next_stage_button.clicked.connect(self.do_next_stage)

        self.debug_start_over_button = QPushButton("歸0")
        self.debug_start_over_button.setFixedSize(100, 30)
        self.debug_start_over_button.setStyleSheet("background-color: #ffffff; color: #000000;")
        self.debug_start_over_button.clicked.connect(self.do_start_over)
        
        debug_layout.addWidget(self.debug_text)
        debug_layout.addWidget(self.debug_next_stage_button)
        debug_layout.addWidget(self.debug_start_over_button)
        control_layout.addLayout(debug_layout)
        
        #
        # 路線選擇
        #
        line_layout = QHBoxLayout()
        line_layout.setContentsMargins(0, 0, 0, 0)
        line_layout.setSpacing(10)
        line_layout.setAlignment(Qt.AlignLeft)
        line_select_label = QLabel("選擇路線：")
        line_select_label.setStyleSheet("background-color: #ffffff; color: #000000;")
        line_select_label.setFixedSize(60, 30)
        line_layout.addWidget(line_select_label)
        self.line_combo = QComboBox()
        self.line_combo.setStyleSheet("background-color: #ffffff; color: #000000;")
        self.line_combo.setFixedSize(200, 30)
        self.line_combo.addItems(list(LINE_INFO_FILE_PATH_MAP.keys()))
        self.line_combo.currentIndexChanged.connect(self.change_operating_line)
        line_layout.addWidget(self.line_combo)
        self.route_combo = QComboBox()
        self.route_combo.setStyleSheet("background-color: #ffffff; color: #000000;")
        self.route_combo.setFixedSize(200, 30)
        self.route_combo.addItems([])
        self.route_combo.currentIndexChanged.connect(self.change_operating_line_route)
        line_layout.addWidget(self.route_combo)
        self.debug_start_line_button = QPushButton("開始此線路")
        self.debug_start_line_button.setFixedSize(100, 30)
        self.debug_start_line_button.setStyleSheet("background-color: #ffffff; color: #000000;")
        self.debug_start_line_button.clicked.connect(self.start_operating_line)
        line_layout.addWidget(self.debug_start_line_button)
        control_layout.addLayout(line_layout)

        #
        # 主垂直布局
        #
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        main_layout.addWidget(self.operator_main)
        main_layout.addWidget(control_panel)

        self.setLayout(main_layout)
        
        # 整理資料
        self.refresh_routes()
    
    def change_operating_line(self, index):
        line_list = list(LINE_INFO_FILE_PATH_MAP.keys())
        if 0 <= index < len(line_list):
            self.line_file = f"{LINE_INFO_FILE_FOLDER}{LINE_INFO_FILE_PATH_MAP[line_list[index]]}"
            self.line_info = LineInfo(self.line_file)
            self.refresh_routes()
            self.debug_text.setText(f"Select line: {self.line_file}")
    
    def refresh_routes(self):
        self.route_combo.clear()
        route_list = self.line_info.directions
        display_route_list = []
        for item in route_list:
            start = self.line_info.get_station(item[0]).name['zh-TW']
            end = self.line_info.get_station(item[1]).name['zh-TW']
            display_route_list.append(f"{start} -> {end}")
        self.route_combo.addItems(display_route_list)
        
    
    def change_operating_line_route(self, index):
        self.line_route = index
    
    def start_operating_line(self):
        self.operator_main.start_line_and_route(self.line_file, self.line_route, 0)
        self.route_director = self.operator_main.director
    
    def operation_callback(self, object):
        station = object[0]
        state = object[1]
        elapsed_time = object[2]
        self.debug_text.setText(f"Route Director Callback: {station}, {STATION_STATE_INTERPRET_MAP[state]}, timestamp {elapsed_time}")

    def do_next_stage(self):
        self.route_director.elapsed_time += 40
    
    def do_start_over(self):
        self.route_director.elapsed_time = 0

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TrainDisplay()
    window.show()
    sys.exit(app.exec_())