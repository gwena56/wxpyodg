# wxpyodg
Python lib for making wxPython UI from an openoffice draw file
- General view (mind mapping)
![alt tag](https://github.com/gwena56/wxpyodg/blob/master/howto/img1.png)
- odglib view (mind mapping)
![alt tag](https://github.com/gwena56/wxpyodg/blob/master/howto/img2.png)
- Parsing XML view (mind mapping)
![alt tag](https://github.com/gwena56/wxpyodg/blob/master/howto/img3.png)

# Dependances
- wxPython 3
- Pillow library for Python
- Some commons python lib (subprocess, shlex, os, sys, ...)

# little how to
- use only png image file inside odg (very important)
- In openoffice (See example ./odg/carpc.odg)
    - do a new odg file sized to a background image (must be the first draw in the odg file)
    - Draw ui element (only rectangle and circle/ellipse at the moment).
    - double-click on draw to put the name of the element as text.
        Example
            - draw a rectangle
            - double-cick 
                - first line put the name of the item ex STD_PUSHBT_name
                - second line put command for the item ex RUN_python <script> 
- Example carpc.py
    - all in comments (french only)
- Example of Openoffice construct file
    - show file carpcUImaking.odg in howto folder for comprehensive tool. 

#Testing Todo List
- Refresh drawing wxPython
- Test Rasberry pi
- Test CubieBoard
- Test Win32
- Test Ubuntu/Debian
- Test Mac OS X
    - install several needed libraries with mac ports or pip (OK)
    - start with console/terminal(OK)
