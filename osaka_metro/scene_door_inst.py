import sys
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import QPropertyAnimation, QRect, QEasingCurve, Qt
from PyQt5.QtGui import QPainter, QPolygon, QColor, QLinearGradient, QBrush
from PyQt5.QtCore import QPoint, Qt, QPropertyAnimation, QRect
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QVBoxLayout, QSpacerItem,
                            QHBoxLayout, QSizePolicy, QMainWindow, QFrame)
import sys
from osaka_metro.osaka_metro import *

class TrainDoor(QWidget):
    def __init__(
        self,
        image_path: str = "osaka_metro\\doors\\doors.png",
        side: str = "left",
        desired_height: int = 300,
        side_image_left: str = "osaka_metro\\doors\\door_side_left.png",
        side_image_right: str = "osaka_metro\\doors\\door_side_right.png",
        parent=None
    ):
        super().__init__(parent)
        self.side = side.lower()
        self.image_path = image_path

        # === 門圖處理 ===
        full_pixmap = QPixmap(self.image_path)
        scale_factor = desired_height / full_pixmap.height()
        full_pixmap = full_pixmap.scaledToHeight(desired_height, Qt.SmoothTransformation)

        half_width = full_pixmap.width() // 2

        if self.side == "left":
            door_pixmap = full_pixmap.copy(0, 0, half_width, desired_height)
        elif self.side == "right":
            door_pixmap = full_pixmap.copy(half_width, 0, half_width, desired_height)
        else:
            raise ValueError("side 必須是 'left' 或 'right'")

        # === 側邊貼圖處理 ===
        if self.side == "left":
            side_pixmap = QPixmap(side_image_left).scaledToHeight(desired_height, Qt.SmoothTransformation)
        else:
            side_pixmap = QPixmap(side_image_right).scaledToHeight(desired_height, Qt.SmoothTransformation)

        side_width = side_pixmap.width()

        # === 建立 QLabel ===
        self.side_label = QLabel(self)
        self.side_label.setPixmap(side_pixmap)
        self.side_label.setGeometry(0, 0, side_width, desired_height)

        self.door_label = QLabel(self)
        self.door_label.setPixmap(door_pixmap)

        if self.side == "left":
            self.door_label.setGeometry(side_width, 0, half_width, desired_height)
        else:
            self.door_label.setGeometry(0, 0, half_width, desired_height)
            self.side_label.setGeometry(half_width, 0, side_width, desired_height)

        total_width = half_width + side_width
        self.setFixedSize(total_width, desired_height)

    def animate(self):
        # 先把側邊圖層提到最上層
        self.side_label.raise_()

        anim = QPropertyAnimation(self.door_label, b"geometry")
        anim.setDuration(1000)
        anim.setEasingCurve(QEasingCurve.OutCubic)
        start_rect = self.door_label.geometry()

        if self.side == "left":
            end_rect = QRect(-start_rect.width(), 0, start_rect.width(), start_rect.height())
        else:  # right
            end_rect = QRect(self.width(), 0, start_rect.width(), start_rect.height())

        anim.setStartValue(start_rect)
        anim.setEndValue(end_rect)
        anim.start()
        self.animation = anim  # 保持參考


