# scene_manager.py
from osaka_metro.scene_station_list import SceneStationList
from osaka_metro.scene_door_inst import SceneDoorInst
from osaka_metro.scene_station_list_en import SceneStationListEN
from osaka_metro.scene_transfer_list import SceneTransferList
from osaka_metro.scene_exit_info import GateInfoWidget

STATION_STATE_APPROACH = 0         # 車即將到達下一站
STATION_STATE_ARRIVED = 1          # 車在車站
STATION_STATE_NEXT = 2             # 車開往下一站
STATION_STATE_READY_TO_DEPART = 3  # 車準備在起站發車
STATION_STATE_IN_TERMINAL = 4      # 車在終點站

class SceneManager:
    def __init__(self):
        self.scenes = {
            "scene_station_list": SceneStationList(),
            "scene_station_list_en": SceneStationListEN(),
            "scene_transfer_list": SceneTransferList(),
            "scene_door_inst": SceneDoorInst(),
            "scene_exit_info" : GateInfoWidget(),
            "scene_exit_info_platform" : GateInfoWidget(),
        }
        self.start_index_of_state = {
            STATION_STATE_APPROACH: 4,
            STATION_STATE_ARRIVED: 4,
            STATION_STATE_NEXT: 0,
            STATION_STATE_READY_TO_DEPART: 0,
            STATION_STATE_IN_TERMINAL: 4,
        }
        self.end_index_of_state = {
            STATION_STATE_APPROACH: 5,
            STATION_STATE_ARRIVED: 5,
            STATION_STATE_NEXT: 3,
            STATION_STATE_READY_TO_DEPART: 1,
            STATION_STATE_IN_TERMINAL: 5,
        }

    def get_scene(self, name):
        return self.scenes.get(name)
    
    def notify_all_scenes(self, line_info, display_station, station_state):
        for scene in self.scenes.values():
            scene.receive_notify(line_info, display_station, station_state)