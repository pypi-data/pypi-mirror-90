# Python Noodle Extensions Editor (PNEE)
*pronounced /nē/ (Ni)*
```
PPPPPPPPPPPPPPPPP   NNNNNNNN        NNNNNNNNEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE
P::::::::::::::::P  N:::::::N       N::::::NE::::::::::::::::::::EE::::::::::::::::::::E
P::::::PPPPPP:::::P N::::::::N      N::::::NE::::::::::::::::::::EE::::::::::::::::::::E
PP:::::P     P:::::PN:::::::::N     N::::::NEE::::::EEEEEEEEE::::EEE::::::EEEEEEEEE::::E
  P::::P     P:::::PN::::::::::N    N::::::N  E:::::E       EEEEEE  E:::::E       EEEEEE
  P::::P     P:::::PN:::::::::::N   N::::::N  E:::::E               E:::::E             
  P::::PPPPPP:::::P N:::::::N::::N  N::::::N  E::::::EEEEEEEEEE     E::::::EEEEEEEEEE   
  P:::::::::::::PP  N::::::N N::::N N::::::N  E:::::::::::::::E     E:::::::::::::::E   
  P::::PPPPPPPPP    N::::::N  N::::N:::::::N  E:::::::::::::::E     E:::::::::::::::E   
  P::::P            N::::::N   N:::::::::::N  E::::::EEEEEEEEEE     E::::::EEEEEEEEEE   
  P::::P            N::::::N    N::::::::::N  E:::::E               E:::::E             
  P::::P            N::::::N     N:::::::::N  E:::::E       EEEEEE  E:::::E       EEEEEE
PP::::::PP          N::::::N      N::::::::NEE::::::EEEEEEEE:::::EEE::::::EEEEEEEE:::::E
P::::::::P          N::::::N       N:::::::NE::::::::::::::::::::EE::::::::::::::::::::E
P::::::::P          N::::::N        N::::::NE::::::::::::::::::::EE::::::::::::::::::::E
PPPPPPPPPP          NNNNNNNN         NNNNNNNEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE
```
## my to-do list
If you want to know what's currently on my to-do list, you can go [here](https://trello.com/b/yA5qQTs7)! Pull requests, feedback, issues, and more are appreciated. If you'd like to contact me, you can do so on discord at `megamaz#1020`
## What is it?
This is a Python Noodle Extensions Editor for Beat Saber levels. Manually editing a JSON file over a long period of time can get really annoying, so this should speed up the process!

## How do I use it?
The docs can be found [Here!](https://github.com/megamaz/NoodleExtensions-python/blob/master/docs/documentation.md) (needs to be fixed and finished!)\
As of installation, you can simply `pip install NoodleExtensions` and you'll be ready to `import noodle_extensions` inside your project.\
No credits are required! Suprisingly a few people have asked me about that. this is just meant to be helpful and if you'd like to give credit that's fine.

## Extra notes:
- Made entirely in python
- Pull requests are appreciated. Someone needs to fix up my horid code.
# Samples

## Simple (blank) animation
```py
from noodle_extensions import Editor, Animator
from noodle_extensions.constants import EventType, Animations

editor = Editor("YourLevel.datPath")
animator = Animator(editor)

# Animations can go here.
# Basic position animation (that does nothing)
animator.animate(EventType().AnimateTrack, Animations().position, [[0, 0]], "DummyTrack", 0, 3)
```

## Current Issues:
- `Editor().updateDependencies` does not work if there are multiple difficulties.
#### Currently testing features (checked features have been tested and are working)
* [ ] Editor.updateDependencies
* [X] Editor.editBlock
* [X] Editor.editWall
* [X] Editor.getBlock
* [X] Editor.getWall
* [X] Editor.removeEvent
* [X] Animator.animate
* [X] Animator.animateBlock
* [X] Animator.animateWall
* [X] Animator.editTrack
