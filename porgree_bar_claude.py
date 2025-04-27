from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QColor, QPainterPath
from PyQt5.QtCore import Qt

class ProgressBarWithArrows(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.progress = 0.0  # 0.0 ~ 1.0
        self.setFixedHeight(100)
        self.arrow_color = QColor(0, 120, 215)  # Blue color for center arrow
        self.chevron_count = 3  # Number of chevrons to draw

    def setProgress(self, value):
        self.progress = max(0.0, min(1.0, value))
        self.update()
        
    def setArrowColor(self, color):
        self.arrow_color = color
        self.update()
        
    def setChevronCount(self, count):
        self.chevron_count = max(1, count)
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        w = self.width()
        h = self.height()
        leftside_gray_offset = 200
        leftside_arrow_offset = 80

        # Draw background (gray)
        painter.setBrush(QColor(131, 131, 131))
        painter.setPen(Qt.NoPen)
        painter.drawRect(leftside_gray_offset, 0, w, h)

        # Red progress bar parameters
        arrow_w = 30  # Arrow width
        arrow_h = h  # Arrow height
        red_width = int(w * self.progress)

        if red_width > arrow_w:
            # Draw red bar (between left and right arrows)
            painter.setBrush(QColor(220, 0, 0))
            painter.drawRect(leftside_arrow_offset, 0, red_width - arrow_w, h)

            # Draw left arrow
            left_arrow = QPainterPath()
            left_arrow.moveTo(leftside_arrow_offset, 0)
            left_arrow.lineTo(leftside_arrow_offset - arrow_w, h/2)
            left_arrow.lineTo(leftside_arrow_offset, h)
            left_arrow.closeSubpath()

            painter.drawPath(left_arrow)

            # Draw right arrow
            right_arrow = QPainterPath()
            base_x = red_width
            right_arrow.moveTo(base_x, h//2)
            right_arrow.lineTo(base_x + arrow_w, h//2 - arrow_h//2)
            right_arrow.lineTo(base_x + arrow_w, h//2 + arrow_h//2)
            right_arrow.closeSubpath()

            painter.drawPath(right_arrow)
            
            # Draw center transition chevron arrows (blue)
            chevron_width = 15
            chevron_spacing = 5
            chevron_height = h * 0.7  # 70% of the height
            
            # Calculate center position (at the end of red section)
            center_x = red_width
            
            # Set color for chevrons
            painter.setBrush(self.arrow_color)
            
            # Draw multiple chevrons
            for i in range(self.chevron_count):
                offset = i * (chevron_width + chevron_spacing)
                
                chevron = QPainterPath()
                chevron.moveTo(center_x - offset, (h - chevron_height) / 2)
                chevron.lineTo(center_x - chevron_width - offset, h / 2)
                chevron.lineTo(center_x - offset, (h + chevron_height) / 2)
                chevron.closeSubpath()
                
                painter.drawPath(chevron)

        painter.end()