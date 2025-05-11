from PyQt5.QtCore import QObject, pyqtSignal, QThread, QTimer
import time
from line_info import *

###
### RouteDirector
### input: 
###
class RouteDirector(QObject):
    report = pyqtSignal(object)   # 發送目前站 StationInfo

    def __init__(self, line_info, route, interval_sec=10, interval_inc=10, init_elapsed_time=0):
        super().__init__()
        self.line_info = line_info     # line_info: LineInfo
        self.route = route             # [M13, M25]
        self.interval = interval_sec
        self.increment = interval_inc
        self._running = False
        self.elapsed_time = init_elapsed_time

        self.thread = QThread()
        self.moveToThread(self.thread)
        self.thread.started.connect(self._run)

    def __del__(self):
        """
        解構子：確保對象被銷毀時正確關閉執行緒
        """
        # 確保執行緒正確停止
        if hasattr(self, '_running') and self._running:
            self._running = False
            
        # 確保執行緒已退出
        if hasattr(self, 'thread') and self.thread.isRunning():
            self.thread.quit()
            # 給執行緒一些時間來退出
            if not self.thread.wait(1000):  # 等待最多1000毫秒
                # 如果執行緒沒有在指定時間內退出，則強制終止
                self.thread.terminate()
                self.thread.wait()  # 等待執行緒真正結束
                
        # 確保斷開所有信號連接
        try:
            if hasattr(self, 'thread') and self.thread.started:
                self.thread.started.disconnect()
        except Exception:
            # 如果信號已經斷開連接，可能會引發異常，我們可以安全地忽略它
            pass
                
        print("RouteDirector 已正確清理並銷毀")


    def start(self):
        if not self._running:
            self._running = True
            self.thread.start()

    def stop(self):
        self._running = False
        self.thread.quit()
        self.thread.wait()

    def reset(self):
        self.elapsed_time = 0
    
    def get_time_elapsed(self):
        return self.elapsed_time

    def get_train_state_in_route(self, line_info, route, elapsedTimeSec, stayInStationSec=30, approachingSec=40):
        """
        Calculate the current train state and station based on elapsed time.
        
        Args:
            line_info: Information about the train line and stations
            route: List containing start and end station IDs, e.g. ["M13", "M25"]
            elapsedTimeSec: Seconds elapsed since the start of the journey
            stayInStationSec: Time in seconds that train stays at each station (default 30)
            approachingSec: Seconds before arrival when state changes to "approaching" (default 50)
        
        Returns:
            tuple: (station_id, state) where state is one of "approaching", "arrived", "to_next"
        """
        if not route or len(route) != 2:
            raise ValueError("Route must contain exactly two stations: start and end")
        
        start_station = route[0]
        end_station = route[1]
        
        # Parse station IDs to generate full path
        # Assuming format like "M13" where "M" is the line prefix and "13" is the station number
        try:
            # Extract prefix and numbers
            start_prefix = ''.join(filter(str.isalpha, start_station))
            end_prefix = ''.join(filter(str.isalpha, end_station))
            start_num = int(''.join(filter(str.isdigit, start_station)))
            end_num = int(''.join(filter(str.isdigit, end_station)))
            
            # Check if same line
            if start_prefix != end_prefix:
                raise ValueError(f"Start station {start_station} and end station {end_station} are not on the same line")
            
            # Generate path based on numbers
            if start_num <= end_num:
                full_path = [f"{start_prefix}{i}" for i in range(start_num, end_num + 1)]
            else:
                full_path = [f"{start_prefix}{i}" for i in range(start_num, end_num - 1, -1)]
        except ValueError as e:
            # If there's any issue with parsing, raise an error
            raise ValueError(f"Could not parse station IDs: {e}")
        
        # Initialize time tracking
        current_time = 0
        
        # First station handling
        if elapsedTimeSec < stayInStationSec:
            return full_path[0], STATION_STATE_READY_TO_DEPART
        
        current_time += stayInStationSec
        
        # Track progress through stations
        for i in range(len(full_path) - 1):
            from_station = full_path[i]
            to_station = full_path[i + 1]
            
            # Get travel time between these stations
            travel_time = line_info.get_station(from_station).next_station[2]  # Time in seconds to next station
            
            # Calculate state transition times
            to_next_end_time = current_time + (travel_time - approachingSec)
            approaching_end_time = to_next_end_time + approachingSec
            arrived_end_time = approaching_end_time + stayInStationSec
            
            # Determine current state
            if elapsedTimeSec < to_next_end_time:
                return to_station, STATION_STATE_NEXT  # Changed to return the next station for to_next state
            elif elapsedTimeSec < approaching_end_time:
                return to_station, STATION_STATE_APPROACH
            elif elapsedTimeSec < arrived_end_time:
                return to_station, STATION_STATE_ARRIVED
            
            # Move time forward to account for this segment
            current_time = arrived_end_time
        
        # If we've gone through all stations and all time segments
        return end_station, STATION_STATE_IN_TERMINAL

    def _run(self):
        time.sleep(self.interval)
        state = STATION_STATE_READY_TO_DEPART
        while state != STATION_STATE_IN_TERMINAL:
            if not self._running:
                break
            self.elapsed_time += self.increment
            station, state = self.get_train_state_in_route(self.line_info, self.route, self.elapsed_time)
            self.report.emit([station, state, self.elapsed_time])  # 通知 UI 換站
            time.sleep(self.interval)
        self._running = False

# Usage
#self.director = RouteDirector(route)
#self.director.station_changed.connect(self.update_ui_for_station)
#self.director.arrived_terminal.connect(self.show_terminal_notice)
#self.director.start()
