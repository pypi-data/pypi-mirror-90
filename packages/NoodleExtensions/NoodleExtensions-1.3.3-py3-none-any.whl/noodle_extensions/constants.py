from enum import Enum

class Animations:
    position         = "_position"
    rotation         = "_rotation"
    localRotation    = "_localRotation"
    scale            = "_scale"
    dissolveCube     = "_dissolve"
    dissolveArrow    = "_dissolveArrow"
    time             = "_time"
    color            = "_color"

class EventType:
    AnimateTrack        = "AnimateTrack"
    AssignPathAnimation = "AssignPathAnimation"
    AssignTrackParent   = "AssignTrackParent"
    AssignPlayerToTrack = "AssignPlayerToTrack"