import sys, os
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout,
    QStackedWidget
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QPoint, QPropertyAnimation, QParallelAnimationGroup
from PyQt5.QtCore import Qt, QTimer

from scene_manager import SceneManager
from animated_text_view import AnimatedTextView

class TrainDisplay(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("車廂顯示器模擬")
        self.setFixedSize(960, 512)
        self.setStyleSheet("background-color: #ffffff;")    
        self.initUI()

    def initUI(self):
        os_is_posix = False
        if (os.name == "posix"):
            os_is_posix = True
        # 字體預設
        family = "Noto Sans JP"
        family_win = "Noto Sans JP SemiBold"

        if (os_is_posix):
            font_large = QFont(family, 32, QFont.Bold)
            font_current_station = QFont(family, 90, QFont.Bold)
            font_car = QFont(family, 48, QFont.Bold)
            font_station_number = QFont(family, 48, QFont.Bold)
        else:
            font_large = QFont(family_win, 28)
            font_current_station = QFont(family_win, 78)
            font_car = QFont(family_win, 42)
            font_station_number = QFont(family_win, 36)

        # 第一大列
        top_layout = QHBoxLayout()
        top_layout.setContentsMargins(0, 0, 0, 0)
        top_layout.setSpacing(0)

        # 目的地layout
        top_left_layout = QVBoxLayout()
        top_left_layout.setContentsMargins(0, 0, 0, 0)
        top_left_layout.setSpacing(0)

        # 目的地（480x240）
        self.textview_destination = AnimatedTextView(220, 60, ["新大阪 ゆき", "しんおおさか　ゆき", "開往 新大阪", "For Shin-Osaka"])
        self.textview_destination.setStyleSheetAll("background-color: #FFFFFF; color: #888888;")
        self.textview_destination.setFont(font_large)
        self.textview_destination.setAlignment(Qt.AlignRight)
        self.textview_destination.start()

        self.textview_now_current = AnimatedTextView(220, 60, ["まもらく", "まもらく", "即將到達", "Arriving at"])
        self.textview_now_current.setStyleSheetAll("background-color: #FFFFFF; color: #000000;")
        self.textview_now_current.setFont(font_large)
        self.textview_now_current.setAlignment(Qt.AlignRight)
        self.textview_now_current.start()

        top_left_layout.addWidget(self.textview_destination.widget())
        top_left_layout.addWidget(self.textview_now_current.widget())

        # 現在/下一站（1280x100）
        center_layout = QVBoxLayout()
        center_layout.setContentsMargins(0, 0, 0, 0)
        center_layout.setSpacing(0)

        self.textview_station = AnimatedTextView(620, 120, ["心斎橋", "しんさいばし", "心齋橋", "Shinsaibashi"],
                                                 animation_type="fold", interval_ms=3000)
        self.textview_station.setStyleSheetAll("background-color: #FFFFFF; border: color: #000000;")
        self.textview_station.setFont(font_current_station)
        self.textview_station.setAlignment(Qt.AlignCenter)
        self.textview_station.start()

        center_layout.addWidget(self.textview_station.widget())

        # 車廂編號（200x240）
        label_car_number = QLabel("5")
        label_car_number.setFont(font_car)
        label_car_number.setFixedSize(100, 120)
        label_car_number.setStyleSheet("background-color: #FFFFFF; color: #888888;")
        label_car_number.setAlignment(Qt.AlignCenter)

        # Combine top layout
        top_layout.addLayout(top_left_layout)
        top_layout.addLayout(center_layout)
        top_layout.addWidget(label_car_number)

        #
        # 第二大列
        #
        second_container_layout = QWidget()
        second_container_layout.setFixedHeight(50)
        second_layout = QHBoxLayout()
        second_layout.setContentsMargins(0, 0, 0, 0)
        second_layout.setSpacing(0)

        # 站號
        label_station_number_left = QLabel("")
        label_station_number_left.setFixedSize(220, 50)
        label_station_number_left.setStyleSheet("background-color: #F61826; color: #FFFFFF;")
        
        label_station_number = QLabel("M19")
        label_station_number.setFont(font_station_number)
        label_station_number.setFixedSize(620, 50)
        label_station_number.setStyleSheet("background-color: #F61826; color: #FFFFFF;")
        label_station_number.setAlignment(Qt.AlignCenter)

        label_station_number_right = QLabel("")
        label_station_number_right.setFixedSize(100, 50)
        label_station_number_right.setStyleSheet("background-color: #F61826; color: #FFFFFF;")
        
        # 第二大列新增
        second_layout.addWidget(label_station_number_left)
        second_layout.addWidget(label_station_number)
        second_layout.addWidget(label_station_number_right)
        second_layout.setContentsMargins(0, 0, 0, 0)
        second_layout.setSpacing(0)
        second_container_layout.setStyleSheet("background-color: #F61826;")
        second_container_layout.setLayout(second_layout)

        #
        # 第三列
        #
        self.scene_manager = SceneManager()
        self.scene_container = QStackedWidget(self)
        self.scene_container.setContentsMargins(0, 0, 0, 0)
        self.scene_keys = list(self.scene_manager.scenes.keys())

        for scene in self.scene_manager.scenes.values():
            self.scene_container.addWidget(scene)

        self.current_index = 0
        self.scene_container.setCurrentIndex(self.current_index)

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.scene_container)

        central = QWidget()
        central.setFixedSize(960, 342)
        central.setLayout(layout)

        # 新增：輪播 Timer
        self.carousel_timer = QTimer(self)
        self.carousel_timer.timeout.connect(self.animate_scene_switch)
        self.carousel_timer.start(7000)

        #
        # 主垂直布局
        #
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        main_layout.addLayout(top_layout)
        main_layout.addWidget(second_container_layout)
        main_layout.addWidget(central)

        self.setLayout(main_layout)

    def animate_scene_switch(self):
        next_index = (self.current_index + 1) % len(self.scene_keys)
        current_widget = self.scene_container.widget(self.current_index)
        next_widget = self.scene_container.widget(next_index)

        w = self.scene_container.width()
        h = self.scene_container.height()

        # 設定初始位置：下一個 widget 放在右側
        next_widget.setGeometry(w, 0, w, h)
        next_widget.show()

        # 創建動畫
        anim_out = QPropertyAnimation(current_widget, b"pos")
        anim_out.setDuration(500)
        anim_out.setStartValue(QPoint(0, 0))
        anim_out.setEndValue(QPoint(-w, 0))

        anim_in = QPropertyAnimation(next_widget, b"pos")
        anim_in.setDuration(500)
        anim_in.setStartValue(QPoint(w, 0))
        anim_in.setEndValue(QPoint(0, 0))

        # 將動畫加入群組
        self.animation_group = QParallelAnimationGroup()
        self.animation_group.addAnimation(anim_out)
        self.animation_group.addAnimation(anim_in)

        def on_finished():
            self.scene_container.setCurrentIndex(next_index)
            current_widget.move(0, 0)
            self.current_index = next_index
            self.animation_group = None  # 清除引用

        self.animation_group.finished.connect(on_finished)
        self.animation_group.start()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TrainDisplay()
    window.show()
    sys.exit(app.exec_())