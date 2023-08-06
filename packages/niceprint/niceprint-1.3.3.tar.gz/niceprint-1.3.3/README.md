Niceprint
---------
This python module is used to print text 
in a fashonable, colored and styled way

Usage
-----

Print :
    This is a class which prints the given text or group of texts in a 
    particular color and at a particular time.
#### Example
```
from niceprint import Print
Print("Print test", color="c")
```

MultiColoredPrint :
    This is a class which prints a given text or group of 
    texts in different colors at a particular time
#### Example
```
from niceprint import MultiColoredPrint as mcp
mcp("Print test", color=["r", "g"])
```
ProgressBar:
    This class creates a progress bar which can be pulsed or filled
#### Example
```
from niceprint import ProgressBar as pb
progress = pb(len=10, color="green")
progress.pulse(step=10)
progress.fill(ms=20)
```

Installation
-----------
For installation
`pip install niceprint` or `pip3 install niceprint`
