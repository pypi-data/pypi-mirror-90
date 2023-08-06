# PPPPPPPPPPPPPPPPP   NNNNNNNN        NNNNNNNNEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE
# P::::::::::::::::P  N:::::::N       N::::::NE::::::::::::::::::::EE::::::::::::::::::::E
# P::::::PPPPPP:::::P N::::::::N      N::::::NE::::::::::::::::::::EE::::::::::::::::::::E
# PP:::::P     P:::::PN:::::::::N     N::::::NEE::::::EEEEEEEEE::::EEE::::::EEEEEEEEE::::E
#   P::::P     P:::::PN::::::::::N    N::::::N  E:::::E       EEEEEE  E:::::E       EEEEEE
#   P::::P     P:::::PN:::::::::::N   N::::::N  E:::::E               E:::::E
#   P::::PPPPPP:::::P N:::::::N::::N  N::::::N  E::::::EEEEEEEEEE     E::::::EEEEEEEEEE
#   P:::::::::::::PP  N::::::N N::::N N::::::N  E:::::::::::::::E     E:::::::::::::::E
#   P::::PPPPPPPPP    N::::::N  N::::N:::::::N  E:::::::::::::::E     E:::::::::::::::E
#   P::::P            N::::::N   N:::::::::::N  E::::::EEEEEEEEEE     E::::::EEEEEEEEEE
#   P::::P            N::::::N    N::::::::::N  E:::::E               E:::::E
#   P::::P            N::::::N     N:::::::::N  E:::::E       EEEEEE  E:::::E       EEEEEE
# PP::::::PP          N::::::N      N::::::::NEE::::::EEEEEEEE:::::EEE::::::EEEEEEEE:::::E
# P::::::::P          N::::::N       N:::::::NE::::::::::::::::::::EE::::::::::::::::::::E
# P::::::::P          N::::::N        N::::::NE::::::::::::::::::::EE::::::::::::::::::::E
# PPPPPPPPPP          NNNNNNNN         NNNNNNNEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE
#
# Python Noodle Extensions Editor. (Great name, I know.) I can't do ASCII, so I used http://patorjk.com/software/taag/#p=testall&h=0&v=0&f=Alpha&t=PNEE "Doh" (Pronounced the same as Knee, /nē/)
# This code is awful. Please improve it.

import json, os
from pathlib import Path
from enum import Enum
from . import constants, exceptions


PATHSWINDOWS = { # A list of internal Beat Saber download paths.
    "Steam":r"C:\Program Files (x86)\Steam\steamapps\common\Beat Saber",
    "Oculus":r"C:\OculusApps\Software\hyperbolic-magnematism-beat-saber"
}
PATHSLINUX = {
    "Steam":r"~/.steam/steam/SteamApps/common/Beat Saber",
    "Oculus":r"unknown" # I need someone to add an oculus download path (if exists) for Linux
}
EASINGSNET = "https://easings.net"
ANIMATORTYPES = [
    "_position",
    "_rotation",
    "_localRotation",
    "_scale",
    "_dissolve",
    "_dissolveArrow",
    "_time",
    "_color"
]
ANIMATORFORMATS = {
     "_position":       '[left/right, up/down, forw/backw, time (beat), "easing"]',
     "_rotation":       '[pitch, yaw, roll, time (beat), "easing"]',
"_localRotation":       '[pitch, yaw, roll, time (beat), "easing"]',
        "_scale":       '[left/right, up/down, forw/backw, time (beat), "easing"]',
     "_dissolve":       '[amount, time (beat), "easing"]',
"_dissolveArrow":       '[amount, time (beat), "easing"]',
         "_time":       '[lifespan, time (beat), "easing"]',
        "_color":       '[red, green, blue, time, easing]'
}
EVENTTYPES = [
    "AnimateTrack",
    "AssignPathAnimation"
]
EVENTTYPESTRACK = [
    "AssignTrackParent",
    "AssignPlayerToTrack"
]
EASINGS = [
    "easeInsine",
    "easeOutSine",
    "easeInOutSine",
    "easeInCubic",
    "easeOutCubic",
    "easeInOutCubic",
    "easeInQuint",
    "easeOutQuint",
    "easeInOutQuint",
    "easeInCirc",
    "easeOutCirc",
    "easeInOutCirc",
    "easeInElastic",
    "easeOutElastic",
    "easeInOutElastic",
    "easeInQuad",
    "easeOutQuad",
    "easeInOutQuad",
    "easeInQuart",
    "easeOutQuart",
    "easeInOutQuart",
    "easeInExpo",
    "easeOutExpo",
    "easeInOutExpo",
    "easeInBack",
    "easeOutBack",
    "easeInOutBack",
    "easeInBounce",
    "easeOutBounce",
    "easeInOutBounce"
]