class ArrowWidget(QWidget):
    def __init__(self, side='left', parent=None):
        super().__init__(parent)
        self.side = side.lower()
        if self.side not in ('left', 'right'):
            raise ValueError("side 必須是 'left' 或 'right'")
        
        self.setMinimumSize(150, 150)
        self.setMaximumSize(300, 300)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        width = self.width()
        height = 100
        arrow_width = int(width * 0.6)
        arrow_height = int(100 * 0.5)
        center_y = height // 2

        if self.side == 'left':
            arrow = QPolygon([
                QPoint(arrow_width, center_y - arrow_height // 2),
                QPoint(int(arrow_width * 0.4), center_y - arrow_height // 2),
                QPoint(int(arrow_width * 0.4), center_y - arrow_height),
                QPoint(0, center_y),
                QPoint(int(arrow_width * 0.4), center_y + arrow_height),
                QPoint(int(arrow_width * 0.4), center_y + arrow_height // 2),
                QPoint(arrow_width, center_y + arrow_height // 2),
            ])

            gradient = QLinearGradient(0, 0, width, 0)
            gradient.setColorAt(0, QColor("#007BFF"))
            gradient.setColorAt(0.8, QColor(0, 123, 255, 150))
            gradient.setColorAt(1.0, QColor(0, 123, 255, 0))

        else:  # side == 'right'
            arrow = QPolygon([
                QPoint(width - arrow_width, center_y - arrow_height // 2),
                QPoint(width - int(arrow_width * 0.4), center_y - arrow_height // 2),
                QPoint(width - int(arrow_width * 0.4), center_y - arrow_height),
                QPoint(width, center_y),
                QPoint(width - int(arrow_width * 0.4), center_y + arrow_height),
                QPoint(width - int(arrow_width * 0.4), center_y + arrow_height // 2),
                QPoint(width - arrow_width, center_y + arrow_height // 2),
            ])

            gradient = QLinearGradient(width, 0, 0, 0)
            gradient.setColorAt(0, QColor("#007BFF"))
            gradient.setColorAt(0.8, QColor(0, 123, 255, 150))
            gradient.setColorAt(1.0, QColor(0, 123, 255, 0))

        painter.setBrush(QBrush(gradient))
        painter.setPen(Qt.NoPen)
        painter.drawPolygon(arrow)
        painter.end()

    def animate(self):
        self.raise_()  # 確保箭頭在頂層（如果有重疊）

        anim = QPropertyAnimation(self, b"geometry")
        anim.setDuration(600)
        #anim.setEasingCurve(Qt.EaseOutCubic)
        start_rect = self.geometry()

        dx = self.width() // 2
        if self.side == 'left':
            end_rect = QRect(start_rect.x() - dx, start_rect.y(), start_rect.width(), start_rect.height())
        else:
            end_rect = QRect(start_rect.x() + dx, start_rect.y(), start_rect.width(), start_rect.height())

        anim.setStartValue(start_rect)
        anim.setEndValue(end_rect)
        anim.start()
        self.anim = anim  # 保持引用避免被GC


class SceneDoorInst(QWidget):
    def __init__(self):
        super().__init__()

        # 主布局 - 垂直布局
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        
        self.setFixedSize(960, 342)
        
        # 1. 頂部標題區域 - 固定在頂部
        self.transfer_instruction = QLabel(DOOR_OPEN_INST[0])
        self.transfer_instruction.setFont(QFont(FONT_NAME, 24))
        self.transfer_instruction.setStyleSheet(f"color: #e5171f; background-color: {TRANSFER_GREY_COLOR}; {BORDER_DEBUG}")
        self.transfer_instruction.setAlignment(Qt.AlignCenter)
        self.transfer_instruction.setFixedSize(960, 50)
        self.main_layout.addWidget(self.transfer_instruction)
        
        # 2. 中間轉乘信息區域 - 會垂直居中
        # 使用一個容器來包含轉乘信息，這樣可以控制它在垂直方向上的居中
        self.transfer_container_outer = QWidget()
        self.transfer_container_outer.setFixedWidth(960)

        desired_height = 342 - 50

        layout = QHBoxLayout(self.transfer_container_outer)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # 左右空白 spacer（置中用）
        spacer = QSpacerItem(40, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)

        layout.addSpacerItem(spacer)
        layout.setAlignment(Qt.AlignCenter)

        # 左箭頭
        self.left_arrow = ArrowWidget(side='left')
        self.left_arrow.setFixedHeight(100)
        layout.addWidget(self.left_arrow)

        # 50px 固定空隙
        layout.addSpacing(50)

        # 左門
        self.left_door = TrainDoor(side='left', desired_height=desired_height)
        layout.addWidget(self.left_door)

        # 右門
        self.right_door = TrainDoor(side='right', desired_height=desired_height)
        layout.addWidget(self.right_door)

        layout.addSpacing(50)

        # 右箭頭
        self.right_arrow = ArrowWidget(side='right')
        self.right_arrow.setFixedHeight(100)
        layout.addWidget(self.right_arrow)

        # 再加一個 spacer 對稱
        layout.addSpacerItem(spacer)

        #self.setLayout(layout)
        self.main_layout.addWidget(self.transfer_container_outer)

    def animate_doors(self):
        self.left_door.animate()
        self.right_door.animate()
        self.left_arrow.animate()
        self.right_arrow.animate()

    def update_scene(self):
        pass

    def on_scene_present(self):
        self.animate_doors()

    def receive_notify(self, line_info, display_station, station_state):
        self.line_info = line_info
        self.station = display_station
        self.station_state = station_state
        self.update_scene()


# 測試
if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = SceneDoorInst()
    w.setWindowTitle("Train Door Panel")
    w.show()

    # 動畫測試（延遲執行）
    from PyQt5.QtCore import QTimer
    QTimer.singleShot(1000, w.animate_doors)

    sys.exit(app.exec_())
