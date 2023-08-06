import json

from Utils.API import API
from Utils.AlarmStatus import AlarmStatus
from Utils.StaticUtils import StaticUtils as Utils


class Alarm(object):
    def __init__(self, username, password):
        self.Username = username
        self.Password = password
        self.API = API(self.Username, self.Password)
        self.Status = None
        self.Users = None
        self.State = None
        self.LastStateChange = None
        self.LastStateChangeBy = None
        self.Sensors = None
        self.UpdateStatus()

    def UpdateStatus(self):
        self.Status = AlarmStatus(self.API.GetState(), self.API)
        self.Users = self.Status.Users
        self.State = self.Status.SystemState.ArmType
        self.Sensors = self.Status.StateDevices
        self.LastStateChange = self.Status.SystemState.ArmTypeChangedTime
        events = json.loads(self.API.GetEvents(date=self.LastStateChange)["Events"])
        matching_events = [
            x
            for x in events
            if Utils.ParseDate(x["Events"][0]["Header"]["LocalTime"].replace('"', "")) == self.LastStateChange
        ]
        if len(matching_events) > 0:
            user_id = matching_events[0]["Events"][0]["UserId"]
            self.LastStateChangeBy = [x for x in self.Users if x.Id == user_id][0]

    def Arm(self):
        self.API.ArmAlarm()
        self.UpdateStatus()

    def NightArm(self):
        self.API.NightArmAlarm()
        self.UpdateStatus()

    def Disarm(self):
        self.API.DisarmAlarm()
        self.UpdateStatus()