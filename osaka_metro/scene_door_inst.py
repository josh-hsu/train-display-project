# scene_door_inst.py
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout

class SceneDoorInst(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        label = QLabel("This is the Station List Scene")
        label.setStyleSheet("background-color: #FF00FF; color: #000000;")
        layout.addWidget(label)
        self.setLayout(layout)