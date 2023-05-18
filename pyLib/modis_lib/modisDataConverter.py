
import glob
import os
from osgeo import gdal

"""
Öffnet alle MOD13Q1-Files in einem Ordner und speichert den NDVI-Layer als .tif File
"""

def convertHDFtoTif(srcFolder=" ",dest_Folder=" "):

	if srcFolder==" ":
		globCommand="*.hdf"
	else:
		globCommand=srcFolder+"/"+"*.hdf"

	modisFiles=glob.glob(globCommand)

	for modis_ds in modisFiles :

		#seperate name from path
		nameParts=getFileNameParts(modis_ds,"MOD13Q1",".")
		finalName=nameParts[0]+"."+nameParts[1]+"."+nameParts[2]
		if dest_Folder==" ":
			convertFileName=finalName+".tif"
		else:
			convertFileName=dest_Folder+"/"+finalName+".tif"
		print(convertFileName)

		#read NDVI band
		hdf_ds = gdal.Open(modis_ds)
		NDVI_band=hdf_ds.GetSubDatasets()[0][0]

		#run conversion command
		command="gdal_translate "+NDVI_band+" "+ convertFileName
		os.popen(command)

#----------------------------------------------------------------------------------------------------

import rasterio
import glob
import os
from osgeo import gdal

"""
Öffnet die MOD13Q1 Daten und speichert den NDVI-Layer als .tif File
"""

def convertHDFtoTifFromFilePath(filepath,dest_Folder=" "):

		modis_ds=filepath

		#seperate name from path
		nameParts=getFileNameParts(modis_ds,"MOD13Q1",".")
		finalName=nameParts[0]+"."+nameParts[1]+"."+nameParts[2]

		if dest_Folder==" ":
			convertFileName=finalName+".tif"
		else:
			convertFileName=dest_Folder+"/"+finalName+".tif"
		print(convertFileName)

		#read NDVI band
		hdf_ds = gdal.Open(modis_ds)
		NDVI_band=hdf_ds.GetSubDatasets()[0][0]

		#run conversion command
		command="gdal_translate "+NDVI_band+" "+ convertFileName
		os.popen(command)


#----------------------------------------------------------------------------------------------------
#### ANA CDL clipping

def clipData_CDL(shapesFolderPath, rasterFile, dest_FolderPath,countryCode=""):
    """
    This fuction takes as input:
    - shapesFolderPath: the folder with Shape files
    - rasterFile: the file to clip, in this case the CDLresized
    - dest_FolderPath: folder to write files cliped
    - countryCode: name of the country for keep track

    returns: nothing
    it just transform the input and saves the files
    """

    shapes=glob.glob(shapesFolderPath+"/*.shp") #finds all shapes to clipp
    ds=gdal.Open(rasterFile)

    for countyShapePath in shapes:

        #get CDLrescaled without datatype and path
        rasterFileName=rasterFile.replace(".tif","")
        startIndex=rasterFileName.find("CDLr")
        rasterFileName=rasterFileName[startIndex:]
        rasterFileNameParts=rasterFileName.split(".")#get parts of the name file
        #this is for giving a name to the otput later on

        #get parts of name of shape file :
        countyLevelID=checkCountyLevelID(countyShapePath)
        indexShapeFiles=countyShapePath.find(countyLevelID)
        shapeFileName=countyShapePath[indexShapeFiles:]
        countyIDShape=shapeFileName.replace(countyLevelID+"_","").replace(".shp","")

        #give name to output file based on shape file and CDL info
        outputName=rasterFileName+"."+countryCode+"."+countyIDShape+".tif"

        outputPath=dest_FolderPath+"/"+outputName

        print(outputPath)
        #the actual clipping:
        dsClip=gdal.Warp(outputPath,ds,cutlineDSName=countyShapePath,cropToCutline=True, dstNodata=-1)

def getFilesToClip_CDL(year,srcFolderPath=" "):
    """
    This fuction looks for all the CDLrescaled files and returns them in a list.
    Takes as input:
    - year: the year from wich the search of files begigns
    - srcFolderPath: folder on wich the search is made

    returs:
    - selectedFilePaths: a list of file paths
    """
    if srcFolderPath==" ":
        globCommand="*.tif";
    else:
        globCommand=srcFolderPath+"/*.tif"

    allFiles=glob.glob(globCommand)
    selectedFilePaths=[]
    allFiles = [s.replace('\\', '/') for s in allFiles]

    for filePath in allFiles:
        fileYear=filePath.split(".")[1] #get the year
        if(int(fileYear)>=year):
            selectedFilePaths.append(filePath)
        else:
            print("please check filename")

    return selectedFilePaths


#________________________________________________________________
import fiona
import glob
from osgeo import gdal
import time

"""
Clippen der Rasterfiles anhand der Shapefiles.
"""

def clipData(shapesFolderPath, rasterFile, dest_FolderPath,countryCode=""):
	shapes=glob.glob(shapesFolderPath+"/*.shp")

	ds=gdal.Open(rasterFile)

	for countyShapePath in shapes:

		#get mergedFileName without datatype and path
		#print(rasterFile)
		rasterFileName=rasterFile.replace(".tif","")
		startIndex=rasterFileName.find("MOD")
		rasterFileName=rasterFileName[startIndex:]
		rasterFileNameParts=rasterFileName.split(".")
		#print(rasterFileName)

		countyLevelID=checkCountyLevelID(countyShapePath)
		indexShapeFiles=countyShapePath.find(countyLevelID)
		shapeFileName=countyShapePath[indexShapeFiles:]
		countyIDShape=shapeFileName.replace(countyLevelID+"_","").replace(".shp","")
		outputName=rasterFileName+"."+countyIDShape+".tif"
		#print(outputName)

		if countryCode=="":
			outputName=rasterFileName+"."+countyIDShape+".tif"
		else:
			outputName=rasterFileNameParts[0]+"."+countryCode+"."+rasterFileNameParts[2]+"."+countyIDShape+".tif"

		outputPath=dest_FolderPath+"/"+outputName

		print(outputPath)
		dsClip=gdal.Warp(outputPath,ds,cutlineDSName=countyShapePath,cropToCutline=True, dstNodata=-1)

