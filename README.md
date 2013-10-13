sosi2shape.py
=============

Simple script that uses Geodatas Sosi&lt;->Shape 3.0 and ESRI's arcpy

Description
-----------
Uses Geodata AS' SOSI<->Shape 3.0 to batch convert a folder of .sos files to shape.
Gets the correct projection from the koordsys variable and defines it.
Option to clip all generated layers to a defined feature set.
Option to merge all layers to containing the same kinds of data (typically used when converting FKB data from multiple municipalities)

Usage
-----
There are some global variables that need to be modified before executing the script.

    sosidir = "c:\\SOSI\\" #path to sosi files
    
    clipfeature = "c:\\SOSI\\clip.shp" # path to feature class to clip from. Set to False to skip clipping
    
    outputdir = "c:\\SOSI\\result\\" #dir to move the resulting files to
    
    merge = True # set this to False to not merge features
    
    deletepreclip = True # Set this to False to keep files that are created before clipping
    
    fileprefix = "^[0-9][0-9]_[0-9][0-9][0-9][0-9]" # Defines the common prefix for your sosi files. Used when merging. You can use [0-9] to replace unknown numbers
    
    sosishapebin = r'"C:\Program Files (x86)\Geodata AS\SOSI-Shape\bin\Sosi2Av.exe"' # Path to the executable Sosi2Av.exe from Sosi<->shape
    
