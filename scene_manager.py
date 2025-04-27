# scene_manager.py
from osaka_metro.scene_station_list import SceneStationList
from osaka_metro.scene_door_inst import SceneDoorInst

class SceneManager:
    def __init__(self):
        self.scenes = {
            "scene_station_list": SceneStationList(),
            "scene_door_inst": SceneStationList(),
        }

    def get_scene(self, name):
        return self.scenes.get(name)