def clipData2(shapesFolderPath, rasterFile, dest_FolderPath,countryCode=""):
	shapes=glob.glob(shapesFolderPath+"/*.shp")

	ds=gdal.Open(rasterFile)

	for countyShapePath in shapes:

		#get mergedFileName without datatype and path
		#print(rasterFile)
		rasterFileName=rasterFile.replace(".tif","")
		startIndex=rasterFileName.find("MOD")
		rasterFileName=rasterFileName[startIndex:]
		rasterFileNameParts=rasterFileName.split(".")
		#print(rasterFileName)

		countyLevelID=checkCountyLevelID(countyShapePath)
		indexShapeFiles=countyShapePath.find(countyLevelID)
		shapeFileName=countyShapePath[indexShapeFiles:]
		countyIDShape=shapeFileName.replace(countyLevelID+"_","").replace(".shp","")
		outputName=rasterFileName+"."+countyIDShape+".tif"
		print(outputName)

		if countryCode=="":
			outputName=rasterFileName+"."+countyIDShape+".tif"
		else:
			outputName=rasterFileNameParts[0]+"."+countryCode+"."+rasterFileNameParts[2]+"."+countyIDShape+".tif"

		outputPath=dest_FolderPath+"/"+outputName

		print(outputPath)
		dsClip=gdal.Warp(outputPath,ds,cutlineDSName=countyShapePath,cropToCutline=True, dstNodata=-1)



# ----------------------------------------------------------------------------
from skimage import io
import numpy as np
from PIL import Image

"""
Einfügen eines Paddings um die geclippten Files auf eine einheitliche größe zu bringen.
"""

def reshapeClippedFiles(srcFolder,dest_Folder,year,hight, width):
	allFiles=glob.glob(srcFolder+"/*.tif")
	selectedFilePaths=[]

	for filePath in allFiles:
		nameParts=getFileNameParts(filePath,"MOD13Q1",".")
		fileYear=nameParts[2][1:5]


		if(int(fileYear)>=year):
			selectedFilePaths.append(filePath)

	for filePath in selectedFilePaths:
		im = io.imread(filePath)
		filenameIndex=filePath.find("MOD13Q1")
		fileName=filePath[filenameIndex:]

		def padding(array, xx, yy):
			"""
			:param array: numpy array
			:param xx: desired height
			:param yy: desirex width
			:return: padded array
			"""

			h = array.shape[0]
			w = array.shape[1]

			a = (xx - h) // 2
			aa = xx - a - h

			b = (yy - w) // 2
			bb = yy - b - w

			return np.pad(array, pad_width=((a, aa), (b, bb)), mode='constant',constant_values=(-1))

		im=padding(im,hight,width)
		print(im.shape)


		im = Image.fromarray(im)
		outputFilePath=dest_Folder+"/"+fileName
		print(outputFilePath)
		im.save(outputFilePath)

#----------------------------------------------------------------------------------------------------
from skimage import io
import numpy as np
from PIL import Image
def normalization_min_max(array, a_min = -20000000, a_max=100000000):
    """
    Takes an array and normalize its values to give an output 
    with elements between 0 and 1. 
    """
    array_resc = (array-a_min)/(a_max -a_min)
    
    return array_resc

"""
Einfügen eines Paddings um die geclippten Files auf eine einheitliche größe zu bringen.
"""
def reshapeClippedFilesCompressed(srcFolder,dest_Folder,year,height, width):
	allFiles=glob.glob(srcFolder+"/*.tif")
	selectedFilePaths=[]
	driver = gdal.GetDriverByName('GTiff')

	for filePath in allFiles:
		nameParts=getFileNameParts(filePath,"MOD13Q1",".")
		fileYear=nameParts[2][1:5]


		if(int(fileYear)>=year):
			selectedFilePaths.append(filePath)

	for filePath in selectedFilePaths:
		im = io.imread(filePath)
		filenameIndex=filePath.find("MOD13Q1")
		fileName=filePath[filenameIndex:]

		def padding(array, xx, yy):
			"""
			:param array: numpy array
			:param xx: desired height
			:param yy: desirex width
			:return: padded array
			"""

			h = array.shape[0]
			w = array.shape[1]

			a = (xx - h) // 2
			aa = xx - a - h

			b = (yy - w) // 2
			bb = yy - b - w

			return np.pad(array, pad_width=((a, aa), (b, bb)), mode='constant',constant_values=(-1))

		im=padding(im,height,width)
		#rescaled = normalization_min_max(im) #get pixel values to range [0,1]
		#now transfer -1 from im
		#rescaled = np.where(im == -1, im, rescaled)
		#im = rescaled 
		print(im.shape)
		
		outputFilePath=dest_Folder+"/"+fileName
		print(outputFilePath, "-- -- -- ")
		#print(driver)
		dstImg = driver.Create(outputFilePath, width, height, 1, gdal.GDT_Int32, options = [ 'COMPRESS=DEFLATE' ])

		#print(dstImg)
		dstImg.GetRasterBand(1).WriteArray(im)
		dstImg.FlushCache()

print("hyyywertuuu  ttttteeettt")

