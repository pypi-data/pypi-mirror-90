from Utils.Enums import ArmType
from Utils.StaticUtils import StaticUtils


class PanelState(object):
    def __init__(self, inputDict: dict):
        self.ArmType = ArmType(inputDict["ArmType"])
        self.ArmTypeChangedTime = StaticUtils.ParseDate(inputDict["ArmTypeChangedTime"])
        self.ArmForcedState = inputDict["ArmForcedState"]
        self.ArmDelayedState = inputDict["ArmDelayedState"]
        self.AlarmState = inputDict["AlarmState"]
        self.AlarmStateTime = StaticUtils.ParseDate(inputDict["AlarmStateTime"])
        self.Partition = inputDict["Partition"]
        self.DeviceName = inputDict["DeviceName"]
        self.ExitDelayArmInProcess = inputDict["ExitDelayArmInProcess"]
        self.EntryDelayArmInProcess = inputDict["EntryDelayArmInProcess"]
        self.ReceptionLevel = inputDict.get("ReceptionLevel")
        self.ReceptionLevelChangedTime = StaticUtils.ParseDate(inputDict.get("ReceptionLevelChangedTime"))
        self.PanelBatteryLevel = inputDict.get("PanelBatteryLevel")
        self.IsPanelOffline = inputDict.get("IsPanelOffline")
        self.IsPanelOfflineChangedTime = StaticUtils.ParseDate(inputDict.get("IsPanelOfflineChangedTime"))
        self.IsZWaveEnabled = inputDict["IsZWaveEnabled"]
        self.IsZWaveEnabledChangedTime = StaticUtils.ParseDate(inputDict["IsZWaveEnabledChangedTime"])
        self.IsMainPowerConnected = inputDict["IsMainPowerConnected"]
        self.IsMainPowerConnectedChangedTime = StaticUtils.ParseDate(inputDict["IsMainPowerConnectedChangedTime"])
        self.IsSimCardReady = inputDict["IsSimCardReady"]
        self.CommunicationLink = inputDict["CommunicationLink"]
        self.BackupChannelStatus = inputDict["BackupChannelStatus"]
        self.BackupChannelStatusDescription = inputDict["BackupChannelStatusDescription"]
        self.HasLowBattery = inputDict["HasLowBattery"]
        self.HasLowBatteryChangedTime = StaticUtils.ParseDate(inputDict["HasLowBatteryChangedTime"])
        self.SetupMode = inputDict["SetupMode"]
        self.SirensVolumeLevel = inputDict["SirensVolumeLevel"]
        self.SirensDuration = inputDict["SirensDuration"]
        self.SirensVolumeLevelDurationChangedTime = StaticUtils.ParseDate(
            inputDict["SirensVolumeLevelDurationChangedTime"]
        )
        self.IsInInstallationMode = inputDict["IsInInstallationMode"]
        self.IsInInstallationModeChangedTime = StaticUtils.ParseDate(inputDict["IsInInstallationModeChangedTime"])
        self.IsInSignalStrengthTest = inputDict["IsInSignalStrengthTest"]
        self.IsInSignalStrengthTestChangedTime = StaticUtils.ParseDate(inputDict["IsInSignalStrengthTestChangedTime"])
        self.PanelId = inputDict["PanelId"]
        self.IsSynchronized = inputDict["IsSynchronized"]
        self.SirensEntryExitDuration = inputDict["SirensEntryExitDuration"]
        self.FrtState = inputDict["FrtState"]
        self.FrtStateChangedTime = StaticUtils.ParseDate(inputDict["FrtStateChangedTime"])


if __name__ == "__main__":
    test_data = {
        "ArmType": 3,
        "ArmTypeChangedTime": "2021-01-03T07:57:25Z",
        "ArmForcedState": 0,
        "ArmDelayedState": 0,
        "AlarmState": 0,
        "AlarmStateTime": None,
        "Partition": -1,
        "DeviceName": None,
        "ExitDelayArmInProcess": False,
        "EntryDelayArmInProcess": False,
        "ReceptionLevel": 3,
        "ReceptionLevelChangedTime": "2021-01-04T11:01:23Z",
        "PanelBatteryLevel": 4,
        "IsPanelOffline": False,
        "IsPanelOfflineChangedTime": "2021-01-04T11:17:37Z",
        "IsZWaveEnabled": True,
        "IsZWaveEnabledChangedTime": "2020-12-01T15:40:38Z",
        "IsMainPowerConnected": True,
        "IsMainPowerConnectedChangedTime": "2021-01-01T06:51:17Z",
        "IsSimCardReady": True,
        "CommunicationLink": 1,
        "BackupChannelStatus": 1,
        "BackupChannelStatusDescription": 0,
        "HasLowBattery": False,
        "HasLowBatteryChangedTime": "2020-12-01T16:55:16Z",
        "SetupMode": False,
        "SirensVolumeLevel": 3,
        "SirensDuration": 90,
        "SirensVolumeLevelDurationChangedTime": "2020-12-01T15:37:11Z",
        "IsInInstallationMode": False,
        "IsInInstallationModeChangedTime": None,
        "IsInSignalStrengthTest": False,
        "IsInSignalStrengthTestChangedTime": None,
        "PanelId": 10039947,
        "IsSynchronized": True,
        "SirensEntryExitDuration": 30,
        "FrtState": 0,
        "FrtStateChangedTime": None,
    }
    test = PanelState(test_data)
    print(test)