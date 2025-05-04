import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QLabel, QVBoxLayout, 
                             QHBoxLayout, QWidget, QSpacerItem, QSizePolicy)
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QPainter, QTransform


class RotatedLabel(QLabel):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.angle = -45  # 向上旋轉45度（在Qt中旋轉方向是逆時針）
        self.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        # 確保標籤有足夠大小顯示旋轉後的文本
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.setRenderHint(QPainter.TextAntialiasing, True)
        
        # 儲存當前畫筆狀態
        painter.save()
        
        # 平移到左邊中點（支點）
        painter.translate(0, self.height() // 2)
        
        # 旋轉
        painter.rotate(self.angle)
        
        # 繪製文字
        painter.drawText(0, 0, self.text())
        
        # 恢復畫筆狀態
        painter.restore()
        
    def minimumSizeHint(self):
        # 確保有足夠的空間顯示旋轉後的文字
        font_metrics = self.fontMetrics()
        text_width = font_metrics.horizontalAdvance(self.text())
        text_height = font_metrics.height()
        
        # 計算旋轉後的尺寸
        diagonal = (text_width**2 + text_height**2)**0.5
        return QSize(int(diagonal * 0.7), int(diagonal * 0.7))
        
    def sizeHint(self):
        return self.minimumSizeHint()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        # 創建主widget和layout
        central_widget = QWidget()
        main_layout = QHBoxLayout(central_widget)
        
        # 創建左側空間
        main_layout.addSpacing(20)  # 左側邊距
        
        # 創建旋轉的標籤
        rotated_label = RotatedLabel("Hello World! This is a rotated text.")
        
        # 將旋轉標籤添加到主佈局中
        main_layout.addWidget(rotated_label)
        
        # 添加右側空間，讓旋轉標籤有足夠的顯示空間
        main_layout.addSpacing(150)
        
        # 設置並顯示主窗口
        self.setCentralWidget(central_widget)
        self.setWindowTitle('Rotated QLabel Demo')
        self.setGeometry(100, 100, 400, 200)
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())