def reshapeClippedFilesCompressed2(srcFolder,dest_Folder,year,height, width):
	allFiles=glob.glob(srcFolder+"/*.tif")
	selectedFilePaths=[]
	driver = gdal.GetDriverByName('GTiff')

	for filePath in allFiles:
		nameParts=getFileNameParts(filePath,"MOD13Q1",".")
		fileYear=nameParts[2][1:5]


		if(int(fileYear)>=year):
			selectedFilePaths.append(filePath)

	for filePath in selectedFilePaths:
		im = io.imread(filePath)
		filenameIndex=filePath.find("MOD13Q1")
		fileName=filePath[filenameIndex:]

		def padding(array, xx, yy):
			"""
			:param array: numpy array
			:param xx: desired height
			:param yy: desirex width
			:return: padded array
			"""

			h = array.shape[0]
			w = array.shape[1]

			a = (xx - h) // 2
			aa = xx - a - h

			b = (yy - w) // 2
			bb = yy - b - w

			return np.pad(array, pad_width=((a, aa), (b, bb)), mode='constant',constant_values=(-1))

		im=padding(im,height,width)
		rescaled = im*0.00000001 #get pixel values to range [-0.2,1]
		#now transfer -1 from im
		rescaled = np.where(im == -1, im, rescaled)#because -1  were also nomilized
		
		#rescaled = normalization_min_max(im) #get pixel values to range [0,1]
		#now transfer -1 from im
		#rescaled = np.where(im == -1, im, rescaled)
		#im = rescaled 
		#print(im.shape)
		
		outputFilePath=dest_Folder+"/"+fileName
		print(outputFilePath)
		#print(driver)
		dstImg = driver.Create(outputFilePath, width, height, 1, gdal.GDT_Int32, options = [ 'COMPRESS=DEFLATE' ])

		#print(dstImg)
		dstImg.GetRasterBand(1).WriteArray(rescaled)
		dstImg.FlushCache()

def reshapeClippedFilesCompressed33(srcFolder,dest_Folder,year,height, width):
	allFiles=glob.glob(srcFolder+"/*.tif")
	selectedFilePaths=[]
	driver = gdal.GetDriverByName('GTiff')

	for filePath in allFiles:
		nameParts=getFileNameParts(filePath,"MOD13Q1",".")
		fileYear=nameParts[2][1:5]


		if(int(fileYear)>=year):
			selectedFilePaths.append(filePath)

	for filePath in selectedFilePaths:
		im = io.imread(filePath)
		filenameIndex=filePath.find("MOD13Q1")
		fileName=filePath[filenameIndex:]

		def padding(array, xx, yy):
			"""
			:param array: numpy array
			:param xx: desired height
			:param yy: desirex width
			:return: padded array
			"""

			h = array.shape[0]
			w = array.shape[1]

			a = (xx - h) // 2
			aa = xx - a - h

			b = (yy - w) // 2
			bb = yy - b - w

			return np.pad(array, pad_width=((a, aa), (b, bb)), mode='constant',constant_values=(-1))

		im=padding(im,height,width)#*0.0001
		print(np.unique(im))
		##rescaled = im*0.0001 #get pixel values to range [-2,000. , 10,000.]
		#now transfer -1 from im
		#rescaled = np.where(im == -1, im, im*0.0001)#because -1  were also nomilized
		
		#im = rescaled 
		print(im.shape, "ddd")
		im=im*0.0001
		print(np.unique(im))
		outputFilePath=dest_Folder+"/"+fileName
		print(outputFilePath, "_33_")
		#print(driver)
		dstImg = driver.Create(outputFilePath, width, height, 1, gdal.GDT_Int32, options = [ 'COMPRESS=DEFLATE' ])

		#print(dstImg)
		dstImg.GetRasterBand(1).WriteArray(im)
		dstImg.FlushCache()

#----------------------------------------------------------------------------------------------------
from skimage import io
import numpy as np
from PIL import Image

"""
Einfügen eines Paddings um die geclippten Files auf eine einheitliche größe zu bringen.
"""

def compressGTIFF(filePath,outputFilePath):
	img = io.imread(filePath)
	print(img.shape)
	driver = gdal.GetDriverByName('GTiff')
	dataset = driver.Create(outputFilePath,img.shape[1], img.shape[0], 1, gdal.GDT_Int32, options = [ 'COMPRESS=DEFLATE' ])
	dataset.GetRasterBand(1).WriteArray(img)
	dataset.FlushCache()
#----------------------------------------------------------------------------------------------------
import numpy as np

def paddingWithNODATA(array, xx, yy, noData):
	"""
	:param array: numpy array
	:param xx: desired height
	:param yy: desirex width
	:return: padded array
	"""

	h = array.shape[0]
	w = array.shape[1]

	a = (xx - h) // 2
	aa = xx - a - h

	b = (yy - w) // 2
	bb = yy - b - w

	return np.pad(array, pad_width=((a, aa), (b, bb)), mode='constant',constant_values=(noData))

	#----------------------------------------------------------------------------------------------------

import glob

def selectModisFiles(srcFolderPath):

	mergeFiles=[]
	allFiles= glob.glob(srcFolderPath+"/*.tif")

	for file in allFiles:

		#seperate name from path
		nameParts=getFileNameParts(file,"MOD13Q1",".")
		finalName=nameParts[0]+"."+nameParts[1]

		if finalName not in mergeFiles:
			mergeFiles.append(finalName)

	return mergeFiles

#----------------------------------------------------------------------------------------------------

import glob
import os

"""
Mergen einer List an tif-Files zu einer einzelnen tif-File
"""

def merge_tif(filesToMerge,mergedFiles,countryCode):

	outvrt = '/vsimem/merged.vrt' #/vsimem is special in-memory virtual "directory"

	fileName=filesToMerge[0]
	nameParts=getFileNameParts(fileName,"MOD13Q1",".")
	finalName=nameParts[0]+"."+countryCode+"."+nameParts[1]+".tif"
	outtif=mergedFiles+"/"+finalName

	outds = gdal.BuildVRT(outvrt, filesToMerge, separate=False)
	outds = gdal.Translate(outtif, outds)

#----------------------------------------------------------------------------------------------------
import glob

