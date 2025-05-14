from PyQt5.QtCore import QTimer, QPropertyAnimation, QPoint, QParallelAnimationGroup, QEasingCurve, Qt
from PyQt5.QtGui import QFont, QFontMetrics, QTransform, QPainter
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QComboBox, QHBoxLayout, QSpinBox
from PyQt5.QtWidgets import QWidget, QStackedLayout, QLabel, QGraphicsOpacityEffect
import sys

class StretchTextLabel(QLabel):
    """
    一個標籤控件，能夠自動調整文字寬度以確保內容完全顯示在控件中。
    """
    def __init__(self, text="", parent=None):
        super().__init__(text, parent)
        self.base_font = self.font()  # 保存原始字體設置
        self.setWordWrap(False)  # 確保文字不會換行
        
    def setText(self, text):
        """設置文字並調整顯示"""
        super().setText(text)
        self.adjustTextDisplay()
    
    def setFont(self, font):
        """設置字體並保存基準字體"""
        super().setFont(font)
        self.base_font = QFont(font)  # 深拷貝字體作為基準
        self.adjustTextDisplay()
        
    def adjustTextDisplay(self):
        """調整文字顯示以適應標籤寬度"""
        if not self.text() or self.width() <= 0:
            return
            
        # 恢復原始字體以重新計算
        font = QFont(self.base_font)
        super().setFont(font)
        
        # 計算文字需要的寬度
        metrics = QFontMetrics(font)
        text_width = metrics.horizontalAdvance(self.text())
        available_width = self.width() - 10  # 留出少量邊距
        
        if text_width > available_width and available_width > 0:
            # 計算需要的壓縮率
            stretch_factor = min(100, max(10, int((available_width / text_width) * 100)))
            
            # 應用壓縮
            font.setStretch(stretch_factor)
            super().setFont(font)
            
            # 如果壓縮過度（低於50%），考慮減小字體大小
            if stretch_factor < 50:
                current_size = font.pointSize()
                if current_size > 0:
                    # 逐步減小字體直到合適
                    while stretch_factor < 50 and current_size > 8:  # 最小字體大小為8
                        current_size -= 1
                        font.setPointSize(current_size)
                        font.setStretch(100)  # 重置壓縮
                        super().setFont(font)
                        
                        # 重新計算
                        metrics = QFontMetrics(font)
                        text_width = metrics.horizontalAdvance(self.text())
                        
                        if text_width <= available_width:
                            break
                        
                        stretch_factor = min(100, max(10, int((available_width / text_width) * 100)))
                        font.setStretch(stretch_factor)
                        super().setFont(font)
    
    def resizeEvent(self, event):
        """當控件大小改變時調整文字"""
        super().resizeEvent(event)
        self.adjustTextDisplay()

