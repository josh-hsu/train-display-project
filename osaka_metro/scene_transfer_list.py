import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QVBoxLayout, 
                            QHBoxLayout, QSizePolicy, QMainWindow, QFrame)
from PyQt5.QtGui import QFont, QPainter, QColor, QPen
from PyQt5.QtCore import Qt, QSize

from osaka_metro.osaka_metro import *
from line_info import LineInfo, StationInfo, TransferInfo, TransferEntry

class CircleIconLabel(QLabel):
    """Custom QLabel that displays a circular background with text centered"""
    def __init__(self, text, bg_color, text_color="white", station_num=None, parent=None):
        super(CircleIconLabel, self).__init__(parent)
        self.text = text
        self.bg_color = bg_color
        self.text_color = text_color
        self.station_num = station_num  # Optional number for station identifiers like "T20"
        self.setFixedSize(60, 60)
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Draw the text
        if self.station_num is None:
            # Draw the circle background
            painter.setPen(Qt.NoPen)
            painter.setBrush(QColor(self.bg_color))
            painter.drawEllipse(0, 0, self.width(), self.height())
            # Just draw the main letter centered
            font = QFont(FONT_NAME, 32, QFont.Bold)
            painter.setFont(font)
            painter.setPen(QColor(self.text_color))
            painter.drawText(0, 0, self.width(), self.height(), 
                             Qt.AlignCenter, self.text)
        else:
            # Draw a hollow circle
            painter.setPen(Qt.NoPen)
            painter.setBrush(QColor(self.bg_color))
            painter.drawEllipse(0, 0, self.width(), self.height())
            painter.setBrush(QColor("#FFFFFF"))
            painter.drawEllipse(4, 4, self.width() - 8, self.height() - 8)
            
            # Just draw the main letter centered with station number
            font = QFont(FONT_NAME, 20, QFont.Bold)
            painter.setBrush(QColor(self.bg_color))
            painter.setFont(font)
            painter.setPen(QColor(self.bg_color))
            painter.drawText(0, 0, self.width(), self.height(), 
                             Qt.AlignCenter, f"{self.text}{self.station_num}")


class TransferLineWidget(QWidget):
    def __init__(self, icon_text, bg_color, top_title, bottom_title, station_num=None, parent=None):
        super(TransferLineWidget, self).__init__(parent)
        
        # Store parameters
        self.icon_text = icon_text
        self.bg_color = bg_color
        self.top_title = top_title
        self.bottom_title = bottom_title
        self.station_num = station_num
        
        # Set widget properties
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        self.setStyleSheet(f"background-color: {MIDOSUJI_BACKGROUND_COLOR}; {BORDER_DEBUG}")
        self.setFixedHeight(70)
        
        # Create main layout
        main_layout = QHBoxLayout(self)
        text_layout = QVBoxLayout()
        
        # Create the circular icon (on the left)
        self.left_icon = CircleIconLabel(icon_text, bg_color, "white", station_num, self)
        
        # Create top title label (Japanese text)
        self.top_title_label = QLabel(top_title)
        self.top_title_label.setFont(QFont(FONT_NAME, 24, QFont.Bold))
        self.top_title_label.setStyleSheet(f"color: {BLACK_COLOR}; {BORDER_DEBUG}")
        
        # Create bottom title label (English text)
        self.bottom_title_label = QLabel(bottom_title)
        self.bottom_title_label.setFont(QFont(FONT_NAME, 20, QFont.Bold))
        self.bottom_title_label.setStyleSheet(f"color: {BLACK_COLOR}; {BORDER_DEBUG}")
        
        # Add widgets to text layout
        text_layout.addWidget(self.top_title_label)
        text_layout.addWidget(self.bottom_title_label)
        text_layout.setSpacing(5)
        text_layout.setContentsMargins(0, 5, 0, 5)
        
        # Add left icon and text to main layout
        main_layout.addWidget(self.left_icon)
        main_layout.addSpacing(10)
        main_layout.addLayout(text_layout)
        main_layout.addStretch(1)  # Push station number icon to the right edge
        
        # Set spacing and margins
        main_layout.setContentsMargins(10, 5, 10, 5)