def getMergeFilesFromCode(modisCode,srcFolderPath=" "):
	selectedFiles=[]

	if srcFolderPath==" ":
		globCommand="*"+modisCode+"*";

	else:
		globCommand=srcFolderPath+"/"+"*"+modisCode+"*"

	allFiles = glob.glob(globCommand)
	for file in allFiles:
		selectedFiles.append(str(file).replace("\\","/"))

	return selectedFiles

#----------------------------------------------------------------------------------------------------

import glob
from shutil import rmtree
import time

"""
Erstellen einer liste die alle file-paths enthält die geclippt werden sollen
"""

def getFilesToClip(year,srcFolderPath=" "):

	if srcFolderPath==" ":
		globCommand="*.tif";
	else:
		globCommand=srcFolderPath+"/*.tif"

	allFiles=glob.glob(globCommand)
	selectedFilePaths=[]
	allFiles = [s.replace('\\', '/') for s in allFiles]
	#print(allFiles)
	for filePath in allFiles:

		nameParts=getFileNameParts(filePath,"MOD13Q1",".")
		fileYear=nameParts[2][1:5]

		if(int(fileYear)>=year):
			selectedFilePaths.append(filePath)
		else:
		    print("please check filename")




	return selectedFilePaths

#----------------------------------------------------------------------------------------------------

import os

"""
Überprüfen ob ein Ordner vorhanden ist,
wenn ja wird dieser gelöscht und neu ersellt,
wenn nein wird dieser neu erstellt.
"""

def checkDirectory(directoryName):

	if not os.path.exists(directoryName):
		os.mkdir(directoryName)
	else:
		rmtree(directoryName)
		time.sleep(1.0)
		os.mkdir(directoryName)

	time.sleep(1.0)

#----------------------------------------------------------------------------------------------------

import glob

"""
Sammeln alles Pfade für MOD13Q1-Files/HDF-Files in einem bestimmten Zeitraum
"""

def getHDFFilesFromPeriod(startyear, endyear, srcFolder=" "):
	allFiles=[]
	selectedYear=startyear

	while selectedYear < endyear+1:
		if srcFolder==" ":
			globCommand="MOD13Q1.A"+str(selectedYear)+"*"+".hdf"
		else:
			globCommand=srcFolder+"/"+"*"+"MOD13Q1.A"+str(selectedYear)+"*"+".hdf"

		selectedYear+=1
		print(globCommand)
		yearFiles=glob.glob(globCommand)
		for file in yearFiles:
			allFiles.append(file)
		#print(allFiles)
	return allFiles


#----------------------------------------------------------------------------------------------------

import rasterio
import glob

"""
Suchen der Maximalen Höhe und Breite aller Files in einem Ordner. Dies wird später fürs Padding verwendet, damit alle Files in die KI gespeißt weren können.
"""

def getMaxFileSize(srcFolder=" "):
	print("Check max Filesize")
	maxWidth=0
	maxHeight=0
	print(srcFolder)
	if srcFolder==" ":
		globCommand="*.tif"
	else:
		globCommand=srcFolder+"/"+"*.tif"

	allFiles=glob.glob(globCommand)
	print("checking "+str(len(allFiles))+" Files. This probably takes some time...")

	for file in allFiles:
		raster_ds=rasterio.open(file)
		width=raster_ds.width
		height=raster_ds.height
		if height>maxHeight:
			maxHeight=height
		if width>maxWidth:
			maxWidth=width

	print("max. height:")
	print(maxHeight)
	print("max. width:")
	print(maxWidth)
#----------------------------------------------------------------------------------------------------
import rasterio
import glob

"""
Suchen der Maximalen Höhe und Breite aller Files in einem Ordner. Dies wird später fürs Padding verwendet, damit alle Files in die KI gespeißt weren können.
"""

def getMaxFileSizeAuto(srcFolder=" "):
	print("Check max Filesize")
	maxWidth=0
	maxHeight=0

	if srcFolder==" ":
		globCommand="*.tif"
	else:
		globCommand=srcFolder+"/"+"*.tif"

	allFiles=glob.glob(globCommand)
	#print(allFiles, "________**************")
	refFile=allFiles[0]
	index=refFile.find("MOD13Q1")
	refFileName=refFile[index:]
	refFileNameParts=refFileName.split(".")
	#print(refFileNameParts)
	year=refFileNameParts[2]

	if srcFolder==" ":
		globCommand="*"+year+"*.tif"
	else:
		globCommand=srcFolder+"/"+"*"+year+"*.tif"

	allFiles=glob.glob(globCommand)
	#print(globCommand)

	print("checking "+str(len(allFiles))+" Files. This probably takes some time...")

	for file in allFiles:
		raster_ds=rasterio.open(file)
		width=raster_ds.width
		height=raster_ds.height
		#print("w:", width, "h:", height)
		if height>maxHeight:
			maxHeight=height
		if width>maxWidth:
			maxWidth=width

	print("max. height:")
	print(maxHeight)
	print("max. width:")
	print(maxWidth)

	return maxHeight,maxWidth


def getMaxFileSizeAuto_CDL(srcFolder=" "):
	print("Check max Filesize")
	maxWidth=0
	maxHeight=0

	if srcFolder==" ":
		globCommand="*.tif"
	else:
		globCommand=srcFolder+"/"+"*.tif"

	allFiles=glob.glob(globCommand)
	refFile=allFiles[0]
	index=refFile.find("rCDL")
	refFileName=refFile[index:]
	refFileNameParts=refFileName.split(".")
	print(refFileNameParts)
	year=refFileNameParts[1]

	if srcFolder==" ":
		globCommand="*"+year+"*.tif"
	else:
		globCommand=srcFolder+"/"+"*"+year+"*.tif"

	allFiles=glob.glob(globCommand)
	print(globCommand)

	print("checking "+str(len(allFiles))+" Files. This probably takes some time...")

	for file in allFiles:
		raster_ds=rasterio.open(file)
		width=raster_ds.width
		height=raster_ds.height
		print("w:", width, "h:", height)
		if height>maxHeight:
			maxHeight=height
		if width>maxWidth:
			maxWidth=width

	print("max. height:")
	print(maxHeight)
	print("max. width:")
	print(maxWidth)

	return maxHeight,maxWidth
