# G4S_Alarm_Py
Python API wrapper for G4S alarm api

Partial implemation

This will probably only work with Danish systems, and i honestly don't even know whether G4S provides alarm systems other places. But the endpoints are on a .dk tld so i'm assuming that other locales will have their own endpoints

Still missing:
* Daytime arming of alarm
* Other G4S devices (smokecannons etc.)
* Tests

Potential issues:
* Even though datetimes are formatted with the Z suffix by the API the time seems to be in the users local timezone rather than UTC

Heavily inspired by the TS implementation by [hyber1z0r](https://github.com/hyber1z0r/g4s/blob/master/src/types/SystemState.ts)
