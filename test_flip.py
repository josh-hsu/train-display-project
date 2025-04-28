from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtGui import QPainter, QBrush, QColor, QPolygon
from PyQt5.QtCore import QPoint, Qt
import sys

class MovingArrow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(120, 40)  # 預設尺寸，可自己調整

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(Qt.NoPen)

        # 紅色部分
        red_brush = QBrush(QColor(255, 0, 0))
        painter.setBrush(red_brush)
        
        red1 = QPolygon([QPoint(0,0), QPoint(20,0), QPoint(0,18)])
        red2 = QPolygon([QPoint(0,18), QPoint(20,36), QPoint(0,36)])
        painter.drawPolygon(red1)
        painter.drawPolygon(red2)

        # 藍色部分
        blue_brush = QBrush(QColor(0, 0, 255))
        painter.setBrush(blue_brush)

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
        grey_brush = QBrush(QColor(160, 160, 160))
        painter.setBrush(grey_brush)
        grey = QPolygon([
            QPoint(60,2), QPoint(43,18), QPoint(60,34)
        ])
        painter.drawPolygon(grey)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MovingArrow()
    w.show()
    sys.exit(app.exec_())