#----------------------------------------------------------------------------------------------------
from osgeo import gdal
import glob

"""
stacken aller files in einer List zu einem Datacube
"""

def stackFiles(outDir, allFilesToStack):
	#print(outDir)
	outvrt = '/vsimem/stacked.vrt' #/vsimem is special in-memory virtual "directory"

	referenceFile=allFilesToStack[len(allFilesToStack)-1]
	#print(referenceFile)
	nameParts=getFileNameParts(referenceFile,"MOD13Q1",".")
	namePartCountryCode=nameParts[1]
	namePartYear=len(nameParts[2])-3
	outputName=nameParts[0]+"."+namePartCountryCode+"."+nameParts[2][:namePartYear]+"."+nameParts[3]+".tif"

	outtif = outDir+"/"+outputName

	print(outtif)
	tifs = allFilesToStack
	#print(tifs)

	outds = gdal.BuildVRT(outvrt, tifs, separate=True)
	outds = gdal.Translate(outtif, outds)

#----------------------------------------------------------------------------------------------------
from osgeo import gdal
import glob

"""
stacken aller files in einer List zu einem Datacube
"""

def stackFilesCompressed(outDir, allFilesToStack):
	#print(outDir)
	outvrt = '/vsimem/stacked.vrt' #/vsimem is special in-memory virtual "directory"

	referenceFile=allFilesToStack[len(allFilesToStack)-1]
	#print(referenceFile)
	nameParts=getFileNameParts(referenceFile,"MOD13Q1",".")
	namePartCountryCode=nameParts[1]
	namePartYear=len(nameParts[2])-3
	outputName=nameParts[0]+"."+namePartCountryCode+"."+nameParts[2][:namePartYear]+"."+nameParts[3]+".tif"

	outputFilePath = outDir+"/"+outputName

	tifs = allFilesToStack
	print("FilesToStack:"+str(len(allFilesToStack)))
	outds = gdal.BuildVRT(outvrt, tifs, separate=True)
	print(outputFilePath)
	if outds is None:
		print('Files not found!\n')
	else:
		numberOfRasterBands=outds.RasterCount
		print("NumberRasterbands:"+str(numberOfRasterBands))
		driver = gdal.GetDriverByName('GTiff')
		dataset = driver.Create(outputFilePath,outds.RasterXSize, outds.RasterYSize, 23, gdal.GDT_Int32, options = [ 'COMPRESS=DEFLATE' ])

		i=1
		while i<=numberOfRasterBands:
			dataset.GetRasterBand(i).WriteArray(outds.GetRasterBand(i).ReadAsArray()) 
			i+=1
		dataset.FlushCache()

#----------------------------------------------------------------------------------------------------
from osgeo import gdal
import glob

"""
Create a list of all County ID's represented in this folder
"""

def getCountyIDs(srcFolder=" "):

	if srcFolder==" ":
		globCommand="*.tif"
	else:
		globCommand=srcFolder+"/"+"*.tif"

	allFiles=glob.glob(globCommand)
	allIDS=[]

	for file in allFiles:
		file=file.replace(".tif","")
		nameParts=file.split(".")
		id=nameParts[len(nameParts)-1]

		if id not in allIDS:
			allIDS.append(id)

	return allIDS

#----------------------------------------------------------------------------------------------------
from osgeo import gdal
import glob

"""
Erstellen einer List die alle FilePaths eines Erntejahres für ein bestimmtes County beinhalte, allerdings werden hier die letzten drei bilder weggelassen
"""

#input year set by the year of harvest => harvested in 2017 means year 2017
def getYearData(countyID,year,CountryCode,srcFolder,imagesLess=0):

	selectedYear=year-1
	#reduce year by one to get the data from august - december the year before due to the intervall set from August until Oktober next year.
	daysPerPeriod=["241","257","273","289","305","321","337","353","001","017","033","049","065","081","097","113","129","145","161","177","193","209","225"]

	if(imagesLess != 0):
		daysPerPeriod=daysPerPeriod[:-imagesLess]

	allFiles=[]

	for day in daysPerPeriod:
		if day=="001":
			selectedYear+=1

		fileName="MOD13Q1."+CountryCode+".A"+str(selectedYear)+day+"."+countyID+".tif"

		allFiles.append(srcFolder+"/"+fileName)

	return allFiles

#----------------------------------------------------------------------------------------------------

import glob
import rasterio
import fiona
import csv

"""
alle Labels aus der CSV/Statistik-Files auslesen
#ReferenceData:
#countyRefData(state,county,id,area)
#InputCounties:
#inputCounties(State,Name,Year,Value)
OutputLabels:
#labels(State,Name,ID,Year,Value)
"""

def getLabelsFromCSV(statisticDataPath, shapeFilePath,startYear,endYear, minPercentage=0,printNotFound=False):

	shapeTuples=getDataTuplesFromShapefiles(shapeFilePath)
	print(len(shapeTuples), "shapes")
	csvTuples=getDataTuplesFromCSV(statisticDataPath)
	print(len(csvTuples), "csvtuples")
	labels=mergeShapeCSVTuplesToLabels(shapeTuples,csvTuples,startYear,endYear,printNotFound)
	print("Labels: "+str(len(labels)))
	labels=filterLabels(labels,minPercentage)
	#print("filteredLabels: "+ str(len(labels)))
	return labels

#----------------------------------------------------------------------------------------------------

import glob
import rasterio
import fiona
import csv

"""

"""

