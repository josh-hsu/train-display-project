from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QFont, QFontMetrics
from PyQt5.QtCore import pyqtProperty, Qt

class AutoStretchLabel(QLabel):
    def __init__(self, text="", parent=None):
        super().__init__(text, parent)
        self._font_size = 32  # 預設字型大小

    def getFontSize(self):
        return self._font_size

    def setFontSize(self, size):
        self._font_size = size
        font = self.font()
        font.setPointSize(size)
        self.setFont(font)

    fontSize = pyqtProperty(int, getFontSize, setFontSize)

    def setText(self, text):
        super().setText(text)
        self.adjust_text_stretch()

    def setFont(self, font):
        super().setFont(font)
        self.base_font = font

    def adjust_text_stretch(self):
        fm = QFontMetrics(self.font())
        text_width = fm.width(self.text())
        label_width = self.width()

        font = self.font()

        if text_width > label_width:
            stretch_ratio = (label_width / text_width) * 100
            stretch_ratio = max(1, int(stretch_ratio))
            font.setStretch(stretch_ratio)
        else:
            font.setStretch(100)

        self.setFont(font)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.adjust_text_stretch()
