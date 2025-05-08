import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout
)
from PyQt5.QtGui import QPainter, QPen, QColor, QFont
from PyQt5.QtCore import Qt, QPropertyAnimation, QRect


# 單一車廂
class SingleCabWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(130, 50)
        self.text = None  # 初始不顯示文字

    def setLabel(self, text):
        self.text = text
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        pen = QPen(Qt.black, 2)
        painter.setPen(pen)
        painter.setBrush(Qt.transparent)
        painter.drawRect(1, 1, self.width() - 2, self.height() - 2)

        # 畫上文字（如有）
        if self.text:
            painter.setPen(QPen(Qt.black))
            font = QFont("Noto Sans JP", 32, QFont.Bold)
            painter.setFont(font)
            painter.drawText(self.rect(), Qt.AlignCenter, self.text)



# 十節車廂列車
class TrainCabWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.cabs = []
        layout = QHBoxLayout()
        layout.setSpacing(2)
        layout.setContentsMargins(0, 0, 0, 0)

        for i in range(10):
            cab = SingleCabWidget()
            self.cabs.append(cab)
            layout.addWidget(cab)
            if i == 4:
                layout.addSpacing(8)

        self.setLayout(layout)
        total_width = 10 * 130 + 9 * 2 + 8
        self.setFixedSize(total_width, 50)

    def labelRearFiveCabs(self):
        for i in range(5):
            label = str(i + 1)
            self.cabs[9 - i].setLabel(label)  # 從最右邊開始標 5→1


# 動畫容器：TrainMovingWidget
class TrainMovingWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(960, 80)
        self.setStyleSheet("background-color: white;")

        self.train_widget = TrainCabWidget()
        self.train_widget.setParent(self)

        # 動畫初始與結束位置
        start_x = self.width() - 130
        cab_full_width = 130 + 2
        end_x = -5 * cab_full_width

        self.animation = QPropertyAnimation(self.train_widget, b"geometry")
        self.animation.setDuration(1500)
        self.animation.setStartValue(QRect(start_x, 15, self.train_widget.width(), self.train_widget.height()))
        self.animation.setEndValue(QRect(end_x, 15, self.train_widget.width(), self.train_widget.height()))
        self.animation.finished.connect(self.onAnimationFinished)
        self.animation.start()

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        painter.fillRect(self.rect(), QColor("#FFFFFF"))

        pen = QPen(Qt.black, 4)
        painter.setPen(pen)
        x_start = 0
        y_pos = 65
        line_len = 720
        painter.drawLine(x_start, y_pos, x_start + line_len, y_pos)
        pen = QPen(Qt.red, 4)
        painter.setPen(pen)
        y_pos = 69
        painter.drawLine(x_start, y_pos, x_start + line_len, y_pos)

    def onAnimationFinished(self):
        self.train_widget.labelRearFiveCabs()
        

# 黑色訊息欄
class MessageInfoWidget(QLabel):
    def __init__(self):
        super().__init__()
        self.setFixedSize(960, 50)
        self.setFont(QFont("Noto Sans JP", 28, QFont.Bold))
        self.setText("こちら側のドアが開きます")
        self.setStyleSheet("background-color: black; color: red;")
        self.setAlignment(Qt.AlignCenter)


# 出口資訊（保留白底）
class GateLayoutWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(960, 210)
        self.setStyleSheet("background-color: white;")

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), QColor("#D9DBDC"))


# 主組合視圖
class GateInfoWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(960, 340)

        layout = QVBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)

        self.gate_info = GateLayoutWidget()
        self.train_view = TrainMovingWidget()
        self.message_info = MessageInfoWidget()

        layout.addWidget(self.gate_info)
        layout.addWidget(self.train_view)
        layout.addWidget(self.message_info)

        self.setLayout(layout)


# 執行主視窗
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GateInfoWidget()
    window.show()
    sys.exit(app.exec_())