class AnimatedTextView_T(QWidget):
    """
    一個可以自動輪播文字的控件，具有多種動畫效果。
    """
    ANIMATION_SLIDE = "slide"  # 滑動動畫
    ANIMATION_FOLD = "fold"    # 折疊動畫
    ANIMATION_FADE = "fade"    # 淡入淡出動畫
    ANIMATION_NONE = "none"    # 無動畫
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # 配置初始化
        self.data = []
        self.current_index = 0
        self.interval = 3000        # 默認間隔3秒
        self.anim_duration = 500    # 默認動畫持續500毫秒
        self.animation_type = self.ANIMATION_SLIDE  # 默認動畫類型
        
        # 保存字體和樣式設定
        self.current_font = self.font()
        self.current_alignment = Qt.AlignCenter
        self.current_stylesheet = ""
        
        # UI初始化
        self.setupUI()
        
        # 計時器初始化
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.showNextText)
        self.animation_group = None
        
        # 用於調試的標誌
        self.is_animating = False
    
    def setupUI(self):
        """初始化用戶界面"""
        self.stack_layout = QStackedLayout(self)
        self.stack_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.stack_layout)
        
        # 標籤列表
        self.labels = []
    
    def setTexts(self, texts):
        """設置要顯示的文字列表"""
        self.stop()
        
        # Reset animation state to ensure it's not stuck
        self.is_animating = False
        
        self.data = texts
        self.current_index = 0
        self.initLabels()
        
        print(f"set texts {texts}")
        
        if self.labels:
            self.stack_layout.setCurrentWidget(self.labels[0])
            # 確保第一個標籤立即可見且位置正確
            self.labels[0].move(0, 0)
            self.labels[0].show()
            self.labels[0].adjustTextDisplay()
            # 強制立即更新
            self.labels[0].update()
            self.update()
        
        # Add a debug print to verify we're deciding to start
        if len(texts) > 1:
            print(f"Starting animation for {len(texts)} texts")
            self.start()
        else:
            print("Not starting animation - only one or zero texts")
    
    def setText(self, text):
        """設置單個文字"""
        self.setTexts([text])
    
    def initLabels(self):
        """初始化標籤控件"""
        # 清除現有標籤
        while self.stack_layout.count():
            widget = self.stack_layout.widget(0)
            self.stack_layout.removeWidget(widget)
            widget.deleteLater()
        self.labels.clear()
        
        # 創建新標籤
        for text in self.data:
            label = StretchTextLabel(text)
            label.setAlignment(self.current_alignment)  # 使用已保存的對齊方式
            label.setFont(self.current_font)  # 使用已保存的字體
            if self.current_stylesheet:
                label.setStyleSheet(self.current_stylesheet)  # 使用已保存的樣式表
            
            # 確保所有標籤都具有正確的大小
            label.setGeometry(0, 0, self.width(), self.height())
            self.stack_layout.addWidget(label)
            self.labels.append(label)
        
        # 立即處理所有標籤
        for label in self.labels:
            label.adjustTextDisplay()
    
    def setFont(self, font):
        """設置所有標籤的字體"""
        self.current_font = QFont(font)  # 保存字體設定
        for label in self.labels:
            label.setFont(font)
    
    def setStyleSheet(self, style):
        """設置所有標籤的樣式表"""
        self.current_stylesheet = style  # 保存樣式表
        for label in self.labels:
            label.setStyleSheet(style)
        super().setStyleSheet(style)  # 也應用到自身
    
    def setAlignment(self, alignment):
        """設置所有標籤的對齊方式"""
        self.current_alignment = alignment  # 保存對齊方式
        for label in self.labels:
            label.setAlignment(alignment)
    
    def setInterval(self, ms):
        """設置文字更新的時間間隔（毫秒）"""
        self.interval = ms
        if self.timer.isActive():
            self.timer.start(ms)
    
    def setAnimationDuration(self, ms):
        """設置動畫持續時間（毫秒）"""
        self.anim_duration = ms
    
    def setAnimationType(self, anim_type):
        """設置動畫類型"""
        if anim_type in [self.ANIMATION_SLIDE, self.ANIMATION_FOLD, self.ANIMATION_FADE, self.ANIMATION_NONE]:
            self.animation_type = anim_type
    
    def start(self):
        """開始文字輪播"""
        if len(self.data) > 1:
            self.timer.start(self.interval)
    
    def stop(self):
        """停止文字輪播"""
        self.timer.stop()
        if self.animation_group:
            self.animation_group.stop()
            self.animation_group.deleteLater()
            self.animation_group = None
    
    def showNextText(self):
        """顯示下一個文字"""
        if len(self.labels) <= 1:
            return
            
        # 如果已經在動畫中，則不執行新的動畫
        if self.is_animating:
            return
            
        # 停止任何正在進行的動畫
        if self.animation_group:
            self.animation_group.stop()
            self.animation_group.deleteLater()
            self.animation_group = None
        
        # 設置動畫標誌
        self.is_animating = True
        
        # 獲取當前和下一個標籤
        current_label = self.labels[self.current_index]
        next_index = (self.current_index + 1) % len(self.labels)
        next_label = self.labels[next_index]
        
        # 確保標籤已正確調整
        current_label.adjustTextDisplay()
        next_label.adjustTextDisplay()
        
        try:
            # 根據動畫類型執行相應的動畫
            if self.animation_type == self.ANIMATION_SLIDE:
                self._animateSlide(current_label, next_label)
            elif self.animation_type == self.ANIMATION_FOLD:
                self._animateFold(current_label, next_label)
            elif self.animation_type == self.ANIMATION_FADE:
                self._animateFade(current_label, next_label)
            else:  # ANIMATION_NONE
                self._switchWithoutAnimation(current_label, next_label)
        except Exception as e:
            print(f"動畫錯誤: {e}")
            # 出錯時使用無動畫切換
            self._switchWithoutAnimation(current_label, next_label)
    
    def _switchWithoutAnimation(self, current_label, next_label):
        """無動畫切換標籤"""
        self.current_index = (self.current_index + 1) % len(self.labels)
        self.stack_layout.setCurrentWidget(next_label)
        self.is_animating = False
    
    def _animateSlide(self, current_label, next_label):
        """滑動動畫效果"""
        width = self.width()
        
        # 設置初始位置
        current_label.move(0, 0)
        next_label.move(width, 0)
        next_label.show()
        
        # 創建動畫
        anim_out = QPropertyAnimation(current_label, b"pos")
        anim_out.setDuration(self.anim_duration)
        anim_out.setStartValue(QPoint(0, 0))
        anim_out.setEndValue(QPoint(-width, 0))
        anim_out.setEasingCurve(QEasingCurve.InOutQuad)
        
        anim_in = QPropertyAnimation(next_label, b"pos")
        anim_in.setDuration(self.anim_duration)
        anim_in.setStartValue(QPoint(width, 0))
        anim_in.setEndValue(QPoint(0, 0))
        anim_in.setEasingCurve(QEasingCurve.InOutQuad)
        
        # 組合動畫
        self.animation_group = QParallelAnimationGroup()
        self.animation_group.addAnimation(anim_out)
        self.animation_group.addAnimation(anim_in)
        
        # 動畫完成後的處理
        def finishSlide():
            self.current_index = (self.current_index + 1) % len(self.labels)
            # 重置標籤位置
            current_label.move(0, 0)
            next_label.move(0, 0)
            self.stack_layout.setCurrentWidget(next_label)
            self.is_animating = False
        
        self.animation_group.finished.connect(finishSlide)
        self.animation_group.start()
    
    def _animateFold(self, current_label, next_label):
        """折疊動畫效果"""
        width = self.width()
        height = self.height()
        
        # 設置初始位置
        current_label.move(0, 0)
        next_label.move(0, -height)
        next_label.show()
        
        # 創建動畫
        anim_out = QPropertyAnimation(current_label, b"pos")
        anim_out.setDuration(self.anim_duration)
        anim_out.setStartValue(QPoint(0, 0))
        anim_out.setEndValue(QPoint(0, height))
        anim_out.setEasingCurve(QEasingCurve.InOutQuad)
        
        anim_in = QPropertyAnimation(next_label, b"pos")
        anim_in.setDuration(self.anim_duration)
        anim_in.setStartValue(QPoint(0, -height))
        anim_in.setEndValue(QPoint(0, 0))
        anim_in.setEasingCurve(QEasingCurve.InOutQuad)
        
        # 組合動畫
        self.animation_group = QParallelAnimationGroup()
        self.animation_group.addAnimation(anim_out)
        self.animation_group.addAnimation(anim_in)
        
        # 動畫完成後的處理
        def finishSlide():
            self.current_index = (self.current_index + 1) % len(self.labels)
            # 重置標籤位置
            current_label.move(0, 0)
            next_label.move(0, 0)
            self.stack_layout.setCurrentWidget(next_label)
            self.is_animating = False
        
        self.animation_group.finished.connect(finishSlide)
        self.animation_group.start()
    
    def _animateFade(self, current_label, next_label):
        """淡入淡出動畫效果"""
        # 設置初始位置
        current_label.setGeometry(0, 0, self.width(), self.height())
        next_label.setGeometry(0, 0, self.width(), self.height())
        
        # 創建透明度效果
        opacity_effect1 = QGraphicsOpacityEffect()
        opacity_effect2 = QGraphicsOpacityEffect()
        
        opacity_effect1.setOpacity(1.0)
        opacity_effect2.setOpacity(0.0)
        
        current_label.setGraphicsEffect(opacity_effect1)
        next_label.setGraphicsEffect(opacity_effect2)
        
        # 確保兩個標籤都可見並在前面
        current_label.show()
        next_label.show()
        current_label.raise_()
        
        # 創建動畫
        anim_out = QPropertyAnimation(opacity_effect1, b"opacity")
        anim_out.setDuration(self.anim_duration)
        anim_out.setStartValue(1.0)
        anim_out.setEndValue(0.0)
        anim_out.setEasingCurve(QEasingCurve.InOutQuad)
        
        anim_in = QPropertyAnimation(opacity_effect2, b"opacity")
        anim_in.setDuration(self.anim_duration)
        anim_in.setStartValue(0.0)
        anim_in.setEndValue(1.0)
        anim_in.setEasingCurve(QEasingCurve.InOutQuad)
        
        # 組合動畫
        self.animation_group = QParallelAnimationGroup()
        self.animation_group.addAnimation(anim_out)
        self.animation_group.addAnimation(anim_in)
        
        # 動畫完成後的處理
        def finishFade():
            self.current_index = (self.current_index + 1) % len(self.labels)
            # 清除效果並確保正確的堆疊順序
            current_label.setGraphicsEffect(None)
            next_label.setGraphicsEffect(None)
            self.stack_layout.setCurrentWidget(next_label)
            self.is_animating = False
        
        self.animation_group.finished.connect(finishFade)
        self.animation_group.start()
    
    def resizeEvent(self, event):
        """當控件大小改變時調整所有標籤"""
        super().resizeEvent(event)
        # 確保所有標籤都具有正確的大小
        for label in self.labels:
            label.setGeometry(0, 0, self.width(), self.height())
            label.adjustTextDisplay()
            
    def showEvent(self, event):
        """當控件顯示時確保標籤正確顯示"""
        super().showEvent(event)
        if self.labels and self.current_index < len(self.labels):
            # 確保當前標籤是可見的
            current_label = self.labels[self.current_index]
            current_label.move(0, 0)
            current_label.show()
            current_label.adjustTextDisplay()
            self.stack_layout.setCurrentWidget(current_label)