class SceneTransferList(QWidget):
    def __init__(self):
        super().__init__()
        self.line_info = None
        self.station = None
        self.init_ui()
    
    def init_ui(self):
        # 主布局 - 垂直布局
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        
        self.setFixedSize(960, 342)
        
        # 1. 頂部標題區域 - 固定在頂部
        self.transfer_instruction = QLabel("のりかえ / Transfer")
        self.transfer_instruction.setFont(QFont(FONT_NAME, 28))
        self.transfer_instruction.setStyleSheet(f"color: {BLACK_COLOR}; {BORDER_DEBUG}")
        self.transfer_instruction.setAlignment(Qt.AlignCenter)
        self.transfer_instruction.setFixedSize(960, 50)
        self.main_layout.addWidget(self.transfer_instruction)
        
        # 2. 中間轉乘信息區域 - 會垂直居中
        # 使用一個容器來包含轉乘信息，這樣可以控制它在垂直方向上的居中
        self.transfer_container_outer = QWidget()
        self.transfer_container_outer.setFixedWidth(960)
        
        # 創建垂直布局使轉乘信息在容器中垂直居中
        self.transfer_container_layout = QVBoxLayout(self.transfer_container_outer)
        self.transfer_container_layout.setContentsMargins(0, 0, 0, 0)
        self.transfer_container_layout.setSpacing(0)
        
        # 添加頂部彈性空間
        self.transfer_container_layout.addStretch(1)
        
        # 創建水平布局實現轉乘信息的水平居中
        self.transfer_container_horizontal = QHBoxLayout()
        self.transfer_container_horizontal.setContentsMargins(0, 0, 0, 0)
        self.transfer_container_horizontal.setSpacing(0)
        
        # 創建實際包含轉乘項目的容器
        self.transfer_container = QWidget()
        self.transfer_container.setFixedWidth(960)
        
        # 轉乘項目的垂直布局
        self.transfer_info_layout = QVBoxLayout(self.transfer_container)
        self.transfer_info_layout.setContentsMargins(0, 0, 0, 0)
        self.transfer_info_layout.setSpacing(5)  # 項目之間的間距
        self.transfer_info_layout.setAlignment(Qt.AlignHCenter)  # 水平居中對齊
        
        # 將轉乘項目容器添加到水平居中布局
        self.transfer_container_horizontal.addStretch(1)  # 左側彈性空間
        self.transfer_container_horizontal.addWidget(self.transfer_container)
        self.transfer_container_horizontal.addStretch(1)  # 右側彈性空間
        
        # 將水平居中布局添加到垂直居中布局
        self.transfer_container_layout.addLayout(self.transfer_container_horizontal)
        
        # 添加底部彈性空間
        self.transfer_container_layout.addStretch(1)
        
        # 將轉乘容器添加到主布局
        self.main_layout.addWidget(self.transfer_container_outer)
        
        self.transfer_layouts = []
        
        # 初始化場景
        if self.line_info is not None and self.station is not None:
            self.update_scene()

    def update_scene(self):
        # 移除所有當前的轉乘條目
        while self.transfer_info_layout.count():
            child = self.transfer_info_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        
        if self.line_info is not None and self.station is not None:
            self.transfer_info = self.station.transfer
            self.transfer_layouts.clear()
            
            # 分類轉乘條目
            code_entries = []
            non_code_entries = []
            
            for item in self.transfer_info.entries:
                if item.code is not None:
                    code_entries.append(item)
                else:
                    non_code_entries.append(item)
            
            # 處理有 code 的條目，每個條目一行
            for entry in code_entries:
                layout_widget = self.create_code_transfer(entry)
                self.transfer_layouts.append(layout_widget)
                self.transfer_info_layout.addWidget(layout_widget)
                
            # 處理沒有 code 的條目，全部放在一行
            if non_code_entries:
                non_code_widget = self.create_non_code_transfers(non_code_entries)
                self.transfer_layouts.append(non_code_widget)
                self.transfer_info_layout.addWidget(non_code_widget)

    def create_code_transfer(self, entry):
        """創建有站點代碼的轉乘條目 (如 T20)"""
        # 創建一個容器 widget
        container = QWidget()
        container.setFixedWidth(960)  # 固定寬度
        
        # 在容器中使用水平佈局
        single_layout = QHBoxLayout(container)
        single_layout.setContentsMargins(0, 0, 0, 0)
        single_layout.setSpacing(0)
        
        # 添加左側彈性空間，幫助實現居中
        single_layout.addStretch(1)

        line_widget = TransferLineWidget(
            icon_text="T", 
            bg_color="#800080",  # Purple
            top_title=f"{TRANSFER_MAP[entry.name]}",
            bottom_title=f"{entry.name} Line"
        )
        station_widget = TransferLineWidget(
            icon_text="T", 
            bg_color="#800080",  # Purple
            top_title=self.station.name['jp'],
            bottom_title=self.station.name['en'],
            station_num="20"
        )
        station_widget.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        line_widget.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        single_layout.addWidget(line_widget)
        single_layout.addWidget(station_widget)
        
        # 添加右側彈性空間，幫助實現居中
        single_layout.addStretch(1)
        
        return container
        
    def create_non_code_transfers(self, entries):
        """將所有沒有站點代碼的轉乘條目放在同一行"""
        # 創建一個容器 widget
        container = QWidget()
        container.setFixedWidth(960)  # 固定寬度
        
        # 在容器中使用水平佈局
        row_layout = QHBoxLayout(container)
        row_layout.setContentsMargins(0, 0, 0, 0)
        row_layout.setSpacing(10)  # 項目之間的間距
        
        # 添加左側彈性空間，幫助實現居中
        row_layout.addStretch(1)
        
        # 添加所有無代碼的轉乘條目
        for entry in entries:
            line_widget = TransferLineWidget(
                icon_text="T", 
                bg_color="#800080",  # Purple
                top_title=f"{TRANSFER_MAP[entry.name]}",
                bottom_title=f"{entry.name} Line"
            )
            line_widget.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
            row_layout.addWidget(line_widget)
        
        # 添加右側彈性空間，幫助實現居中
        row_layout.addStretch(1)
        
        return container
        
    def receive_notify(self, line_info, display_station, station_state):
        self.line_info = line_info
        self.station = display_station
        self.station_state = station_state
        self.update_scene()


