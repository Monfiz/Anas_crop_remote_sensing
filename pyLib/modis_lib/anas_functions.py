#Anas fuctions
from PIL import Image
import numpy as np
import glob
from osgeo import gdal
import rasterio
import tifffile 
import torch
from skimage import io
########## Lutz fuctions:
"""
method:
Recognize which ID level the shapefile has in GDAM
input:
filePathShape: Path to the corresponding shapefile
"""

def checkCountyLevelID(filePathShape):
	index=filePathShape.find("ID_")
	countyLevelID=filePathShape[index:index+4]
	return countyLevelID
######################


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



def clipData_CDL(shapesFolderPath, rasterFile, dest_FolderPath,countryCode=""):
    """
    This fuction takes a layer, shape files and clips the files
    Takes as input:
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
        dsClip=gdal.Warp(outputPath,ds,cutlineDSName=countyShapePath,cropToCutline=True, dstNodata=-1)#try NA=0
        #assignment of -1 to NAs, this convention will continue

def CDL_clip_stats(countie_stats, data_clipped ,countryCode):
    """
    This fuction tupples CDLclipped files with their corresponding NASS statistics
    Takes as input:
    - county_stats: list of counties and statistics
    - data_clipped: folder with CDL clip
    - countryCode: just to give name to files

    returns:
    Two lists one with the CDL and other with the corresponding statistics
    """
    CDLclip=[]
    stats=[]

    clipData=glob.glob(data_clipped+"/*.tif") #serch all CDLclip files
    clipData = [s.replace('\\', '/') for s in clipData] #just in case name is bad writen by windows

    for countie in countie_stats:
        CDLclip.append(countie[len(countie)-1]) #adds the CDLcounty into the list
        #path vriable is used to find coincidences between the statistics file and the CDLclip files
        path=data_clipped+"/"+"CDLr."+str(countie[3])+"."+countryCode+"."+str(countie[2])+".tif"

        if(path in clipData):
            #if the coincidence exist then it gets writen
            stats.append(path)

    return stats, CDLclip

from PIL import Image

def calibrate_CDL(files_persent, folder_calibrated):
    """This fuction takes a double list of files to calibrate with their correct % of coverage
       and saves the calibrated images in the folder provided.
       Input:
       - files_persent: double list of CDLresized and the corresponding NASS statistic
       - folder_calibrated: folder to save the output

       Output:
       - cons: list of constants of calibration
       - original_persent: list of the NASS percentages
       - cdl_percent: list of the CDL perecentages before calibration and before normalization
       - cdl_percent_norm: list of the CDL perecentages before calibration and after normalization
       - dif: list with the subrtrction of NASS%-CDLcalibrated to check that the calibration worked
       - average_cdl_prev: average of CDLcalibrated before returning NAvalues
       - average_cdl_post average of CDLcalibrated after returning NAvalues

       """
    cons = [] #list of constants
    original_persent = []  #list of percentage stats
    cdl_percent = []
    cdl_percent_norm = []
    #w = []
    dif = []
    print("chavacanooooooo :)")
    average_cdl_prev = [] #prev to -1 assing to NAs
    average_cdl_post = [] #post
    for i in range(len(files_persent[0])):
        original_persent.append(files_persent[1][i])#save nass percent
        cdl = tifffile.imread(files_persent[0][i]) #open a picture
        #cdl = np.array(p) #trasform it to np array

        #cdl[cdl < 0] = -1 #!!! Fixe weird values made by gdal

        #cdl[cdl < 0] = np.nan #trasfrom -1 values to NA
        cdl[cdl < 0] = np.nan
        por = np.nanmean(cdl)
        cdl_percent.append(por)
        por = por#*0.01 #calculate persentage of CDL, by 0.01 to have values in rage[0,1]
        cdl_percent_norm.append(por)
        x = files_persent[1][i]/por #calculate constant of calibration (true value/cdl value)
        cons.append(x) #save constant in list for statistics propuses

        #calibration:
        calibrated_cdl = cdl*x #multiply array by cosntant of calibration
        cld_prev = np.nanmean(calibrated_cdl) #again nomalize by *0.01 ("cdl" was not normalized)
        average_cdl_prev.append(cld_prev)#save before adding NAs

        calibrated_cdl = np.nan_to_num(calibrated_cdl ,nan=-1)#return to -1 nan values because of convention    quitamos calibrated_cdl*0.01
        average_cdl_post.append(np.nanmean(calibrated_cdl))

        diference = cld_prev - files_persent[1][i]
        if diference < 0.00001:
            dif.append(0)
        else:
            dif.append("error in difference")#in case somthing is wrong this will show up

        #now we save the np array in atext file in the route provided
        nom = files_persent[0][i][:] #take parts of the name
        nom = nom.split(".")
        output_name = "/calib_CDLr." + nom[1] + "." + nom[2] + "." + nom[3] + ".txt"
        out = folder_calibrated + output_name
        np.savetxt(out, calibrated_cdl)


    print("Done :)")
    return cons, original_persent, cdl_percent, cdl_percent_norm , dif, average_cdl_prev, average_cdl_post



def getMaxFileSizeAuto_CDL(srcFolder=" "):
	"""
	This fuction takes a folder with .tiff files, messures their high and width
	and returns the maximum of this messurments
	"""

	print("Check max Filesize")
	maxWidth=0
	maxHeight=0

	if srcFolder==" ":
		globCommand="*.tif"
	else:
		globCommand=srcFolder+"/"+"*.tif"

	allFiles=glob.glob(globCommand)
	refFile=allFiles[0]
	index=refFile.find("CDLr")
	refFileName=refFile[index:]
	refFileNameParts=refFileName.split(".")
	#print(refFileNameParts)
	year=refFileNameParts[1]

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


def cdl_pad(in_route, out_route, x, y):
    """
    This fuction takes one folder with files, resize them into the size(x,y)
    and write the output in the other provided folder
    Input:
    - in_route: folder with files to transform
    - out_route: folder to write files
    - x: size of new width
    - y: size of new high
    """
    
    allFiles=glob.glob(in_route+"/*.txt")#finds all the files to reshape
    allFiles = [s.replace('\\', '/') for s in allFiles] #just in case windows do wierd stuff with paths
    print("all filles:", len(allFiles))

    for i in allFiles:
        cdl = np.loadtxt(i) #load file
        cdl = padding(cdl, x, y)#reshape it
        cdl = cdl.reshape((1,x,y)) #to match torch convention (chanel,high,width)
        #print(cdl.shape)
        index=i.find("CDLr") ## give it a new name
        re=i[index:]
        re=re.split(".")

        outname = "resh." +re[0]+"."+re[1]+"." + re[2]+"."+re[3]
        cdl_torch = torch.from_numpy(cdl)

        torch.save(cdl_torch, out_route + "/" + outname + ".pt")
        #np.savetxt(out_route + "/" + outname  , a) #save it
    print("Done pytorch!")



def getFilesFromLabels_trianingCDL(counties, stacked_data, data_reshaped ,countryCode):
    """
    This function takes a list of counties in different years with their
    corresponding value of coverage%, and folders to look for coincidences.
    If the files are found it returns lists with the data in ordered (train, target, coverage %).

    Input:
    - counties: list of counties in different years with their corresponding value of coverage%
    - stacked_data: path to folder with the syaked data (train)
    - data_reshaped: path to folder with data reshaped (target)
    - countryCode: name, just to asign references

    Output:
    - tuple with list ordered data: orderedTraingsdata, orderedTarget, orderedPerscentages

    """
    orderedPerscentages=[]
    orderedTraingsdata=[]
    orderedTarget=[]

    #find staked files in folder (traning points)
    stackedData=glob.glob(stacked_data+"/*.tif")
    stackedData = [s.replace('\\', '/') for s in stackedData]

    #find reshaped files in folder (target)
    reshaaa = glob.glob(data_reshaped+"/*.txt")
    reshaaa = [s.replace('\\', '/') for s in reshaaa]

    for countie in counties:
        #define name for searching files coincidences
        path=stacked_data +"/"+"MOD13Q1."+countryCode+".A"+str(countie[3])+"."+str(countie[2])+".tif"
        path_target=data_reshaped+"/"+"resh.CDLr."+str(countie[3])+"."+countryCode+"."+str(countie[2])+".txt"

        #if both files exist(trainig and target) they get added to their respective list
        if(path in stackedData):
            orderedTraingsdata.append(path)
        if(path_target in reshaaa):
            orderedPerscentages.append(countie[len(countie)-1]) #takes the percentage
            orderedTarget.append(path_target)

    return orderedTraingsdata, orderedTarget, orderedPerscentages

def normalization_min_max(array, a_min = -20000000, a_max=100000000):
    """
    Takes an array and normalize its values to give an output 
    with elements between 0 and 1. 
    """
    array_resc = (array-a_min)/(a_max -a_min)
    
    return array_resc

def MODIS_points2(in_folder, out_folder):
    """Tkes a folder with stacked modis data in .tif and retuns
       the same staked data but as tensors for pytorch and saved 
       as .pt with the correct dimensions in the out_folder"""
    
    stackedData=glob.glob(in_folder+"/*.tif")
    stackedData = [s.replace('\\', '/') for s in stackedData]
    
    for file in stackedData:
        #prepare output name:
        ll = file.split(".")
        name = "MODIS_torch." + ll[1] + "." + ll[2]+"."+ll[3]
        name_path = out_folder + '/' + name + ".pt"
        print(name_path )
        #transform modis:
        modis = io.imread(file) #read tif file into np array
        
        modis = np.transpose(modis, (2,0,1))
        modis = modis.reshape((1,modis.shape[0],modis.shape[1],modis.shape[2]))
        #modis = modis.reshape((1,modis.shape[2],modis.shape[0],modis.shape[1])) #fit pytorch demands torch.nn.Conv3d N,C,D,H,W
        modis_torch = torch.from_numpy(modis)
        torch.save(modis_torch, name_path) 

#print("helo")

def getFilesFromLabels_data_points(counties, stacked_data, data_reshaped ,countryCode):
    """
    This function takes a list of counties in different years with their
    corresponding value of coverage%, and folders to look for coincidences.
    If the files are found it returns lists with the data in ordered (train, target, coverage %).

    Input:
    - counties: list of counties in different years with their corresponding value of coverage%
    - stacked_data: path to folder with the syaked data (train)
    - data_reshaped: path to folder with data reshaped (target)
    - countryCode: name, just to asign references

    Output:
    - tuple with list ordered data: orderedTraingsdata, orderedTarget, orderedPerscentages

    """
    orderedPerscentages=[]
    orderedTraingsdata=[]
    orderedTarget=[]

    #find staked files in folder (traning points)
    stackedData=glob.glob(stacked_data+"/*.pt")
    stackedData = [s.replace('\\', '/') for s in stackedData]
    
    #find reshaped files in folder (target)
    reshaaa = glob.glob(data_reshaped+"/*.pt")
    reshaaa = [s.replace('\\', '/') for s in reshaaa]
    
    for countie in counties:
        #define name for searching files coincidences
        path=stacked_data +"/"+"MODIS_torch."+countryCode+".A"+str(countie[3])+"."+str(countie[2])+".pt"
        path_target=data_reshaped+"/"+"resh.CDLr."+str(countie[3])+"."+countryCode+"."+str(countie[2])+".pt"
        #print(path_target)

        #if both files exist(trainig and target) they get added to their respective list
        if(path in stackedData):
            orderedTraingsdata.append(path)
        if(path_target in reshaaa):
            orderedPerscentages.append(countie[len(countie)-1]) #takes the percentage
            orderedTarget.append(path_target)

    return orderedTraingsdata, orderedTarget, orderedPerscentages



def read_lits(l0,l1,l2):
    """recives 3 files with lists
    return a triple list with the lists"""
    
    # empty list to read list from a file
    b0 = []
    b1 = []
    b2 = []
    # open file and read the content in a list
    with open(l0, 'r') as fp:
        for line in fp:
            # remove linebreak from a current name
            # linebreak is the last character of each line
            x = line[:-1]
            # add current item to the list
            b0.append(x)

    with open(l1, 'r') as fp:
        for line in fp:
            x = line[:-1]
            b1.append(x)

    with open(l2, 'r') as fp:
        for line in fp:
            x = line[:-1]
            b2.append(float(x))
    B2 = [b0, b1, b2]
    return B2

def cdl_pad_original(in_route, out_route, x, y):
    """
    This fuction takes one folder with files, resize them into the size(x,y)
    and write the output in the other provided folder
    Input:
    - in_route: folder with files to transform
    - out_route: folder to write files
    - x: size of new width
    - y: size of new high
    """
    
    allFiles=glob.glob(in_route+"/*.tif")#finds all the files to reshape
    allFiles = [s.replace('\\', '/') for s in allFiles] #just in case windows do wierd stuff with paths
    print("all filles:", len(allFiles))

    for i in allFiles:
        cdl = io.imread(i) #load file
        cdl = padding(cdl, x, y)#reshape it
        #print(cdl.min())
        #cdl = cdl.reshape((1,x,y)) #to match torch convention (chanel,high,width)
        #print(cdl.shape)
        index=i.find("CDLr") ## give it a new name
        re=i[index:]
        re=re.split(".")

        outname = out_route + "/original_paded." +re[0]+"."+re[1]+"." + re[2]+"."+re[3] +".tif"
        
        cdl = Image.fromarray(cdl)
        cdl.save(outname)
        #matplotlib.image.imsave(outname, cdl)
    print("Done cdl!")
