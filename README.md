sosi2shape.py
=============
Requirements
-----------
SOSI<->Shape 3.0
ArcGis extensions to python arcpy

Description
-----------
Uses Geodata AS' SOSI<->Shape 3.0 to batch convert a folder of .sos files to shape.

Gets the correct projection from the koordsys variable and defines it.

Option to clip all generated layers to a defined feature set.

Option to merge all layers to containing the same kinds of data (typically used when converting FKB data from multiple municipalities)

Usage
-----
See example.py for sample usage

    import sosi2shape
    from sosi2shape import dir2shape
    #User options
    sosidir = "c:\\Areal\\" #path to sosi files
    clipfeature = False  # path to feature class to clip from. Set to False to skip clippings
    clipfeature = "c:\\sos\\clip.shp" #path to feature file to clip from comment this line to not clip features comment this line to skip clipping
    outputdir = "c:\\Areal\\result\\" #dir to move the resulting files to
    merge = True # set this to false to not merge features
    deletepreclip = True # Set this to false to keep files that are created before clipping
    fileprefix = "^[0-9][0-9]_[0-9][0-9][0-9][0-9]" #Defines the common prefix for your sosifiles. Used when merging. You can use [0-9] to replace unknown numbers
    sosishapebin = r'"C:\Program Files (x86)\Geodata AS\SOSI-Shape\bin\Sosi2Av.exe"' # Path to the executable Sosi2Av.exe from Sosi<->shape
    dir2shape(sosidir, clipfeature, outputdir, merge, deletepreclip, fileprefix, sosishapebin)

Running
-------

        <path-to-python>\python.exe <script>

Example:

        C:\Python27\ArcGIS10.1\python.exe example.py