def filterLabels(labels,minPercentage):
	filteredLabels=[]

	for label in labels:
		try:
			if(float(str(label[4]))>=minPercentage):
				#print(label)
				filteredLabels.append(label)
		except:
		  print("\nError in Label: \n "+str(label))


	return filteredLabels

#----------------------------------------------------------------------------------------------------
import glob
import fiona
import glob
import rasterio
import fiona
import csv
import sys, os, imp

"""
method: Auslesen der Daten aus der CSV und verpacken in DataTuples
input: csvFilePath: Pfad zur CSV-File
"""

def getDataTuplesFromCSV(csvFilePath):
	csvTuples=[]
	#print("hello you")
	with open(csvFilePath) as csvFile:
		reader = csv.reader(csvFile, delimiter=',')
		startYear=0
		for row in reader:
			if(row[1]=='STATE'):
				startYear=int(row[3])
				continue
			i=0
			while i<len(row)-3:
				year=startYear-i
				country=row[0]
				state=row[1]
				county=row[2]
				areaIndex=i+3
				area=row[areaIndex].replace(",","")
					#if(area!="" and area!="0"):
				if(area!="" and area!="qw"):
					dataTuple=[country,state,county,year,area]
					csvTuples.append(dataTuple)
				i+=1

		return csvTuples
#----------------------------------------------------------------------------------------------------
import glob
import fiona
import glob
import rasterio
import fiona
import csv
import sys, os, imp

"""
method: hier werden aus den Shapefiles die Daten in Tuples verpackt
input: shapeFilePath: Pfad zu den Shapefiles
"""

def getDataTuplesFromShapefiles(shapeFilePath):

	allShapes=glob.glob(shapeFilePath+"/*.shp")
	shapeTuples=[]

	if(len(allShapes)==0):
		print("No Shapesfiles found!!!!")
	else:
		print("allShapes: "+str(len(allShapes)))

	for shape in allShapes:
		countyLevelID=checkCountyLevelID(shape)

		if(countyLevelID=="ID_2"):
			name1='NAME_1'
			name2='NAME_2'
		elif(countyLevelID=="ID_1"):
			name1='NAME_0'
			name2='NAME_1'
		else:
			name1='NAME_2'
			name2='NAME_3'

		selectedShape=fiona.open(shape)
		#Abfrage fall eine Shapefile keine properties hat. Kam in Deutschland vor
		if(selectedShape[0] is None):
			continue

		countyState=selectedShape[0]['properties'][name1].upper()
		countyName=selectedShape[0]['properties'][name2].upper()
		countyID=selectedShape[0]['properties'][countyLevelID]
		countyArea=selectedShape[0]['properties']['AREA']

		dataTuple=(countyState,countyName,countyID,countyArea)
		shapeTuples.append(dataTuple)

	return shapeTuples
#----------------------------------------------------------------------------------------------------
import glob
import fiona
import glob
import rasterio
import fiona
import csv
import sys, os, imp
"""
method: Hier werden die Daten aus der Shapefile ausgelesen und falls vorhanden mit den CSV-Daten zu Trainingslabels verpackt
input: shapeFilePath: Pfad zu den Shapefiles
"""
def mergeShapeCSVTuplesToLabels(shapeTuples,csvTuples,startYear,endYear, printNotFound):

	labels=[]
	notFound=[]
	i=0
	while i<len(csvTuples):
		statsCountry=csvTuples[i][0]
		statsCountyState=csvTuples[i][1]
		statsCountyName=csvTuples[i][2]
		statsYear=csvTuples[i][3]
		statsHarvestedArea=csvTuples[i][4]

		found=False
		for shapeTuple in shapeTuples:
			shapeCountyState=shapeTuple[0]
			shapeCountyName=shapeTuple[1]
			shapeCountyID=shapeTuple[2]
			shapeCountyArea=shapeTuple[3]

			if(shapeCountyName.upper()==statsCountyName.upper()and (statsCountyState.upper()==shapeCountyState.upper() or statsCountyState=="")):
				try:
					statsHarvestedArea=float(statsHarvestedArea)
					shapeCountyArea=float(shapeCountyArea)

					wheatPercentage=(statsHarvestedArea)/(shapeCountyArea)
					if ((int(statsYear) >= startYear) and (int(statsYear) <= endYear)):
						labelTuple=(statsCountyState,statsCountyName.upper(),shapeCountyID,statsYear,wheatPercentage)
						labels.append(labelTuple)

					found=True

				except ValueError:
					print("Invalid value skipped!")
		i+=1
		if(found==False):
			if(statsCountyName.upper() not in notFound):
				notFound.append(statsCountyName.upper())

	if(printNotFound):
		print(notFound)
		print("notFound: "+str(len(notFound)))
	return labels


#----------------------------------------------------------------------------------------------------

import glob
import rasterio
import fiona
import csv

"""
Sammeln aller File-Pfade von Rasterfiles für die es ein Label gibt.

Collecting all file paths of raster files for which there is a label.
"""

def getFilesFromLabels(labels,srcFolder,countryCode):
	orderedLabels=[]
	orderedTraingsdata=[]

	stackedData=glob.glob(srcFolder+"/*.tif")
	stackedData = [s.replace('\\', '/') for s in stackedData]

	#print("***************************************************")
	#print(stackedData)

	for label in labels:

		orderedLabels.append(label[len(label)-1])
		path=srcFolder+"/"+"MOD13Q1."+countryCode+".A"+str(label[3])+"."+str(label[2])+".tif"

		if(path in stackedData):
			#print("holiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii")
			orderedTraingsdata.append(path)
	#print(len(orderedLabels))
	#print(len(orderedTraingsdata))

	return orderedTraingsdata, orderedLabels


#----------------------------------------------------------------------------------------------------

import glob
import rasterio
import fiona
import csv

"""
Erstellen der Inputdaten für die KI.
Erst alles Labels aus der Statistik auslesen. Dannach alle Files zu denen es eine Statistik gibt auslesen.
"""

