import requests
from datetime import timedelta


class API(object):
    def __init__(self, username, password):
        self.Username = username
        self.Password = password
        self.BaseUrl = "https://mit.g4severhome.dk/ESI.API/API"
        self.StatusUrlPart = "systemstatus/getState"
        self.CommandUrlPart = "Commands/invokeAPI"
        self.PanelId = None

    def GetState(self):
        url = f"{self.BaseUrl}/{self.StatusUrlPart}"
        body = {"username": self.Username, "password": self.Password}
        if self.PanelId is not None:
            body["panelId"] = panel_id
        r = requests.post(url, json=body)
        r.raise_for_status()

        return_value = r.json()
        if self.PanelId is None:
            self.PanelId = return_value["panelInfo"]["PanelId"]
        return return_value

    def ArmAlarm(self):
        url = f"{self.BaseUrl}/{self.CommandUrlPart}"
        body = {"email": self.Username, "password": self.Password, "methodToInvoke": "Arm", "panelId": self.PanelId}
        r = requests.post(url, json=body)
        return r.json()

    def NightArmAlarm(self):
        url = f"{self.BaseUrl}/{self.CommandUrlPart}"
        body = {
            "email": self.Username,
            "password": self.Password,
            "methodToInvoke": "Arm",
            "partition": 2,
            "panelId": self.PanelId,
        }
        r = requests.post(url, json=body)
        return r.json()

    def DisarmAlarm(self):
        url = f"{self.BaseUrl}/{self.CommandUrlPart}"
        body = {"email": self.Username, "password": self.Password, "methodToInvoke": "Disarm", "panelId": self.PanelId}
        r = requests.post(url, json=body)
        return r.json()

    def ChangeUserPanelPin(self, user_id, access_code):
        url = f"{self.BaseUrl}/users/SetTr5AccessCode"
        body = {
            "panelId": self.PanelId,
            "userName": self.Username,
            "password": self.Password,
            "accessCode": access_code,
            "userId": user_id,
        }
        r.raise_for_status()
        return r.json()

    def GetEvents(self, event_type_list=None, count=100, date=None):
        url = f"{self.BaseUrl}/Events/InvokeApi"
        body = {
            "email": self.Username,
            "password": self.Password,
            "methodToInvoke": "GetEventsHistory",
            "panelId": self.PanelId,
            "eventTypeList": "314,56,57,51,58,59,1,2,5,153,155,3,156,8,9,1010,39,40,203,211,212,215,216,222,223,411,412,506,510,511,513,514,515,516,904,906,907,909,910,912,913,915,916,918,919,921,104,106,105,101,103,102,150,152,151,204,1201,1207,1253,706,705,220,221,107,109,112,113,114,418,1258,1259,1260,1875,1876,1205,1208,1602,1601,1604,1610,1611,1640,1641,1612,1613,1614,1615,1616,927,928,930,931,933,901,903,108,810,811,812,813,814,927,815,1617,1618,1810,1811,1891,1892,1893,1894,1895,1896,30,1812,1879,1883,1884,1899,1900,1901,1902,1903",
            "numberOfEvents": count,
        }
        if event_type_list is not None:
            body["eventTypeList"] = ",".join(event_type_list)

        if date is not None:
            body["fromDate"] = date.strftime("%Y-%m-%d")
            body["toDate"] = (date + timedelta(days=1)).strftime("%Y-%m-%d")
        r = requests.post(url, json=body)
        r.raise_for_status()
        return r.json()
