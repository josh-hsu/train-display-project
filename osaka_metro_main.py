import sys, os
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout,
    QStackedWidget
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QPoint, QPropertyAnimation, QParallelAnimationGroup
from PyQt5.QtCore import Qt, QTimer, pyqtSignal

from scene_manager import SceneManager
from osaka_metro.osaka_metro import *
from line_info import *
from route_director import RouteDirector

from train_textview_libs import *

class OsakaMetroTrainDisplay(QWidget):
    operation_route_callback = pyqtSignal(object)
    
    def __init__(self, line_file=None, route_select=0, elapsed_time=0):
        super().__init__()
        
        self.line_file = line_file
        self.route_select = route_select
        self.director = None
        if self.line_file is None:
            self.line_select = "Midosuji"
            self.line_file = f"{LINE_INFO_FILE_FOLDER}{LINE_INFO_FILE_PATH_MAP[self.line_select]}"
        self.line_color = "#e5171f"
        self.scene_anim_duration = 0
        
        self.setFixedSize(960, 512)
        self.setStyleSheet("background-color: #ffffff;")
        self.initUI()
        self.start_line_and_route(self.line_file, self.route_select, elapsed_time)

    def initLineInfo(self, line_file, route_select):
        self.line_info = LineInfo(line_file)
        self.line_info.set_route(route_select)
        self.route = self.line_info.get_current_route()
        self.line_color = self.line_info.main_color
        self.station_num_container_layout.setStyleSheet(f"background-color: {self.line_color}; {BORDER_DEBUG}")

    def initRouteDirector(self, line_info: LineInfo, default_elapsed_time):
        self.train_state = STATION_STATE_READY_TO_DEPART
        if self.director is not None:
            self.director.__del__()
        self.director = RouteDirector(line_info, self.route, interval_sec=1, interval_inc=1, init_elapsed_time=default_elapsed_time)
        self.director.report.connect(self.route_director_callback)
        self.director.start()

    def initUI(self):
        # 字體預設
        family = FONT_NAME

        if os.name == "posix":
            font_large = QFont(family, 32, QFont.Bold)
            font_current_station = QFont(family, 90, QFont.Bold)
            font_car = QFont(family, 48, QFont.Bold)
            font_car_instructions = QFont(family, 16, QFont.Bold)
            font_station_number = QFont(family, 48, QFont.Bold)
        else:
            font_large = QFont(family, 28)
            font_current_station = QFont(family, 78)
            font_car = QFont(family, 42)
            font_car_instructions = QFont(family, 16)
            font_station_number = QFont(family, 36)

        # 第一大列
        top_layout = QHBoxLayout()
        top_layout.setContentsMargins(0, 0, 0, 0)
        top_layout.setSpacing(0)

        # 目的地layout
        top_left_layout = QVBoxLayout()
        top_left_layout.setContentsMargins(0, 0, 0, 0)
        top_left_layout.setSpacing(0)

        # 目的地（480x240）
        self.textview_destination = AnimatedTextView_T()
        self.textview_destination.setFixedSize(220, 60)
        self.textview_destination.setTexts(DEST_STATION_INFO)
        self.textview_destination.setMinimumHeight(60)
        self.textview_destination.setStyleSheet(f"background-color: {WHITE_BACKGROUND_COLOR}; color: {GREY_COLOR}; {BORDER_DEBUG}")
        self.textview_destination.setFont(font_large)
        self.textview_destination.setAlignment(Qt.AlignRight)
        self.textview_destination.setAnimationType(AnimatedTextView_T.ANIMATION_NONE)

        self.textview_now_state = AnimatedTextView_T()
        self.textview_now_state.setFixedSize(220, 60)
        self.textview_now_state.setMinimumHeight(60)
        self.textview_now_state.setTexts(NOW_STATE_MAP['0'])
        self.textview_now_state.setStyleSheet(f"background-color: {WHITE_BACKGROUND_COLOR}; color: {BLACK_COLOR}; {BORDER_DEBUG}")
        self.textview_now_state.setFont(font_large)
        self.textview_now_state.setAlignment(Qt.AlignRight)
        self.textview_now_state.setAnimationType(AnimatedTextView_T.ANIMATION_NONE)

        top_left_layout.addWidget(self.textview_destination)
        top_left_layout.addWidget(self.textview_now_state)

        # 現在/下一站（1280x100）
        center_layout = QVBoxLayout()
        center_layout.setContentsMargins(0, 0, 0, 0)
        center_layout.setSpacing(0)

        self.textview_station = AnimatedTextView_T()
        self.textview_station.setFixedSize(620, 120)
        self.textview_station.setStyleSheet(f"background-color: {WHITE_BACKGROUND_COLOR}; color: {BLACK_COLOR}; {BORDER_DEBUG}")
        self.textview_station.setFont(font_current_station)
        self.textview_station.setAlignment(Qt.AlignCenter)
        self.textview_station.setAnimationType(AnimatedTextView_T.ANIMATION_FOLD)

        center_layout.addWidget(self.textview_station)

        # 車廂編號（200x240）
        right_layout = QVBoxLayout()
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(0)
        self.label_top_car_number = AnimatedTextView_T()
        self.label_top_car_number.setFixedSize(100, 30)
        self.label_top_car_number.setTexts(CAR_INST_TOP)
        self.label_top_car_number.setFont(font_car_instructions)
        self.label_top_car_number.setStyleSheet(f"background-color: {WHITE_BACKGROUND_COLOR}; color: {GREY_COLOR}; {BORDER_DEBUG}")
        self.label_top_car_number.setAlignment(Qt.AlignCenter)
        self.label_top_car_number.setAnimationType(AnimatedTextView_T.ANIMATION_NONE)
        right_layout.addWidget(self.label_top_car_number)
        self.label_car_number = QLabel("5")
        self.label_car_number.setFont(font_car)
        self.label_car_number.setFixedSize(100, 60)
        self.label_car_number.setStyleSheet(f"background-color: {WHITE_BACKGROUND_COLOR}; color: {GREY_COLOR}; {BORDER_DEBUG}")
        self.label_car_number.setAlignment(Qt.AlignCenter)
        self.label_car_number.setContentsMargins(0, 0, 0, 0)
        right_layout.addWidget(self.label_car_number)
        self.label_bottom_car_number = AnimatedTextView_T()
        self.label_bottom_car_number.setFixedSize(100, 30)
        self.label_bottom_car_number.setTexts(CAR_INST_BOT)
        self.label_bottom_car_number.setFont(font_car_instructions)
        self.label_bottom_car_number.setStyleSheet(f"background-color: {WHITE_BACKGROUND_COLOR}; color: {GREY_COLOR}; {BORDER_DEBUG}")
        self.label_bottom_car_number.setAlignment(Qt.AlignCenter)
        self.label_bottom_car_number.setAnimationType(AnimatedTextView_T.ANIMATION_NONE)
        right_layout.addWidget(self.label_bottom_car_number)
        # Combine top layout
        top_layout.addLayout(top_left_layout)
        top_layout.addLayout(center_layout)
        top_layout.addLayout(right_layout)

        #
        # 第二大列
        #
        self.station_num_container_layout = QWidget()
        self.station_num_container_layout.setFixedHeight(50)
        second_layout = QHBoxLayout()
        second_layout.setContentsMargins(0, 0, 0, 0)
        second_layout.setSpacing(0)

        # 站號
        label_station_number_left = QLabel("")
        label_station_number_left.setFixedSize(220, 50)
        
        self.label_station_number = QLabel("M19")
        self.label_station_number.setFont(font_station_number)
        self.label_station_number.setStyleSheet(f"color: #FFFFFF")
        self.label_station_number.setFixedSize(620, 50)
        self.label_station_number.setAlignment(Qt.AlignCenter)

        label_station_number_right = QLabel("")
        label_station_number_right.setFixedSize(100, 50)

        # 第二大列新增
        second_layout.addWidget(label_station_number_left)
        second_layout.addWidget(self.label_station_number)
        second_layout.addWidget(label_station_number_right)
        second_layout.setContentsMargins(0, 0, 0, 0)
        second_layout.setSpacing(0)
        self.station_num_container_layout.setStyleSheet(f"background-color: #000000; {BORDER_DEBUG}")
        self.station_num_container_layout.setLayout(second_layout)

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
        main_layout.addWidget(self.station_num_container_layout)
        main_layout.addWidget(central)

        self.setLayout(main_layout)

    def scene_switch_immediately(self):
        start_index = self.scene_manager.start_index_of_state[self.train_state]
        end_index = self.scene_manager.end_index_of_state[self.train_state]
        self.current_index = start_index

        print(f"reset, start: {start_index} end: {end_index} next: {self.current_index}")

        current_widget = self.scene_container.widget(self.current_index)
        self.scene_container.setCurrentIndex(self.current_index)
        current_widget.on_scene_present()
        for i in range(len(self.scene_keys)):
            scene = self.scene_container.widget(i)
            if scene is not current_widget:
                scene.on_scene_disappear()

    def animate_scene_switch(self):
        start_index = self.scene_manager.start_index_of_state[self.train_state]
        end_index = self.scene_manager.end_index_of_state[self.train_state]
        next_index = (self.current_index + 1) % len(self.scene_keys)

        if next_index > end_index or next_index < start_index:
            next_index = start_index

        print(f"callback, start: {start_index} end: {end_index} next: {next_index}")

        current_widget = self.scene_container.widget(self.current_index)
        next_widget = self.scene_container.widget(next_index)

        w = self.scene_container.width()
        h = self.scene_container.height()

        # 設定初始位置：下一個 widget 放在右側
        next_widget.setGeometry(w, 0, w, h)
        next_widget.show()

        # 創建動畫
        anim_out = QPropertyAnimation(current_widget, b"pos")
        anim_out.setDuration(self.scene_anim_duration)
        anim_out.setStartValue(QPoint(0, 0))
        anim_out.setEndValue(QPoint(-w, 0))

        anim_in = QPropertyAnimation(next_widget, b"pos")
        anim_in.setDuration(self.scene_anim_duration)
        anim_in.setStartValue(QPoint(w, 0))
        anim_in.setEndValue(QPoint(0, 0))

        # 將動畫加入群組
        self.animation_group = QParallelAnimationGroup()
        self.animation_group.addAnimation(anim_out)
        self.animation_group.addAnimation(anim_in)

        def on_finished():
            self.scene_container.setCurrentIndex(next_index)
            next_widget.on_scene_present()
            current_widget.on_scene_disappear()
            current_widget.move(0, 0)
            self.current_index = next_index
            self.animation_group = None  # 清除引用

        self.animation_group.finished.connect(on_finished)
        self.animation_group.start()

    def format_train_destination(self):
        line_info = self.line_info
        self.destination_texts = []
        termianl_station_id = line_info.get_current_route()[-1]
        termianl_station = line_info.get_station(termianl_station_id)

        self.destination_texts.append(f"{termianl_station.name['jp']}{DEST_STATION_INFO[0]}")
        self.destination_texts.append(f"{termianl_station.name['jp-hiragana']}{DEST_STATION_INFO[1]}")
        self.destination_texts.append(f"{DEST_STATION_INFO[2]}{termianl_station.name['en']}")
        self.destination_texts.append(f"{DEST_STATION_INFO[3]}{termianl_station.name['zh-TW']}")

    def prepare_line_name(self):
        line_info = self.line_info
        self.destination_texts = []

        self.destination_texts.append(line_info.name['jp'])
        self.destination_texts.append(line_info.name['jp-hinagana'])
        self.destination_texts.append(line_info.name['en'])
        self.destination_texts.append(line_info.name['zh-TW'])

    def start_new_train(self):
        line_info = self.line_info
        current_station_id = line_info.get_current_route()[0]
        current_station = line_info.get_station(current_station_id)
        termianl_station_id = line_info.get_current_route()[-1]
        termianl_station = line_info.get_station(termianl_station_id)
        self.train_state = STATION_STATE_READY_TO_DEPART
        self.prepare_line_name()
        self.textview_now_state.setTexts(NOW_STATE_MAP[f"{self.train_state}"])
        self.textview_destination.setTexts(self.destination_texts)
        self.label_station_number.setText(f"{current_station_id}")
        self.textview_station.setTexts(list(termianl_station.name.values()))
        self.label_top_car_number.setTexts(CAR_INST_TOP)
        self.label_bottom_car_number.setTexts(CAR_INST_BOT)
        self.scene_manager.notify_all_scenes(line_info, current_station, self.train_state)

    def update_train_state(self, station_id, state):
        line_info = self.line_info
        station = line_info.get_station(station_id)
        self.train_state = state
        if state == STATION_STATE_READY_TO_DEPART:
            self.prepare_line_name()
        else:
            self.format_train_destination()
        self.label_station_number.setText(f"{station.id}")
        self.textview_station.setTexts(list(station.name.values()))
        self.textview_now_state.setTexts(NOW_STATE_MAP[f"{state}"])
        self.textview_destination.setTexts(self.destination_texts)
        self.label_top_car_number.setTexts(CAR_INST_TOP)
        self.label_bottom_car_number.setTexts(CAR_INST_BOT)
        self.scene_manager.notify_all_scenes(line_info, station, state)
        self.scene_switch_immediately()

    def route_director_callback(self, object):
        station = object[0]
        state = object[1]
        elapsed_time = object[2]
        self.operation_route_callback.emit(object)
        print(f"Route Director Callback: {station}, {state}, timestamp {elapsed_time}")
        if state is not self.train_state:
            self.update_train_state(station, state)
        self.train_state = state
    
    def start_line_and_route(self, line, route, elapsed):
        self.line_file = line
        self.route_select = route
        self.initLineInfo(self.line_file, self.route_select)
        self.setWindowTitle(f"車廂顯示器模擬 - {self.line_info.name['zh-TW']}")
        self.initRouteDirector(self.line_info, elapsed)
        self.start_new_train()
    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = OsakaMetroTrainDisplay()
    window.show()
    sys.exit(app.exec_())