def getInputData(statisticDataPath, shapeFilePath, rasterSrcFolder,startYear,endYear,countryCode,minPercentage,printNotFoundCountys):


	allLabels=getLabelsFromCSV(statisticDataPath, shapeFilePath,startYear,endYear,minPercentage,printNotFoundCountys)
	#print(allLabels)
	data=getFilesFromLabels(allLabels,rasterSrcFolder,countryCode)

	#print(data)
	traingsdata=data[0]
	#print(traingsdata)
	labels=data[1]
	return traingsdata, labels

#----------------------------------------------------------------------------------------------------
from skimage import io
import numpy as np


def getCDLAverages(validation_data_path):
	allErg=[]
	allErgPath=[]
	for filePath in validation_data_path:
	    im = io.imread(filePath)
	    im[im<0]=0
	    avg=np.average(im)
	    erg=avg/100
	    allErg.append(erg)
	    allErgPath.append(filePath)

	return allErg,allErgPath


#----------------------------------------------------------------------------------------------------
import csv

"""
Schreiben von Ergebnissen in ein CSV
"""

def writeResultCSV(location,header,dataTuple):
	with open(location, 'w', encoding='UTF8',newline='') as f:
		writer = csv.writer(f)

		# write the header
		writer.writerow(header)
		for dataTuple in dataTuple:
			writer.writerow(dataTuple)

#----------------------------------------------------------------------------------------------------

def printStats(diff):
	diffAsNumpy=np.array(diff)
	print('Average delta:'+str(np.average(diffAsNumpy)))
	print('Max delta:'+str(np.amax(diffAsNumpy)))
	print('Min delta:'+str(np.amin(diffAsNumpy)))
	print('')


#----------------------------------------------------------------------------------------------------
import csv
import numpy as np

"""
Schreiben von Predictionsergebnissen in ein CSV
"""

def writePredStatsToCSV(yearDiffs,location):
	yearData=[]
	header=["year","avg","minDiff","maxDiff"]
	for diffs in yearDiffs:
		year=diffs[1]
		diffAsNumpy=np.array(diffs[0])
		avg=(np.average(diffAsNumpy))
		minDiff=(np.amin(diffAsNumpy))
		maxDiff=(np.amax(diffAsNumpy))
		yearData.append((year,avg,minDiff,maxDiff))

	writeResultCSV(location,header,yearData)

#----------------------------------------------------------------------------------------------------
"""
Rasterfile eine neue Projection geben
"""

def array_to_projectedRaster(array, dst_filename, img_width, img_height,transform,wkt_projection,xOffset,yOffset):
    driver = gdal.GetDriverByName('GTiff')

    dataset = driver.Create(
        dst_filename,
        img_width,
        img_height,
        1,
        gdal.GDT_Float32, )


    dataset.SetGeoTransform((
        transform[0]+((xOffset/2)*-231.65635826388908),
        transform[1],
        transform[2],
        transform[3]+((yOffset/2)*231.65635826388908),
        transform[4],
        transform[5]))

    dataset.SetProjection(wkt_projection)
    dataset.GetRasterBand(1).WriteArray(array)
    dataset.FlushCache()

#----------------------------------------------------------------------------------------------------
import sys, os, imp
import rasterio
import numpy as np
from rasterio.transform import from_origin
import glob
from osgeo import gdal
from skimage import io
"""
Setzten der Projection der PredicitonImgs anhand ihrer orginal geclippten Files
"""

def reprojectPredFiles(refFiles,predFiles,outputFolder,countryCode,img_height, img_width):

	print("reproject predImgs...")
	allPredImgs=glob.glob(predFiles+"/"+"*.tif")
	print("PredImgs: "+ str(len(allPredImgs)))
	print(refFiles)
	allClippedRefFiles=glob.glob(refFiles+"/"+"*.tif")
	print("refFiles: "+ str(len(allClippedRefFiles)))

	for predFilePath in allPredImgs:
		predFilePathParts=predFilePath.split(".")
		predCountyID=predFilePathParts[2]
		predYear=predFilePathParts[3]
		predFieldCrop=predFilePathParts[4]
		predModelCode=predFilePathParts[5]
		predImgData=io.imread(predFilePath)

		isChecked=False

		for refFilePath in allClippedRefFiles:

			refFilePathParts=getFileNameParts(refFilePath,"MOD13Q1",".")
			refCountyID=refFilePathParts[3]

			if ((refCountyID==predCountyID) and (isChecked!=True)):
				isChecked=True
				refData=io.imread(refFilePath)
				refDataShape=refData.shape

				xOffset=img_width-refDataShape[1]
				yOffset=img_height-refDataShape[0]

				data=gdal.Open(refFilePath)
				transform=data.GetGeoTransform()
				wkt=data.GetProjectionRef()

				outputFilePath=outputFolder+"/"+"PRED.PRJ."+countryCode+"."+str(predCountyID)+"."+str(predYear)+"."+predFieldCrop+"."+predModelCode+".tif"

				array_to_projectedRaster(predImgData,outputFilePath,img_width,img_height,transform,wkt,xOffset,yOffset)


#----------------------------------------------------------------------------------------------------
import sys, os, imp
from osgeo import gdal
import glob
"""
Clippen der PredImgs anhand ihrer Shapefile um das Padding rund herum zu entfernen
"""

