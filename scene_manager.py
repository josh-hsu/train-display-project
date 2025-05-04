# scene_manager.py
from osaka_metro.scene_station_list import SceneStationList
from osaka_metro.scene_door_inst import SceneDoorInst
from osaka_metro.scene_station_list_en import SceneStationListEN

class SceneManager:
    def __init__(self):
        self.scenes = {
            "scene_station_list": SceneStationList(),
            "scene_station_list_en": SceneStationListEN(),
            #"scene_door_inst": SceneStationList(),
        }

    def get_scene(self, name):
        return self.scenes.get(name)
    
    def notify_all_scenes(self, line_info, display_station, station_state):
        for scene in self.scenes.values():
            scene.receive_notify(line_info, display_station, station_state)