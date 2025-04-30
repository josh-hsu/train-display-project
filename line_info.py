import yaml

class StationInfo:
    def __init__(self, data: dict):
        self.id = data.get("id")
        self.line = data.get("line")
        self.name = data.get("name", {})  # jp, jp-hinagana, en, zh-TW
        self.transfer = data.get("transfer", [])
        self.gate_info = data.get("gate_info", {})
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
        self.lang = line_data.get("lang", [])
        self.name = line_data.get("name", {})
        self.operator = line_data.get("operator")
        self.directions = line_data.get("directions", [])

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
    
    def get_routes(self, route):
        pass