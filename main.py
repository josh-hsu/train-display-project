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
        self.operator_main = OsakaMetroTrainDisplay()

        #
        # Debug 階段
        #
        debug_layout = QHBoxLayout()
        debug_layout.setContentsMargins(0, 0, 0, 0)
        debug_layout.setAlignment(Qt.AlignLeft)

        debug_text = QLabel("Debug message: testing ...")
        debug_text.setFont(debug_font)
        debug_text.setFixedSize(400, 50)
        debug_text.setStyleSheet(f"background-color: {MIDOSUJI_BACKGROUND_COLOR}; color: {GREY_COLOR};")

        debug_button = QPushButton("Next stage")
        debug_button.setFixedSize(200, 50)
        debug_button.setStyleSheet("background-color: #ffffff; color: #000000;")
        debug_button.clicked.connect(self.debug_next_stage)

        debug_check_state = QPushButton("Check state")
        debug_check_state.setFixedSize(200, 50)
        debug_check_state.setStyleSheet("background-color: #ffffff; color: #000000;")
        debug_check_state.clicked.connect(self.debug_check_state)
        
        debug_layout.addWidget(debug_text)
        debug_layout.addWidget(debug_button)
        debug_layout.addWidget(debug_check_state)

        #
        # 主垂直布局
        #
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        main_layout.addWidget(self.operator_main)
        main_layout.addLayout(debug_layout)

        self.setLayout(main_layout)
    
    def debug_next_stage(self):
        pass
    
    def debug_check_state(self):
        self.operator_main.update_train_state()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TrainDisplay()
    window.show()
    sys.exit(app.exec_())