class Editor:

    def updateDependencies(self, dependency:str) -> list:
        '''Update Dependencies adds a `_requirements` item. Do note it doesn't check if you have it installed nor does it check whether or not that dependency is real.\n
        However, it does check whether or not it's already in the list.\n
        Returns the list of dependencies.
        - `dependency` the string item you want to add to the `_requirements`
        '''
        infodatpath = self.customLevelPath
        infodatpath = infodatpath.split("\\")
        infodatpath.remove(infodatpath[len(infodatpath)-1])
        infodatpath.append("info.dat")
        infodatpath = "\\".join(infodatpath)

        with open(infodatpath, 'r') as getinfodat:
            infodat = json.load(getinfodat)
        with open(infodatpath, 'w') as editinfodat:
            for x in range(len(infodat["_difficultyBeatmapSets"])):
                # warning: the next few lines are ugly.
                for _difficultyBeatmaps in infodat["_difficultyBeatmapSets"][x]["_difficultyBeatmaps"]:
                    if _difficultyBeatmaps["_beatmapFilename"] == self.customLevelPath.split("\\")[len(self.customLevelPath.split("\\"))-1]: # if the difficulty is the same file as the one the user is using
                        if _difficultyBeatmaps["_customData"].get("_requirements") is None:
                            _difficultyBeatmaps["_customData"]["_requirements"] = []
                        if not dependency in _difficultyBeatmaps["_customData"]["_requirements"]:
                            _difficultyBeatmaps["_customData"]["_requirements"].append(dependency)
                        json.dump(infodat, editinfodat)
                        return _difficultyBeatmaps["_customData"]["_requirements"]

    def __init__(self, customLevelPath:str):
        '''The base editor for editing. This will not be animating.
        - `customLevelPath` The path where the `level.dat` is. (include `.dat`)
        '''
        if not os.path.exists(customLevelPath):
            raise FileNotFoundError("This level.dat file does not exist.")
        elif not customLevelPath.endswith(".dat"):
            raise FileNotFoundError("Please include the .dat / make sure you include the level.dat at the end of the directory")
        self.customLevelPath = customLevelPath

        # Edit info.dat to have noodle_extensions as a req
        self.updateDependencies("Noodle Extensions")

    def editBlock(self, beat:int, pos:tuple, track:str=None, fake:bool=False, interactable:bool=True) -> dict:
        '''Edits a specific block/note (same thing) Returns the note's data
        - `beat` The beat at which the block can be found.
        - `pos` The position of the block (tuple). (0, 0) is found left-most row, bottom layer.

        ### To edit the block
        - `track` add / change the track of a block. (ignore this to remove the track.)
        - `false` whether or not the block will affect the player's score.
        - `interactable` whether or not the saber can go through the block.

        Do note that if `interactable` is set to False, `false` will also be set to False.
        You don't want a block that will kill the player that cannot be hit.
        '''
        with open(self.customLevelPath, 'r') as editnote:
            notes = json.load(editnote)
        with open(self.customLevelPath, 'w') as editnote_:
            for note in notes["_notes"]:
                if note["_time"] == beat and note["_lineIndex"] == pos[0] and note["_lineLayer"] == pos[1]:
                    fake = False if not interactable else False if not fake else True # "Do note that if `interactable` is set to False, `false` will also be set to False. You don't want a block that will kill the player that cannot be hit."
                    if track is None:
                        note["_customData"] = {
                            "_fake" : fake,
                            "_interactable" : interactable
                        }
                    else:
                        note["_customData"] = {
                            "_fake" : fake,
                            "_interactable" : interactable,
                            "_track" : track
                        }
                    json.dump(notes, editnote_)
                    return note
            json.dump(notes, editnote_)

    def editWall(self, beat:int, length:int, index:int, track:str=None, fake:bool=False, interactable:bool=True) -> dict:
        '''The exact same as EditNote except it's EditWall (edits a wall.) Returns the wall's data
        - `beat` The beat at which it starts
        - `length` The beat at which it ends
        - `index` The row on which it's on (0 is left-most)

        - `track` The track to assign to the wall. Leave empty to remove it
        - `false` whether or not the Wall will damage the player.
        - `interactable` whether or not the wall will vibrate the controllers.
        '''
        with open(self.customLevelPath, 'r') as getWalls:
            walls = json.load(getWalls)
        with open(self.customLevelPath, 'w') as EditWalls:
            for obst in walls["_obstacles"]:
                if obst["_time"] == beat and obst["_duration"] == length-beat and obst["_lineIndex"] == index: # if we're talking about the same wall
                    if track is not None:
                        obst["_customData"] = {
                            "_track" : track,
                            "_fake" : fake,
                            "_interactable" : interactable
                        }
                    else:
                        obst["_customData"] = {
                            "_fake" : fake,
                            "_interactable" : interactable
                        }
                    json.dump(walls, EditWalls)
                    return obst
            json.dump(walls, EditWalls)
    def getBlock(self, beat:int, pos:tuple) -> dict:
        '''Returns a note's data
        - `beat` the beat at which the note can be found
        - `pos` The position of the block (tuple). (0, 0) is found left-most row, bottom layer.
        '''
        with open(self.customLevelPath, 'r') as getNote:
            notes = json.load(getNote)
        
        for x in notes["_notes"]:
            if x["_time"] == beat and x["_lineIndex"] == pos[0] and x["_lineLayer"] == pos[1]:
                return x
        raise exceptions.NoteNotFoundError("Could not find note")
    def getWall(self, beat:int, index:int, length:int) -> dict:
        '''Returns a wall's data.
        - `beat` the beat at which the wall starts.
        - `index` the row on which the left side of the wall is (0 is left-most)
        - `length` how long the wall lasts (in beats)
        '''
        with open(self.customLevelPath, 'r') as getNote:
            notes = json.load(getNote)
        
        for x in notes["_obstacles"]:
            if x["_time"] == beat and x["_lineIndex"] == index and x["_duration"] == length:
                return x
        raise exceptions.WallNotFoundError("Could not find wall.")
    def removeEvent(self, time:int, eventType:str, track:str, animationType:str=None) -> dict:
        '''Removes an event from the `_customEvents` list. (Returns the removed event's data)\n
        If there is more than just the `animationType` provided in the event, it will only remove the `animationType` property of the animation.\n
        Otherwise, it will remove the entire event.
        - `time` the time at which the custom event happens
        - `EventType` the event type that will get removed. (constants.EventType)
        - `track` the track of the event that's to be removed
        - `animationType` the animation type to remove (constants.Animations) leave empty to remove entire event
        '''

        if eventType not in EVENTTYPES:
            raise ValueError("EventTypes is invalid")
        elif animationType not in ANIMATORTYPES and animationType is not None:
            raise ValueError("animationType is invalid")

        with open(self.customLevelPath, 'r') as getData:
            events = json.load(getData)
        
        with open(self.customLevelPath, 'w') as Remove:
            
            for x in events["_customData"]["_customEvents"]:
                if x["_time"] == time and x["_type"] == eventType and x["_data"]["_track"] == track:
                    if animationType is not None:
                        if x["_data"].get(animationType) != None:
                            totals = 0
                            for y in x.keys():
                                totals = totals+1 if y in ANIMATORTYPES else totals
                            
                            if totals > 1 and animationType is not None:
                                del x["_data"][animationType]
                                json.dump(events, Remove)
                                return x
                    else:
                        events["_customData"]["_customEvents"].remove(x)
                        json.dump(events, Remove)
                        return x
            json.dump(events, Remove)
            
            

