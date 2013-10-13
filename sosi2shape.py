# Simple python scripts that batch converts sosi files to shape
# cuts them to a defined feature and merges the result to files
# containing the same data.
# Copyright 2013 Torbjorn Vilhelmsen
# You are free to modify and redistribute this file as you want
# Uses arcpy and Geodata As Sosi<->shape 3.0


import arcpy, os, os.path, subprocess, re
from arcpy import env
koordsysdict = { #lookup dictionarythat maps the sosi koordsys variabe to arcgis spatialreference
	1: arcpy.SpatialReference(27391),
	2: arcpy.SpatialReference(27392),
	3: arcpy.SpatialReference(27393),
	4: arcpy.SpatialReference(27394),
	5: arcpy.SpatialReference(27395),
	6: arcpy.SpatialReference(27396),
	7: arcpy.SpatialReference(27397),
	8: arcpy.SpatialReference(27398),
	9: arcpy.SpatialReference(4273),
	21: arcpy.SpatialReference(32631),
	22: arcpy.SpatialReference(32632),
	23: arcpy.SpatialReference(32633),
	24: arcpy.SpatialReference(32634),
	25: arcpy.SpatialReference(32635),
	26: arcpy.SpatialReference(32636),
	31: arcpy.SpatialReference(23031),
	32: arcpy.SpatialReference(23032),
	33: arcpy.SpatialReference(23033),
	34: arcpy.SpatialReference(23034),
	35: arcpy.SpatialReference(23035),
	36: arcpy.SpatialReference(23036),
	50: arcpy.SpatialReference(4230),
	72: arcpy.SpatialReference(4322),
	84: arcpy.SpatialReference(4326),
	87: arcpy.SpatialReference(4231)
}
envworkspace = "c:\\SOSI\\" #path to sosi files
clipfeature = False
#clipfeature = "c:\\sos\\clip.shp" #path to feature file to clip from comment this line to not clip features
outputdir = "c:\\SOSI\\result\\" #dir to move the resulting files to
merge = True # set this to false to not merge features
deletepreclip = True
fileprefix = "^[0-9][0-9]_[0-9][0-9][0-9][0-9]" #you can use [0-9] to replace unknown numbers
sosishapebin = r'"C:\Program Files (x86)\Geodata AS\SOSI-Shape\bin\Sosi2Av.exe"'
def getKoordsys(sosifile):
	with open(sosifile) as f:
		for line in f:
			if line.lower().find("koordsys")>-1:
				koordsysStr = line.lower()
				break
		koordsys = koordsysStr.replace("...koordsys ", "")
		return int(koordsys)
def mergeFeatureClasses(shapedir):
	if not os.path.isdir(outputdir):
		os.makedirs(outputdir)
	for root, _, files in os.walk(envworkspace):
	    for f in files:
	        fullpath = os.path.join(root, f)
	        if f.lower().endswith(".shp"):
	        	m = re.search(fileprefix, f)
	        	name = f[m.end():]
			if not os.path.exists(outputdir+name):
				arcpy.Copy_management(fullpath, outputdir+name)
				arcpy.Delete_management(fullpath)
			else:
				#SChould look into some potential mappings here
				arcpy.Append_management([fullpath], outputdir+name, "NO_TEST")
				arcpy.Delete_management(fullpath)



def removeEmptyShapeFile(shapefile):
	#cleans up empty shape files after processing
	count = int(arcpy.GetCount_management(shapefile).getOutput(0)) 
	print count
	if count == 0:
		print "Removing "+shapefile
		arcpy.Delete_management(shapefile)
		return False
	return True

def defineProjection(sosifile, shapefile):
	koordsys = getKoordsys(sosifile)
	print koordsys
	sr = koordsysdict[koordsys]
	arcpy.DefineProjection_management(shapefile, sr)

def executeSosiShape(args, f,fullpath, tempDir,append):
	flower = f.lower().replace('.sos','')
	output = tempDir+flower+"_"+append
	arg = args.format(fullpath, output)
	a = subprocess.call(sosishapebin+arg, shell=True)
	shapefile = output+'.shp'
	if removeEmptyShapeFile(shapefile):
		defineProjection(fullpath, shapefile)

def dir2shape(): 
	tempDir = envworkspace+"tmp\\"
	if not os.path.isdir(tempDir):
		os.makedirs(tempDir)
	lineargs = ' -L "{1}" "{0}"'
	polygonargs = ' -F "{1}" "{0}"'
	pointargs = ' -P "{1}" "{0}"'
	for root, _, files in os.walk(envworkspace):
	    for f in files:
	        fullpath = os.path.join(root, f)
	        if f.lower().endswith(".sos"):
	            executeSosiShape(lineargs,f,fullpath,tempDir,"l")
	            executeSosiShape(polygonargs,f,fullpath,tempDir,"f")
	            executeSosiShape(pointargs,f,fullpath,tempDir,"p")
	if clipfeature:
		clipfeatureclasses(clipfeature, tempDir)
	if merge:
		mergeFeatureClasses(tempDir)
def clipfeatureclasses(clipFeature, indir):
	feature_classes = []
	for root, _, files in os.walk(indir): #os.walk instead of arcpy.da.Walk because 10.1 sp1 is not installed
	    for f in files:
	        fullpath = os.path.join(root, f)
	        if f.lower().endswith(".shp"):
	        	feature_classes.append(fullpath)
	for feature in feature_classes:
		print "Clipping "+feature
		shapefile =  feature.replace(".shp","")+"_clip.shp"
		arcpy.Clip_analysis(feature, clipFeature, shapefile)
		removeEmptyShapeFile(shapefile)
		if deletepreclip:
			arcpy.Delete_management(feature)
dir2shape()