class VerticalText(QWidget):
    def __init__(self, text='', parent=None, font=QFont("Noto Sans JP", 40, QFont.Bold)):
        super().__init__(parent)
        self.layout = QVBoxLayout()
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)
        self.user_font = font
        self.labels = []
        self.setText(text)  # 呼叫下面的 setText

    def setText(self, text):
        # 先清掉舊的 label
        while self.layout.count():
            child = self.layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        # 逐字產生新的 label
        self.labels = []
        for char in text:
            label = QLabel(char)
            label.setFont(self.user_font)
            label.setAlignment(Qt.AlignCenter)
            label.setStyleSheet("font-size: 24px;")  # 這裡可以改字體大小
            self.labels.append(label)
            self.layout.addWidget(label)

    def setStyleSheet(self, styleSheet):
        super().setStyleSheet(styleSheet)
        for label in self.labels:
            label.setStyleSheet(styleSheet)

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

class DemoWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AnimatedTextView 示例")
        self.setGeometry(100, 100, 600, 400)
        self.setFixedWidth(600)
        
        # 創建中央窗口部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 主布局
        main_layout = QVBoxLayout(central_widget)
        
        # 創建 AnimatedTextView
        self.animated_view = AnimatedTextView_T()
        self.animated_view.setMinimumHeight(100)
        
        # 設置示例文字
        self.sample_texts = [
            "西中島南方",
            "にしなかじまみなみがた",
            "Nishinakajima-Minamigata"
        ]
        self.animated_view.setTexts(self.sample_texts)
        
        # 設置字體
        font = QFont("Noto Sans JP SemiBold", 100)
        self.animated_view.setFont(font)
        
        # 設置樣式表
        self.animated_view.setStyleSheet("background-color: #f0f0f0; color: #333; border: 2px solid #ccc; border-radius: 5px;")
        
        # 添加到主布局
        main_layout.addWidget(QLabel("AnimatedTextView 示例："))
        main_layout.addWidget(self.animated_view)
        
        # 控制面板
        control_panel = QWidget()
        control_layout = QVBoxLayout(control_panel)
        
        # 動畫類型選擇
        anim_layout = QHBoxLayout()
        anim_layout.addWidget(QLabel("動畫類型："))
        self.anim_combo = QComboBox()
        self.anim_combo.addItems(["滑動", "折疊", "淡入淡出", "無動畫"])
        self.anim_combo.currentIndexChanged.connect(self.changeAnimationType)
        anim_layout.addWidget(self.anim_combo)
        control_layout.addLayout(anim_layout)
        
        # 時間間隔設置
        interval_layout = QHBoxLayout()
        interval_layout.addWidget(QLabel("切換間隔 (毫秒)："))
        self.interval_spin = QSpinBox()
        self.interval_spin.setRange(500, 10000)
        self.interval_spin.setSingleStep(500)
        self.interval_spin.setValue(3000)
        self.interval_spin.valueChanged.connect(self.changeInterval)
        interval_layout.addWidget(self.interval_spin)
        control_layout.addLayout(interval_layout)
        
        # 動畫持續時間設置
        duration_layout = QHBoxLayout()
        duration_layout.addWidget(QLabel("動畫持續時間 (毫秒)："))
        self.duration_spin = QSpinBox()
        self.duration_spin.setRange(100, 2000)
        self.duration_spin.setSingleStep(100)
        self.duration_spin.setValue(500)
        self.duration_spin.valueChanged.connect(self.changeDuration)
        duration_layout.addWidget(self.duration_spin)
        control_layout.addLayout(duration_layout)
        
        # 控制按鈕
        button_layout = QHBoxLayout()
        
        # 開始按鈕
        self.start_button = QPushButton("開始")
        self.start_button.clicked.connect(self.animated_view.start)
        button_layout.addWidget(self.start_button)
        
        # 停止按鈕
        self.stop_button = QPushButton("停止")
        self.stop_button.clicked.connect(self.animated_view.stop)
        button_layout.addWidget(self.stop_button)
        
        control_layout.addLayout(button_layout)
        main_layout.addWidget(control_panel)
        
        # 設置初始狀態
        self.changeAnimationType(0)  # 默認為滑動動畫
    
    def changeAnimationType(self, index):
        """切換動畫類型"""
        animation_types = [
            AnimatedTextView_T.ANIMATION_SLIDE,
            AnimatedTextView_T.ANIMATION_FOLD,
            AnimatedTextView_T.ANIMATION_FADE,
            AnimatedTextView_T.ANIMATION_NONE
        ]
        if 0 <= index < len(animation_types):
            self.animated_view.setAnimationType(animation_types[index])
    
    def changeInterval(self, value):
        """更改切換間隔"""
        self.animated_view.setInterval(value)
    
    def changeDuration(self, value):
        """更改動畫持續時間"""
        self.animated_view.setAnimationDuration(value)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DemoWindow()
    window.show()
    sys.exit(app.exec_())
    
    app = QApplication(sys.argv)
    w = VerticalText("心斎橋")
    w.show()

    # 測試 2 秒後改字
    from PyQt5.QtCore import QTimer
    def change_text():
        w.setText("梅田")
    QTimer.singleShot(2000, change_text)

    sys.exit(app.exec_())
    
