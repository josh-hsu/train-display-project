from PyQt5.QtCore import QObject, pyqtSignal, QThread, QTimer
import time

class RouteDirector(QObject):
    station_changed = pyqtSignal(object)   # 發送目前站 StationInfo
    arrived_terminal = pyqtSignal()        # 抵達終點

    def __init__(self, route: list, interval_sec=3):
        super().__init__()
        self.route = route  # List[StationInfo]
        self.interval = interval_sec
        self._running = False

        self.thread = QThread()
        self.moveToThread(self.thread)
        self.thread.started.connect(self._run)

    def start(self):
        if not self._running:
            self._running = True
            self.thread.start()

    def stop(self):
        self._running = False
        self.thread.quit()
        self.thread.wait()

    def _run(self):
        for station in self.route:
            if not self._running:
                break
            self.station_changed.emit(station)  # 通知 UI 換站
            time.sleep(self.interval)

        if self._running:
            self.arrived_terminal.emit()
        self._running = False

# Usage
#self.director = RouteDirector(route)
#self.director.station_changed.connect(self.update_ui_for_station)
#self.director.arrived_terminal.connect(self.show_terminal_notice)
#self.director.start()
