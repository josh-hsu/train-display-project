# animated_text_view.py

from PyQt5.QtWidgets import QWidget, QStackedLayout
from PyQt5.QtCore import QTimer, QPropertyAnimation, QPoint, QParallelAnimationGroup, QRect, QEasingCurve, Qt

from auto_stretch_label import AutoStretchLabel

class AnimatedTextView:
    def __init__(self, width, height, data, interval_ms=3000, anim_duration_ms=500, animation_type="slide"):
        self.data = data
        self.index = 0
        self.width = width
        self.height = height
        self.interval = interval_ms
        self.anim_duration = anim_duration_ms
        self.animation_type = animation_type  # "slide" or "fold"

        self.container = QWidget()
        self.container.setFixedSize(width, height)

        self.stack_layout = QStackedLayout()
        self.container.setLayout(self.stack_layout)

        self.labels = []

        for text in self.data:
            label = AutoStretchLabel(text)
            label.setAlignment(Qt.AlignCenter)
            label.setStyleSheet("font-size: 32px; color: white; background-color: #111;")
            self.stack_layout.addWidget(label)
            self.labels.append(label)

        self.timer = QTimer()
        self.timer.timeout.connect(self.animate_next)

        self.animation_group = None

    def widget(self):
        return self.container

    def setStyleSheet(self, index, style):
        if 0 <= index < len(self.labels):
            self.labels[index].setStyleSheet(style)
        else:
            raise IndexError("Index out of range for labels.")
    
    def setStyleSheetAll(self, style):
        for label in self.labels:
            label.setStyleSheet(style)

    def setFont(self, font):
        for label in self.labels:
            label.setFont(font)
    
    def setAlignment(self, alignment):
        for label in self.labels:
            label.setAlignment(alignment)
            
    def start(self):
        self.timer.start(self.interval)

    def stop(self):
        self.timer.stop()

    def animate_next(self):
        current_label = self.labels[self.index]
        next_index = (self.index + 1) % len(self.labels)
        next_label = self.labels[next_index]

        self.stack_layout.setCurrentWidget(current_label)
        next_label.show()

        if self.animation_type == "slide":
            self._animate_slide(current_label, next_label)
        elif self.animation_type == "fold":
            self._animate_fold(current_label, next_label)

    def _animate_slide(self, current_label, next_label):
        w = self.width
        h = self.height

        current_label.move(0, 0)
        next_label.move(w, 0)

        anim_out = QPropertyAnimation(current_label, b"pos")
        anim_out.setDuration(self.anim_duration)
        anim_out.setStartValue(QPoint(0, 0))
        anim_out.setEndValue(QPoint(-w, 0))

        anim_in = QPropertyAnimation(next_label, b"pos")
        anim_in.setDuration(self.anim_duration)
        anim_in.setStartValue(QPoint(w, 0))
        anim_in.setEndValue(QPoint(0, 0))

        self.animation_group = QParallelAnimationGroup()
        self.animation_group.addAnimation(anim_out)
        self.animation_group.addAnimation(anim_in)

        def slide_finish():
            self.index = (self.index + 1) % len(self.labels)
            current_label.move(0, 0)  # reset
            self.stack_layout.setCurrentWidget(next_label)

        self.animation_group.finished.connect(slide_finish)
        self.animation_group.start()

    def _animate_fold(self, current_label, next_label):
        w = self.width
        h = self.height

        # Reset positions
        current_label.setGeometry(0, 0, w, h)
        next_label.setGeometry(0, 0, w, 0)  # Start with height of 0

        anim_out = QPropertyAnimation(current_label, b"geometry")
        anim_out.setDuration(self.anim_duration)
        anim_out.setStartValue(QRect(0, 0, w, h))
        anim_out.setEndValue(QRect(0, h, w, h))
        anim_out.setEasingCurve(QEasingCurve.InOutCubic)

        anim_in = QPropertyAnimation(next_label, b"geometry")
        anim_in.setDuration(self.anim_duration)
        anim_in.setStartValue(QRect(0, 0, w, 0))
        anim_in.setEndValue(QRect(0, 0, w, h))
        anim_in.setEasingCurve(QEasingCurve.InOutCubic)

        self.animation_group = QParallelAnimationGroup()
        self.animation_group.addAnimation(anim_out)
        self.animation_group.addAnimation(anim_in)

        def fold_finish():
            self.index = (self.index + 1) % len(self.labels)  # Fixed: use self.labels instead
            current_label.setGeometry(0, 0, w, h)  # Reset geometry
            next_label.setGeometry(0, 0, w, h)     # Reset geometry
            self.stack_layout.setCurrentWidget(next_label)

        self.animation_group.finished.connect(fold_finish)
        self.animation_group.start()