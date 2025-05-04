from PyQt5.QtWidgets import QLabel, QApplication, QWidget
from PyQt5.QtGui import QPainter, QTransform, QFont
from PyQt5.QtCore import Qt
import sys

class RotatedLabel(QLabel):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setFont(QFont("Arial", 14))
        self.setMinimumSize(150, 100)  # 調整大小方便顯示旋轉後的文字

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # 將支點設在 QLabel 左下角
        transform = QTransform()
        transform.translate(0, self.height())  # 移動到左下角
        transform.rotate(-45)  # 向上旋轉 45 度（逆時針）

        painter.setTransform(transform)
        painter.drawText(0, 0, self.text())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = QWidget()
    window.setWindowTitle("Rotated QLabel Demo")
    
    label = RotatedLabel("Sample Text", window)
    label.move(50, 50)
    
    window.resize(300, 200)
    window.show()
    sys.exit(app.exec_())
