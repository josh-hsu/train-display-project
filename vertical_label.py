from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QApplication
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
import sys

class VerticalText(QWidget):
    def __init__(self, text='', parent=None, font=QFont("Noto Sans JP", 40, QFont.Bold)):
        super().__init__(parent)
        self.layout = QVBoxLayout()
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)
        self.user_font = font

        self.setText(text)  # 呼叫下面的 setText

    def setText(self, text):
        # 先清掉舊的 label
        while self.layout.count():
            child = self.layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        # 逐字產生新的 label
        for char in text:
            label = QLabel(char)
            label.setFont(self.user_font)
            label.setAlignment(Qt.AlignCenter)
            label.setStyleSheet("font-size: 24px;")  # 這裡可以改字體大小
            self.layout.addWidget(label)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = VerticalText("心斎橋")
    w.show()

    # 測試 2 秒後改字
    from PyQt5.QtCore import QTimer
    def change_text():
        w.setText("梅田")
    QTimer.singleShot(2000, change_text)

    sys.exit(app.exec_())
