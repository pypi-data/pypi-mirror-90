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
