from enum import Enum


class ArmType(Enum):
    FULL_ARM = 0
    NIGHT_ARM = 1
    UNKNOWN = 2
    DISARMED = 3


class DeviceType(Enum):
    Unknown = -1
    Hub = 1
    DoorWindowSensor = 2
    Panel = 14
    Smokealarm = 16
    Siren = 24
    Camera = 38
    AccessChip = 201

    @classmethod
    def _missing_(cls, value):
        return DeviceType.Unknown


class EventType(Enum):
    Unknown = -1
    Arm = 39
    Disarm = 40
    NightArm = 57

    @classmethod
    def _missing_(cls, value):
        return EventType.Unknown