from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QColor, QPainterPath
from PyQt5.QtCore import Qt
import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout,
    QGridLayout, QPushButton, QStackedWidget
)
from PyQt5.QtGui import QFont, QFontDatabase, QColor, QPalette
from PyQt5.QtCore import QPoint, QPropertyAnimation, QParallelAnimationGroup
from PyQt5.QtCore import Qt, QTimer

from scene_manager import SceneManager
from animated_text_view import AnimatedTextView
from test_widget import ProgressBarWithArrows


class TrainDisplay(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("車廂顯示器模擬")
        self.setFixedSize(960, 512)
        self.setStyleSheet("background-color: #ffffff;")    
        self.initUI()
    
    def initUI(self):
        # 字體預設
        family = "Noto Sans JP"

        font_large = QFont(family, 32, QFont.Bold)
        font_current_station = QFont(family, 64, QFont.Bold)
        font_car = QFont(family, 48, QFont.Bold)
        font_station_number = QFont(family, 48, QFont.Bold)

        main_layout = QVBoxLayout()
        bar = ProgressBarWithArrows()
        bar.setProgress(0.5)  # 設定進度條的進度
        main_layout.addWidget(bar)

        self.setLayout(main_layout)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TrainDisplay()
    window.show()
    sys.exit(app.exec_())