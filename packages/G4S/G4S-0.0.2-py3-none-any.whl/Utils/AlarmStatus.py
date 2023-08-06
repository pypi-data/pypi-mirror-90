from Utils.PanelState import PanelState
from Utils.StateDevice import StateDevice
from Utils.User import User


class AlarmStatus(object):
    def __init__(self, inputDict, api):
        self.PanelId = inputDict["panelInfo"]["PanelId"]
        self.Name = inputDict["panelInfo"]["Name"]
        self.PanelState = PanelState(inputDict["panelState"])
        self.StateDevices = [StateDevice(device) for device in inputDict["stateDevices"]]
        self.SystemState = PanelState(inputDict["systemState"])
        self.Users = [User(user, api) for user in inputDict["users"]]