class Animator:

    def __init__(self, editor:Editor):
        '''just put in the Editor object you're using.'''
        if editor is None:
            raise ValueError("editor cannot be None")

        self.editor = editor # this is as to be able to access the actual level.dat file.

    def animate(self, eventType:str, animationType:str, data:list, track:str, start:int, end:int) -> dict:
        '''Animates a block and returns the Event's dictionary.
        This doesn't support `AssignTrackParent` and `AssignPlayerToTrack`.\n
        Instead, use `Animator.editTrack`\n
        If you want to re-animate a track's certain property, this script will change it and not dupe it.

        - `data` (list) that should look something like this;
        - `eventType` what kind of animation is this (noodle_extensions.EVENTTYPES)
        - `animationType` how the note should be animated. (noodle_extensions.ANIMATIONTYPES)

        It will be used to animate the blocks in the track.
        - First few data points. (Gained from noodle_extensions.TRACKANIMATIONFORMATS)
        - time  : The beat where the animation should start
        - ease  : easings. The speed which the note should move between animations. (can be gained from `noodle_extensions.EASINGSNET`)

        - `track` the track you want to animate.
        - `start` the start (in beats) where the animation should start
        - `end` the end (in beats) where the animation should end.
        '''
        
        if animationType not in ANIMATORTYPES:
            raise ValueError(f"The provided animation type {animationType} is not valid.")

        if eventType not in EVENTTYPES:
            raise ValueError(f"The provided event type {eventType} is not valid")


        if animationType == "_color":
            # add chroma as a requirement if using _color
            self.editor.updateDependencies("Chroma")
        
        with open(self.editor.customLevelPath, 'r') as GetCustomEvents:
            ce = json.load(GetCustomEvents)
        with open(self.editor.customLevelPath, 'w') as EditCustomEvents:
            if ce["_customData"].get("_customEvents") is None:
                ce["_customData"]["_customEvents"] = []

            for event in ce["_customData"]["_customEvents"]:
                if event["_data"]["_track"] == track and event["_type"] == eventType and event["_time"] == start and event["_data"]["_duration"] == (end-start):
                    event["_data"][animationType] = data
                    json.dump(ce, EditCustomEvents)
                    return event
            
            newEvent = {
                "_time": start,
                "_type": eventType,
                "_data": {
                    "_track": track,
                    "_duration": end-start,
                    animationType:data
                }
            }
            ce["_customData"]["_customEvents"].append(newEvent)
            json.dump(ce, EditCustomEvents)
            return newEvent


    def animateBlock(self, beat, pos:tuple, animationType:str, data) -> dict:
        '''Animate a specific note. (Returns the note's `_customData` property)
        - `beat` the beat at which the note can be found
        - `pos` The (x, y) position where the note is. (0, 0) is found left-most row, bottom layer.
        - `animationType` the property you want to animate. 
        - `data` how the note should be animated
        '''
        
        incorrect = True
        for x in ANIMATORTYPES:
            if x == animationType:
                incorrect = False
                break
        if incorrect:
            raise ValueError("Incorrect animation type")
        
        with open(self.editor.customLevelPath, 'r') as getNote:
            notes = json.load(getNote)

        note = self.editor.getBlock(beat, pos)
        with open(self.editor.customLevelPath, 'w') as editNote:
            for x in notes["_notes"]:
                if x == note:
                    if x.get("_customData") is None:
                        x["_customData"] = {
                            animationType:data
                        }
                    else:
                        x["_customData"][animationType] = data
            
                    json.dump(notes, editNote)
                    return x["_customData"]


    
    def animateWall(self, beat:int, length:int, index:int, animationType:str, data:list):
        '''Animates a specific wall.
        - `beat` the beat at which the wall starts.
        - `length` the length (in beat) of how long the wall is.
        - `index` 
        '''
        incorrect = True
        for x in ANIMATORTYPES:
            if x == animationType:
                incorrect = False
                break
        if incorrect:
            raise ValueError("Incorrect animation type")
        
        with open(self.editor.customLevelPath, 'r') as getWalls:
            walls = json.load(getWalls)
        
        wall = self.editor.getWall(beat, index, length)
        with open(self.editor.customLevelPath, 'w') as editWalls:
            for x in walls["_obstacles"]:
                if x == wall:
                    if x.get("_customData") is None:
                        x["_customData"] = {
                            animationType: data
                        }
                    else:
                        x["_customData"][animationType] = data
                    json.dump(walls, editWalls)
                    return x["_customData"]
    def editTrack(self, eventType, time, tracks, parentTrack:str=None) -> dict:
        '''Edit Track allows you to either do `AssignTrackParent` or `AssignPlayerToTrack` and returns the event
        - `eventType` Either `AssignTrackParent` or `AssignPlayerToTrack`
        - `time` The time (in beats) at which the event should happen
        - `tracks` either a list of all the tracks you want to edit or a single track.
        - `parentTrack` the track you want all of the `tracks` to be parented to. Only needed if using  `AssignTrackParent`
        '''

        tracks = tracks.split() if type(tracks) != list else tracks # Makes tracks a list if it is a string
        if eventType == "AssignTrackParent" and parentTrack is None:
            raise exceptions.NoParentTrack("Received AssignTrackParent but no parentTrack")
        
        if eventType == "AssignTrackParent":
            event = {
                "_time":time,
                "_type":eventType,
                "_data":{
                    "_childrenTracks":tracks,
                    "_parentTrack":parentTrack
                }
            }            
            with open(self.editor.customLevelPath, 'r') as getEvents:
                events = json.load(getEvents)

            with open(self.editor.customLevelPath, 'w') as editEvents:
                for customs in events["_customData"]["_customEvents"]:
                    if customs == event: # if the event already exists
                        json.dump(events, editEvents)
                        return event
                events["_customData"]["_customEvents"].append(event)
            return event
        
        elif eventType == "AssignPlayerToTrack":
            event = {
                "_time":time,
                "_type":eventType,
                "_data":{
                    "_track":tracks[0]
                }
            }

            with open(self.editor.customLevelPath, 'r') as getEvents:
                events = json.load(getEvents)
            
            with open(self.editor.customLevelPath, 'w') as editEvents:
                for customs in events["_customData"]["_customEvents"]:
                    if customs == event:
                        json.dump(events, editEvents)
                        return event
                events["_customData"]["_customEvents"].append(event)
                json.dump(events, editEvents)
                return event
