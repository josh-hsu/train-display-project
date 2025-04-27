import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QPainter, QPolygon, QColor, QPen
from PyQt5.QtCore import QPoint, Qt

class ArrowWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('箭頭圖案')
        self.resize(300, 100)

    def paintEvent(self, event):
        painter = QPainter(self)

        # 畫背景
        painter.fillRect(0, 0, self.width() // 2, self.height(), QColor(255, 0, 0))  # 紅色左半邊
        painter.fillRect(self.width() // 2, 0, self.width() // 2, self.height(), QColor(160, 160, 160))  # 灰色右半邊

        # 設定畫筆
        pen = QPen(Qt.NoPen)
        painter.setPen(pen)
        painter.setBrush(QColor(0, 0, 255))  # 藍色

        # 箭頭參數
        arrow_width = self.height() * 0.6
        arrow_height = self.height() * 0.8
        spacing = 10  # 箭頭間距
        start_x = self.width() * 0.6

        for i in range(3):
            offset = i * (arrow_width * 0.6 + spacing)
            points = QPolygon([
                QPoint(start_x - offset, self.height() // 2),
                QPoint(start_x - offset + arrow_width * 0.6, self.height() // 2 - arrow_height / 2),
                QPoint(start_x - offset + arrow_width * 0.6, self.height() // 2 - arrow_height / 4),
                QPoint(start_x - offset + arrow_width, self.height() // 2 - arrow_height / 4),
                QPoint(start_x - offset + arrow_width, self.height() // 2 + arrow_height / 4),
                QPoint(start_x - offset + arrow_width * 0.6, self.height() // 2 + arrow_height / 4),
                QPoint(start_x - offset + arrow_width * 0.6, self.height() // 2 + arrow_height / 2),
            ])
            painter.drawPolygon(points)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = ArrowWidget()
    widget.show()
    sys.exit(app.exec_())