# Demo application
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Transit Line Widget Demo")
        self.resize(600, 400)
        
        # Create central widget with light background
        central = QWidget()
        central.setStyleSheet("background-color: #f0f0f0;")
        self.setCentralWidget(central)
        
        # Layout for central widget
        layout = QVBoxLayout(central)
        
        # Create all four widgets from the image
        # Tanimachi Line
        tanimachi_widget = TransferLineWidget(
            icon_text="T", 
            bg_color="#800080",  # Purple
            top_title="谷町線",
            bottom_title="Tanimachi Line"
        )
        
        # Higashi-Umeda Station
        higashi_umeda_widget = TransferLineWidget(
            icon_text="T", 
            bg_color="#800080",  # Purple
            top_title="東梅田駅",
            bottom_title="Higashi-Umeda Sta.",
            station_num="20"
        )
        
        # Yotsubashi Line
        yotsubashi_widget = TransferLineWidget(
            icon_text="Y", 
            bg_color="#3080C0",  # Blue
            top_title="四つ橋線",
            bottom_title="Yotsubashi Line"
        )
        
        # Nishi-Umeda Station
        nishi_umeda_widget = TransferLineWidget(
            icon_text="Y", 
            bg_color="#3080C0",  # Blue
            top_title="西梅田駅",
            bottom_title="Nishi-Umeda Sta.",
            station_num="11"
        )
        
        # Add separators between widgets
        layout.addWidget(tanimachi_widget)
        layout.addWidget(create_separator())
        layout.addWidget(higashi_umeda_widget)
        layout.addWidget(create_separator())
        layout.addWidget(yotsubashi_widget)
        layout.addWidget(create_separator())
        layout.addWidget(nishi_umeda_widget)
        
        layout.addStretch(1)  # Push everything to the top


def create_separator():
    """Create a horizontal separator line"""
    line = QFrame()
    line.setFrameShape(QFrame.HLine)
    line.setFrameShadow(QFrame.Sunken)
    return line


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())