import sys
import yaml
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout
)
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt, QTimer


class DisplayPanel(QWidget):
    def __init__(self, yaml_file):
        super().__init__()

        # 讀取 YAML
        with open(yaml_file, 'r', encoding='utf-8') as f:
            self.data = yaml.safe_load(f)

        self.stations = self.data['line']['stations']
        self.line_name = self.data['line']['name_display']
        self.current_index = 0

        # 解析 display size
        self.window_width, self.window_height = self.get_display_size()

        self.setWindowTitle(f"{self.line_name} 模擬顯示器")
        self.setFixedSize(self.window_width, self.window_height)

        self.initUI()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.next_station)
        self.timer.start(5000)

    def get_display_size(self):
        display_conf = self.data['line'].get('displays', [])
        if display_conf:
            size_str = display_conf[0].get('size', '')
            if '*' in size_str:
                try:
                    width_str, height_str = size_str.split('*')
                    return int(width_str.strip()), int(height_str.strip())
                except ValueError:
                    pass
        # fallback 預設值
        return 600, 400

    def initUI(self):
        self.label_line = QLabel(f"路線：{self.line_name}")
        self.label_line.setFont(QFont("Arial", 14, QFont.Bold))

        self.label_current = QLabel("")
        self.label_next = QLabel("")
        self.label_image = QLabel("")
        self.label_image.setFixedHeight(200)
        self.label_image.setAlignment(Qt.AlignCenter)

        self.button_next = QPushButton("下一站 ▶")
        self.button_next.clicked.connect(self.next_station)

        layout = QVBoxLayout()
        layout.addWidget(self.label_line)
        layout.addWidget(self.label_current)
        layout.addWidget(self.label_next)
        layout.addWidget(self.label_image)
        layout.addWidget(self.button_next, alignment=Qt.AlignRight)
        self.setLayout(layout)

        self.update_display()

    def update_display(self):
        if self.current_index >= len(self.stations):
            self.label_current.setText("終點站到達")
            self.label_next.setText("")
            self.label_image.clear()
            return

        current = self.stations[self.current_index]
        next_station = (
            self.stations[self.current_index + 1]
            if self.current_index + 1 < len(self.stations)
            else None
        )

        self.label_current.setText(f"目前：{current['name_display']} ({current['name']})")
        if next_station:
            self.label_next.setText(f"下一站：{next_station['name_display']} ({next_station['name']})")
        else:
            self.label_next.setText("下一站：終點站")

        img_path = current.get("display_image", "")
        if img_path:
            pixmap = QPixmap(img_path).scaledToHeight(200, Qt.SmoothTransformation)
            self.label_image.setPixmap(pixmap)
        else:
            self.label_image.clear()

    def next_station(self):
        self.current_index += 1
        self.update_display()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    panel = DisplayPanel("osaka_metro/midosuji_line.yaml")
    panel.show()
    sys.exit(app.exec_())
