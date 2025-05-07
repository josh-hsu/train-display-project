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
            font = QFont("Arial", 32, QFont.Bold)
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
            font = QFont("Arial", 20, QFont.Bold)
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
        self.setFixedHeight(70)
        
        # Create main layout
        main_layout = QHBoxLayout(self)
        text_layout = QVBoxLayout()
        
        # Create the circular icon (on the left)
        self.left_icon = CircleIconLabel(icon_text, bg_color, "white", station_num, self)
        
        # Create top title label (Japanese text)
        self.top_title_label = QLabel(top_title)
        self.top_title_label.setFont(QFont("Arial", 14, QFont.Bold))
        
        # Create bottom title label (English text)
        self.bottom_title_label = QLabel(bottom_title)
        self.bottom_title_label.setFont(QFont("Arial", 12))
        self.bottom_title_label.setStyleSheet("color: black;")
        
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
        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        self.main_layout.setAlignment(Qt.AlignCenter)
        self.setStyleSheet(f"background-color: {MIDOSUJI_BACKGROUND_COLOR}; {BORDER_DEBUG}")
        self.setFixedSize(960, 342)

        if self.line_info is not None and self.station is not None:
            self.transfer_info = self.station.transfer
            self.transfer_layouts = []
            for item in self.transfer_info.entries:
                layout = self.create_single_transfer(item)
                self.transfer_layouts.append(layout)
                self.main_layout.addLayout(layout)
        
        self.setLayout(self.main_layout)

    def update_scene(self):
        while self.main_layout.count():
            child = self.main_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        
        if self.line_info is not None and self.station is not None:
            self.transfer_info = self.station.transfer
            self.transfer_layouts = []
            for item in self.transfer_info.entries:
                layout = self.create_single_transfer(item)
                self.transfer_layouts.append(layout)
                self.main_layout.addLayout(layout)


    def create_single_transfer(self, entry:TransferEntry):
        single_layout = QHBoxLayout()
        single_layout.setContentsMargins(0, 0, 0, 0)
        single_layout.setSpacing(0)
        single_layout.setAlignment(Qt.AlignHCenter)

        if entry.code is not None:
            line_widget = TransferLineWidget(
                icon_text="T", 
                bg_color="#800080",  # Purple
                top_title=f"{TRANSFER_MAP[entry.name]}",
                bottom_title=entry.name
            )
            station_widget = TransferLineWidget(
                icon_text="T", 
                bg_color="#800080",  # Purple
                top_title=self.station.name['jp'],
                bottom_title=self.station.name['en'],
                station_num="20"
            )
            single_layout.addWidget(line_widget)
            single_layout.addWidget(station_widget)
        else:
            line_widget = TransferLineWidget(
                icon_text="T", 
                bg_color="#800080",  # Purple
                top_title=f"{TRANSFER_MAP[entry.name]}",
                bottom_title=entry.name
            )
            single_layout.addWidget(line_widget)
        return single_layout
        
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