def clipPredFiles(predReprojectFiles,outputFolder,shapeFiles):

	print("clip predImgs ...")

	filesToClip=glob.glob(predReprojectFiles+"/"+"*.tif")
	allShapeFiles=glob.glob(shapeFiles+"/"+"*.shp")
	print(predReprojectFiles)
	print(shapeFiles)
	print("filesToClip: "+str(len(filesToClip)))
	print("shapeFiles:" +str(len(allShapeFiles)))

	for rasterFile in filesToClip:
		print(rasterFile)
		fileNameParts=getFileNameParts(rasterFile,"PRED.PRJ",".")
		countyID=fileNameParts[3]
		countyLevelID=checkCountyLevelIDFromID(countyID,shapeFiles)
		year=fileNameParts[4]
		countryCode=fileNameParts[2]
		fieldCrop=fileNameParts[5]
		modelCode=fileNameParts[6]
		selectedShapeFile=shapeFiles+"/"+countyLevelID+"_"+str(countyID)+".shp"
		print(selectedShapeFile)

		ds=gdal.Open(rasterFile)
		outputPath=outputFolder+"/PRED."+countryCode+"."+str(countyID)+"."+str(year)+"."+fieldCrop+"."+modelCode+".tif"
		print(outputPath)
		gdal.Warp(outputPath,ds,cutlineDSName=selectedShapeFile,cropToCutline=True, dstNodata=-1)

#----------------------------------------------------------------------------------------------------
import time
import sys, os, imp
import glob
from osgeo import gdal

"""
method:
Zusammensetzen aller PredImgs zu einem gesamten Bild
input:
clippedPredImgs: Ordner in dem die geclippten PredImgs liegen
outputFolder: Ordner in dem die gemergete File abgelegt werden soll
areaCode:Hier konnen Kürzel bezüglich des abgedecketen Gebiets gemacht werden, welche im Dateinname auftauchen

"""

def mergePredFiles(clippedPredImgs,outputFolder,areaCode=""):

	print("merge predImgs ...")

	fileYears=getFileYears(clippedPredImgs)

	for fileYear in fileYears:

		allReprojectFiles=glob.glob(clippedPredImgs+"/*"+fileYear+"*.tif")
		print(fileYear+": "+str(len(allReprojectFiles)))

		outvrt = '/vsimem/merge.vrt' #/vsimem is special in-memory virtual "directory"

		fileName=allReprojectFiles[0]
		nameParts=getFileNameParts(fileName,"PRED",".")
		countyID=nameParts[2]
		year=nameParts[3]
		countryCode=nameParts[1]
		fieldCrop=nameParts[4]
		modelCode=nameParts[5]

		if areaCode=="":
			finalName="PRED."+countryCode+"."+str(year)+"."+fieldCrop+"."+modelCode+".tif"
		else:
			finalName="PRED."+countryCode+"."+areaCode+"."+str(year)+"."+fieldCrop+"."+modelCode+".tif"

		outtif=outputFolder+"/"+finalName
		outds = gdal.BuildVRT(outvrt, allReprojectFiles, separate=False)
		outds = gdal.Translate(outtif, outds)

#----------------------------------------------------------------------------------------------------
import time
import sys, os, imp
import glob
from osgeo import gdal

"""
Hier werden alle auftretenden Jahre der PredImgs gefiltert
"""

def getFileYears(srcFolder):
	allFiles=glob.glob(srcFolder+"/*.tif")
	allYears=[]

	for filePath in allFiles:
		fileNameParts=getFileNameParts(filePath,"PRED",".")
		year=fileNameParts[3]
		if year not in allYears:
			allYears.append(year)

	print(allYears)

	return allYears

#----------------------------------------------------------------------------------------------------

"""
method:
Ausgabe der Vorhersagedaten eines Jahres
"""

def printPredictionSummary(predictionDataSum, amountPredictions,year):


	avgDelta=predictionDataSum/amountPredictions
	print("---------------------------------------")
	print("Year: "+str(year))
	print("AVG-Pred-Delta: "+ str(avgDelta))
	print("Number of Predictions: " + str(amountPredictions))
	print("---------------------------------------")

#----------------------------------------------------------------------------------------------------

"""
method:
Aufteilen der Fliename in unterschiedliche Teile
input:
filePath: der Filepfad in dem der Name gesucht wird
fileType: Typ der File (z.B: MOD13Q1)
splitChar: zeichen an dem der Name getrennt werden soll (meisten ".")
"""

def getFileNameParts(filePath, fileType ,splitChar):
	index=filePath.find(fileType)
	fileName=filePath[index:]
	fileNameParts=fileName.split(splitChar)
	return fileNameParts


#----------------------------------------------------------------------------------------------------

"""
method:
Erkennen welches ID Level die Shapefile in GDAM hat
input:
filePathShape: Pfad zur entsprechenden Shapefile
"""

def checkCountyLevelID(filePathShape):
	index=filePathShape.find("ID_")
	countyLevelID=filePathShape[index:index+4]
	return countyLevelID

#----------------------------------------------------------------------------------------------------
"""
method:
Erkennen welches ID Level die Shapefile in GDAM hat basierend auf der CountyID
input:
countyID: ID des gesuchten Countys
filePathShape: Pfad zu den verwendeten Shapefiles
"""
def checkCountyLevelIDFromID(countyID,shapes):
	allShapes=glob.glob(shapes+"/*.shp")
	#print("allShapes:" + str(len(allShapes)))
	for shape in allShapes:
		#print(shape)
		if countyID in shape:
			return checkCountyLevelID(shape)
	return ""

#----------------------------------------------------------------------------------------------------
"""
method:
Sammeln aller Predfiles anhand der Shapefiles
input:
countyID: ID des gesuchten Countys
filePathShape: Pfad zu den verwendeten Shapefiles
"""
def getPredDataFromShapes(shapes,stackedFiles,countryCode,pred_startyear):
	allShapes=glob.glob(shapes+"/*.shp")
	if len(allShapes)==0:
		print("No Shapefiles found !!!")
	predData=[]

	for shape in allShapes:
		index=shape.find("ID_")
		shapeID=shape[index+5:].replace(".shp","")
		predData.append(stackedFiles+"/MOD13Q1."+countryCode+".A"+str(pred_startyear)+"."+shapeID+".tif")
	return predData
