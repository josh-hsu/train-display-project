# scene_station_list.py
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QLayout
from PyQt5.QtCore import Qt, QPoint, QTimer
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtGui import QPainter, QColor, QPainterPath
from PyQt5.QtGui import QBrush, QPolygon

import os
from osaka_metro.osaka_metro import *
from train_textview_libs import RotatedLabel
from train_textview_libs import *
from line_info import *

class SideArrow(QWidget):
    def __init__(self, line_color, parent=None):
        super().__init__(parent)
        self.line_color = line_color

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

        painter.setBrush(QColor(self.line_color))
        painter.drawPath(complete_path)

        painter.end()

class MovingArrow(QWidget):
    def __init__(self, line_color, parent=None):
        super().__init__(parent)
        self.setMinimumSize(120, 40)  # 預設尺寸，可自己調整
        self.blue_is_red = False  # 目前藍色部分是不是變紅色
        self.line_color = line_color

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
        red_brush = QBrush(QColor(self.line_color))
        painter.setBrush(red_brush)
        
        red1 = QPolygon([QPoint(0,0), QPoint(20,0), QPoint(0,18)])
        red2 = QPolygon([QPoint(0,18), QPoint(20,36), QPoint(0,36)])
        painter.drawPolygon(red1)
        painter.drawPolygon(red2)

        # 藍色部分
        if self.blue_is_red:
            painter.setBrush(QColor(RED_COLOR))  # 當作紅色
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
        self.icon_dir = icon_dir
        self.line_font = QFont(FONT_NAME, 12)
        self.line_color = "#e5171f"

        self.layout = QVBoxLayout()
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setAlignment(Qt.AlignTop)

        self.setLayout(self.layout)
        self.setData(icon_names, station_names)

    def setData(self, icon_names, station_names):
        # 清空原本 layout 的內容
        while self.layout.count():
            item = self.layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
            elif item.layout():
                self._delete_layout(item.layout())

        # 重新加入新的圖示與站名
        for icon_name, station_name in zip(icon_names, station_names):
            row = QHBoxLayout()
            row.setSpacing(0)
            row.setAlignment(Qt.AlignLeft)
            row.setContentsMargins(0, 0, 0, 0)

            icon_path = os.path.join(self.icon_dir, ICON_MAP.get(icon_name, ""))
            icon_label = QLabel()
            if os.path.exists(icon_path):
                pixmap = QPixmap(icon_path)
                icon_label.setPixmap(pixmap.scaled(24, 24, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            icon_label.setFixedSize(24, 24)
            icon_label.setScaledContents(True)

            text_label = StretchTextLabel(station_name)
            text_label.setFont(self.line_font)
            text_label.setFixedSize(96, 24)
            text_label.setStyleSheet(f"background-color: {WHITE_BACKGROUND_COLOR}; color: #000000;")

            row_widget = QWidget()
            row_widget.setLayout(row)
            row.addWidget(icon_label)
            row.addWidget(text_label)

            self.layout.addWidget(row_widget)

    def _delete_layout(self, layout):
        """遞迴清理巢狀 layout 中的 widget"""
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
            elif item.layout():
                self._delete_layout(item.layout())
        layout.deleteLater()

class SceneStationListEN(QWidget):
    def __init__(self):
        super().__init__()
        self.line_info = None
        self.display_station = None
        self.station_state = STATION_STATE_READY_TO_DEPART
        self.line_color = "#e5171f" #default to red
        self.init_ui()
    
    def init_ui(self):
        if (os.name == "posix"):
            family = "Noto Sans JP"
            self.sta_font = QFont(family, 32, QFont.Bold)
            self.en_font = QFont(family, 18, QFont.Bold)
            self.min_font = QFont(family, 24, QFont.Bold)
            self.approx_font = QFont(family, 18, QFont.Bold)
        else:
            family = "Noto Sans JP SemiBold"
            self.sta_font = QFont(family, 28, QFont.Bold)
            self.en_font = QFont(family, 16, QFont.Bold)
            self.min_font = QFont(family, 20, QFont.Bold)
            self.approx_font = QFont(family, 12, QFont.Bold)
        
        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        self.setStyleSheet(f"background-color: {self.line_color}; {BORDER_DEBUG}")
        self.setFixedSize(960, 342)
        
        # station names layout
        self.top_layout = QHBoxLayout()
        self.top_layout.setContentsMargins(0, 0, 0, 0)
        self.top_layout.setSpacing(0)
        self.sta_leftmost = QLabel("")
        self.sta_leftmost.setFixedSize(150, 150)
        self.sta_leftmost.setStyleSheet(f"background-color: {WHITE_BACKGROUND_COLOR}; color: {WHITE_BACKGROUND_COLOR}; {BORDER_DEBUG}")
        self.top_layout.addWidget(self.sta_leftmost)
        self.sta = []
        for i in range(7):
            label = RotatedLabel(f"")
            label.setStyleSheet(f"background-color: {WHITE_BACKGROUND_COLOR}; color: {BLACK_COLOR}; {BORDER_DEBUG}")
            label.setFixedSize(120, 150)
            label.setContentsMargins(20, 20, 20, 20)
            label.setFont(self.en_font)
            self.top_layout.addWidget(label)
            self.sta.append(label)
        self.sta_rightmost = QLabel("")
        self.sta_rightmost.setFixedSize(30, 150)
        self.sta_rightmost.setStyleSheet(f"background-color: {WHITE_BACKGROUND_COLOR}; color: {WHITE_BACKGROUND_COLOR}; {BORDER_DEBUG}")
        self.top_layout.addWidget(self.sta_rightmost)
        self.main_layout.addLayout(self.top_layout)

        # 2nd layout: progress bar
        self.second_layout = QHBoxLayout()
        self.second_layout.setContentsMargins(0, 0, 0, 0)
        self.second_layout.setSpacing(0)
        self.progress_index = 11
        self.progress = []
        self.init_progress_bar(self.second_layout)
        self.main_layout.addLayout(self.second_layout)

        # 3rd layout: minute time
        self.third_layout = QHBoxLayout()
        self.third_layout.setContentsMargins(0, 0, 0, 0)
        self.third_layout.setSpacing(0)
        self.min_leftmost = QLabel("Approx.")
        self.min_leftmost.setAlignment(Qt.AlignCenter)
        self.min_leftmost.setFont(self.approx_font)
        self.min_leftmost.setFixedSize(90, 30)
        self.min_leftmost.setStyleSheet(f"background-color: {WHITE_BACKGROUND_COLOR}; color: {BLACK_COLOR}; {BORDER_DEBUG}")  
        self.third_layout.addWidget(self.min_leftmost)
        self.min = []
        for i in range(12):
            label = QLabel("")
            label.setAlignment(Qt.AlignCenter)
            label.setFixedSize(60, 30)
            label.setFont(self.min_font)
            label.setStyleSheet(f"background-color: {WHITE_BACKGROUND_COLOR}; color: {BLACK_COLOR}; {BORDER_DEBUG}")   
            self.min.append(label)
            self.third_layout.addWidget(label)
        self.min_rightmost = QLabel("")
        self.min_rightmost.setAlignment(Qt.AlignRight)
        self.min_rightmost.setFixedSize(150, 30)
        self.min_rightmost.setFont(self.approx_font)
        self.min_rightmost.setStyleSheet(f"background-color: {WHITE_BACKGROUND_COLOR}; color: {BLACK_COLOR}; {BORDER_DEBUG}")
        self.third_layout.addWidget(self.min_rightmost)
        self.main_layout.addLayout(self.third_layout)

        # 4th layout
        self.bottom_layout = QHBoxLayout()
        self.bottom_layout.setContentsMargins(0, 0, 0, 0)
        self.bottom_layout.setSpacing(0)
        self.transfer_leftmost = QLabel("")
        self.transfer_leftmost.setAlignment(Qt.AlignCenter)
        self.transfer_leftmost.setFont(self.sta_font)
        self.transfer_leftmost.setFixedSize(60, 124)
        self.transfer_leftmost.setStyleSheet(f"background-color: {WHITE_BACKGROUND_COLOR}; color: {BLACK_COLOR}; {BORDER_DEBUG}")
        self.bottom_layout.addWidget(self.transfer_leftmost)
        self.transfer_info_view = []
        for i in range(6):
            icon_keys = ["Sennichimae", "Kintetsu", "Nankai"]
            station_names = ["Sennichimae Line  ", "近鐵線", "南海線"]
            transfer_info_widget = TransferInfo(icon_keys, station_names)
            transfer_info_widget.setFixedSize(120, 124)
            self.transfer_info_view.append(transfer_info_widget)
            self.bottom_layout.addWidget(transfer_info_widget)
        self.transfer_rightmost = QLabel("")
        self.transfer_rightmost.setAlignment(Qt.AlignRight)
        self.transfer_rightmost.setFixedSize(180, 124)
        self.transfer_rightmost.setStyleSheet(f"background-color: {WHITE_BACKGROUND_COLOR}; color: {BLACK_COLOR}; {BORDER_DEBUG}")
        self.bottom_layout.addWidget(self.transfer_rightmost)
        self.main_layout.addLayout(self.bottom_layout)

        self.setLayout(self.main_layout)

    def clear_layout(self, layout: QLayout):
        """安全刪除 layout 中所有 widgets 和子 layouts"""
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            child_layout = item.layout()

            if widget is not None:
                widget.setParent(None)
                widget.deleteLater()

            elif child_layout is not None:
                self.clear_layout(child_layout)
                child_layout.deleteLater()

    def init_progress_bar(self, layout: QHBoxLayout):
        # 清除 stack_layout 中的所有 widget
        self.clear_layout(layout)
        
        self.progress_leftmost = SideArrow(self.line_color)
        self.progress_leftmost.setFixedSize(90, 36)
        self.progress_leftmost.setStyleSheet(f"background-color: {self.line_color}; color: {WHITE_BACKGROUND_COLOR}; {BORDER_DEBUG}")
        layout.addWidget(self.progress_leftmost)
        self.progress = []
        for i in range(13):
            if i < self.progress_index:
                label = QLabel("")
                label.setFont(self.min_font)
                label.setAlignment(Qt.AlignCenter)
                label.setFixedSize(60, 36)
                label.setStyleSheet(f"background-color: {self.line_color}; color: {WHITE_BACKGROUND_COLOR}; {BORDER_DEBUG}")
                self.progress.append(label)
                layout.addWidget(label)
            elif i == self.progress_index:
                self.moving_arrow = MovingArrow(self.line_color)
                self.moving_arrow.setFixedSize(60, 36)
                layout.addWidget(self.moving_arrow)
            else:
                label = QLabel("")
                label.setFont(self.min_font)
                label.setAlignment(Qt.AlignCenter)
                label.setFixedSize(60, 36)
                label.setStyleSheet(f"background-color: {GREY_COLOR}; color: {WHITE_BACKGROUND_COLOR}; {BORDER_DEBUG}")
                self.progress.append(label)
                layout.addWidget(label)
   
        self.progress_rightmost = QLabel()
        self.progress_rightmost.setFixedSize(90, 36)
        self.progress_rightmost.setStyleSheet(f"background-color: {GREY_COLOR}; {BORDER_DEBUG}")
        layout.addWidget(self.progress_rightmost)

    def get_seven_stations_with_index(self, terminal, start, current):
        direction = 1 if terminal > start else -1  # 判斷方向
        stations = []
        
        if start == current:
            for i in range(6, -1, -1):
                station = current + direction * i
                if (direction == 1 and station <= terminal) or (direction == -1 and station >= terminal):
                    stations.append(station)
        elif abs(terminal - current) <= 5:
            for i in range(7):
                station = terminal - direction * i
                stations.append(station)
        else:
            for i in range(5, -2, -1):  # 從前五站到前一站，共七站
                station = current + direction * i
                if (direction == 1 and station <= terminal) or (direction == -1 and station >= terminal):
                    stations.append(station)

        # 找出 current 在 stations 中的位置（理論上一定會在內）
        try:
            current_index = stations.index(current)
        except ValueError:
            current_index = -1  # 如果 current 不在七站內（理論上不會發生）

        #print(f"get_seven_stations_with_index: {stations}, current_index: {current_index}")

        return stations, current_index

    def update_station_list(self):
        route = self.line_info.directions[self.line_info.route]  # [M13, M22]
        start_id = route[0]
        end_id = route[1]
        start_id_num = extract_first_integer(start_id)
        end_id_num = extract_first_integer(end_id)
        current_id_num = extract_first_integer(self.display_station.id)
        seven_stations_num, current_index = self.get_seven_stations_with_index(end_id_num, start_id_num, current_id_num)
        
        if current_index < 5:
            self.progress_index = 11 - (5 - current_index) * 2
        self.init_progress_bar(self.second_layout)
        
        # 清除舊資料
        for min_label in self.min:
            min_label.setText("")

        # 計算實際分鐘
        counting_index = current_index
        if current_index == 6:
            counting_index = 5
        travel_minute = [0, 0, 0, 0, 0, 0]
        for i in range(counting_index + 2):
            j = seven_stations_num[i]
            station_id = index_to_station_id(self.line_info.id_prefix, j)
            station = self.line_info.get_station(station_id)
            if station:
                min = station.next_station[2]
                if min is None:
                    min = "0"
                #print(f"station_id: {station_id}, station: {station.name['jp']}, next min: {station.next_station[2]}")
                minute = int(min)
                for k in range(i):
                    travel_minute[k] += minute
        
        for i in range(6):
            j = seven_stations_num[i]
            station_id = index_to_station_id(self.line_info.id_prefix, j)
            station = self.line_info.get_station(station_id)
            transfer = station.transfer
            
            #print(f"station_id: {station_id}, station: {station}, transfer: {transfer}")
            if station:
                station_name_disp = format_train_progress_station_name(station.name["en"])
                self.sta[i].setText(f"   {station_name_disp}")
                if i * 2 < self.progress_index:
                    self.progress[i * 2].setText(station_id)
                    self.min[i * 2].setText(f"{travel_minute[i]/60:.0f}")
                else:
                    self.progress[i * 2 - 1].setText(station_id)
                    self.min[i * 2].setText(f"")
                #self.progress[i * 2].setText(station_id)
                self.transfer_info_view[i].setData(transfer.get_station_list(), [f"{name} Line " for name in transfer.get_station_list()])
            else:
                self.sta[i*2].setText("???")
                
        # 更新最右邊的站名
        if current_index == 6:
            self.min[11].setText("min")
        else:
            self.min[current_index * 2 + 1].setText("min")
        station_id = index_to_station_id(self.line_info.id_prefix, seven_stations_num[6])
        station = self.line_info.get_station(station_id)
        if station:
            station_name_disp = format_train_progress_station_name(station.name["en"])
            self.sta[6].setText(f"   {station_name_disp}")
            self.progress[-1].setText(station_id)
        
        #for i in range(6):
        #    self.transfer[i].setText("i")
    
    def on_scene_present(self):
        pass

    def on_scene_disappear(self):
        pass

    def receive_notify(self, line_info, display_station, station_state):
        self.line_info = line_info
        self.line_color = line_info.main_color
        self.display_station = display_station
        self.station_state = station_state
        self.update_station_list()