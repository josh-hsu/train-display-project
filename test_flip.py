from line_info import *
from osaka_metro_main import *

class TestFlip:
    def __init__(self):
        self.stations = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]  # 假設的車站列表

    def initLineInfo(self, line_file=MIDOSUJI_LINE_INFO):
        self.line_info = LineInfo(line_file)
        self.line_info.set_route(3) # select route 1
        self.route = self.line_info.get_current_route()
        print(f"Route: {self.route}")

    def get_train_state_in_route(self, line_info, route, elapsedTimeSec, stayInStationSec=30, approachingSec=50):
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


if __name__ == "__main__":
    test = TestFlip()
    elapsed_time = 150  # 秒
    test.initLineInfo()
    station, state = test.get_train_state_in_route(test.line_info, test.line_info.get_current_route(), elapsed_time)
    print(station, state)  # e.g. M15 approaching