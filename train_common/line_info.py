import yaml, re
from osaka_metro.osaka_metro import LINE_COLOR_MAP

STATION_STATE_APPROACH = 0         # 車即將到達下一站
STATION_STATE_ARRIVED = 1          # 車在車站
STATION_STATE_NEXT = 2             # 車開往下一站
STATION_STATE_READY_TO_DEPART = 3  # 車準備在起站發車
STATION_STATE_IN_TERMINAL = 4      # 車在終點站

DEPART_READY_TIME_SEC = 30

def extract_first_integer(s):
    match = re.search(r'\d+', s)
    return int(match.group()) if match else None

def index_to_station_id(prefix: str, index: int) -> str:
    return f"{prefix}{index}"

def get_station_prefix_number(s: str) -> tuple[str, int]:
    """
    將輸入的字串分割為字母與數字部分。
    
    參數:
        s (str): 輸入字串，例如 "T20", "C02", "U2"
    
    回傳:
        tuple[str, int]: 字母（字串）與數字（整數）
    """
    if not s or len(s) < 2:
        raise ValueError("輸入格式錯誤，至少需要一個字母與一個數字")

    letter = s[0]
    number = int(s[1:])

    return letter, number

def format_train_progress_station_name(name: str):
    """
    Format Japanese station names according to specific rules:
    - If name has 1 character or 4+ characters: return as is
    - If name has 3 characters: add "　" at the beginning
    - If name has 2 characters: add "　" at beginning and between characters
    
    Examples:
    - "心齋橋" (3 chars) -> "一心齋橋"
    - "本町" (2 chars) -> "一本一町"
    - "中" (1 char) -> "中"
    - "西中島南方" (5 chars) -> "西中島南方"
    """
    if len(name) == 1 or len(name) >= 4:
        return name
    elif len(name) == 3:
        return "　" + name
    elif len(name) == 2:
        return "　" + name[0] + "　" + name[1]
    return name

class TransferEntry:
    def __init__(self, name, code=None, direction=None):
        self.name = name
        self.code = code
        self.direction = direction

    def to_dict(self):
        return {
            "name": self.name,
            "code": self.code,
            "direction": self.direction
        }

    def __repr__(self):
        return f"TransferEntry(name={self.name!r}, code={self.code!r}, direction={self.direction!r})"


class TransferInfo:
    def __init__(self, transfer_list=None):
        self.entries = []
        if transfer_list:
            self.set_data(transfer_list)

    def set_data(self, transfer_list):
        self.entries = [
            TransferEntry(*entry) for entry in transfer_list
        ]

    def get_station_list(self):
        return [entry.name for entry in self.entries]

    def get_code_list(self):
        return [entry.code for entry in self.entries]

    def get_direction_list(self):
        return [entry.direction for entry in self.entries]

    def to_list(self):
        return [entry.to_dict() for entry in self.entries]

    def __len__(self):
        return len(self.entries)

    def __getitem__(self, index):
        return self.entries[index]

    def __repr__(self):
        return f"TransferInfo({self.entries})"

class StationInfo:
    def __init__(self, data: dict):
        self.id = data.get("id")
        self.line = data.get("line")
        self.name = data.get("name", {})  # jp, jp-hinagana, en, zh-TW
        self.transfer = TransferInfo(data.get("transfer", []))
        self.gate_info = data.get("gate_info", {})
        self.gate_info_detail = data.get("gate_info_detail", {})
        self.previous_station = data.get("previous_station", [])
        self.next_station = data.get("next_station", [])
        self.door_open = data.get("door_open")

    def __repr__(self):
        return f"<StationInfo {self.id}: {self.name.get('en', '')}>"

class LineInfo:
    def __init__(self, yaml_path: str):
        with open(yaml_path, "r", encoding="utf-8") as f:
            self.raw = yaml.safe_load(f)

        line_data = self.raw.get("line", {})
        self.id = line_data.get("id")
        self.id_prefix = line_data.get("id_prefix")
        self.lang = line_data.get("lang", [])
        self.name = line_data.get("name", {})
        self.operator = line_data.get("operator")
        self.directions = line_data.get("directions", [])
        self.route = 0
        self.main_color = LINE_COLOR_MAP[self.id]

        self.stations = []
        self.station_map = {}

        for station_data in line_data.get("stations", []):
            station = StationInfo(station_data)
            self.stations.append(station)
            self.station_map[station.id] = station
        
        print(f"route: {self.directions}, num: {len(self.directions)}")

    def get_station(self, station_id: str) -> StationInfo:
        return self.station_map.get(station_id)

    def get_all_stations(self):
        return self.stations
    
    def get_route(self, route):
        return self.directions[route] if route < len(self.directions) else None
    
    def get_current_route(self):
        return self.directions[self.route] if self.route < len(self.directions) else None
    
    def set_route(self, direction_index):
        self.route = direction_index