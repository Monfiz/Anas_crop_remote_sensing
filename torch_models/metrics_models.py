

from skimage import io
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.image

#libraries 
import numpy as np
import time
import sys, os, imp
import glob
#from osgeo import gdal
from PIL import Image
import matplotlib.pyplot as plt
import time

def mse_eval_CDL(folder_pred):
    """
    Takes folders with targets and predictions and compers them
    with MSE. Only taking into account the pixels with value of interest,
    ignoring the padding.
    """
    
    predicted_files=glob.glob(folder_pred+"/*.tif")#finds all the files predicted
    predicted_files = [s.replace('\\', '/') for s in predicted_files] #just in case windows do wierd stuff with paths
    print("all filles:", len(predicted_files))
    generic_route = "Preprocessing/CDL/cdl_pad_original/original_paded.CDLr.2019.US.US262.tif"#fro finding targets
    w = generic_route.split(".") 
    
    mse_list = [] 
    for file in predicted_files:      
        q = file.split(".")
        #here we find match the corresponding file target-prediction
        target_route = w[0]+ "." + w[1]+ "." + q[1][1:] + "." + w[3] +"."+q[2] + ".tif"
        #red images as np arrays
        img_pred = io.imread(file)
        img_orig = io.imread(target_route)
        #create mask to take into account only no pad values
        mask = np.where(img_orig == -1, 0., 1.)
        #apply mask to both 
        pred = img_pred*mask
        origin = img_orig*mask
        #compute mse
        mse = ((pred - origin)**2).sum()/mask.sum()#average between the true values 
        mse_list.append(mse)
        
    return mse_list

def mse_eval_CDLcal(folder_pred):
    """
    Takes folders with targets and predictions and compers them
    with MSE. Only taking into account the pixels with value of interest,
    ignoring the padding.
    """
    
    predicted_files=glob.glob(folder_pred+"/*.tif")#finds all the files predicted
    predicted_files = [s.replace('\\', '/') for s in predicted_files] #just in case windows do wierd stuff with paths
    print("all filles:", len(predicted_files))
    generic_route = "Preprocessing/CDL/cdl_pad_calibrated/resh.CDLr.2019.US.US262.tif"#fro finding targets
    w = generic_route.split(".") 
    
    mse_list = [] 
    for file in predicted_files:      
        q = file.split(".")
        #here we find match the corresponding file target-prediction
        target_route = w[0]+ "." + w[1]+ "." + q[1][1:] + "." + w[3] +"."+q[2] + ".tif"
        #red images as np arrays
        img_pred = io.imread(file)
        img_orig = io.imread(target_route)
        #create mask to take into account only no pad values
        mask = np.where(img_orig == -1, 0., 1.)
        #apply mask to both 
        pred = img_pred*mask
        origin = img_orig*mask
        #compute mse
        mse = ((pred - origin)**2).sum()/mask.sum()#average between the true values 
        mse_list.append(mse)
        if mse > 1:
            print(file, target_route)
        
    return mse_list


def mse_eval_CDL_North(folder_pred):
    """
    Takes folders with targets and predictions and compers them
    with MSE. Only taking into account the pixels with value of interest,
    ignoring the padding.
    """
    
    predicted_files=glob.glob(folder_pred+"/*.tif")#finds all the files predicted
    predicted_files = [s.replace('\\', '/') for s in predicted_files] #just in case windows do wierd stuff with paths
    print("all filles:", len(predicted_files))
    generic_route = "Preprocessing/CDL/cdl_pad_original_north/original_paded.CDLr.2019.US.US262.tif"#fro finding targets
    w = generic_route.split(".") 
    
    mse_list = [] 
    for file in predicted_files:      
        q = file.split(".")
        #here we find match the corresponding file target-prediction
        target_route = w[0]+ "." + w[1]+ "." + q[1][1:] + "." + w[3] +"."+q[2] + ".tif"
        #red images as np arrays
        img_pred = io.imread(file)
        img_orig = io.imread(target_route)
        #create mask to take into account only no pad values
        mask = np.where(img_orig == -1, 0., 1.)
        #apply mask to both 
        pred = img_pred*mask
        origin = img_orig*mask
        #compute mse
        mse = ((pred - origin)**2).sum()/mask.sum()#average between the true values 
        mse_list.append(mse)
        
    return mse_list


def mse_eval_NASS(folder_pred, B_list):
    """
    Takes folders with targets and predictions and compers them
    with MSE. Only taking into account the pixels with value of interest,
    ignoring the padding.
    """
    
    predicted_files=glob.glob(folder_pred+"/*.tif")#finds all the files predicted
    predicted_files = [s.replace('\\', '/') for s in predicted_files] #just in case windows do wierd stuff with paths
    print("all filles:", len(predicted_files))
    generic_route = 'Preprocessing/modis/modis_TorchPoints/MODIS_torch.US.A2020.US245.pt'#fro finding targets
    generic_route_2 = "Preprocessing/CDL/cdl_pad_original/original_paded.CDLr.2019.US.US262.tif"
    generic_route = generic_route.split(".") 
    generic_route_2 = generic_route_2.split(".")
    
    mse_list = [] 
    for file in predicted_files:      
        fi = file.split(".")
        #here we find match the corresponding file target-prediction
        target = generic_route[0] + "." + generic_route[1] + "." + fi[1] + "." + fi[2] + ".pt" 
        #find position in list
        index = B_list[0].index(target)
        #find NASS percentage:
        NASS = B_list[2][index]
        
        #Find CDL target just to get the mask:
        target_route = generic_route_2[0]+ "." + generic_route_2[1]+ "." + fi[1][1:] + "." + generic_route_2[3] +"."+fi[2] + ".tif"
        #print(target_route)
        img_orig = io.imread(target_route)
        mask = np.where(img_orig == -1, 0., 1.)
        
        
        #red images as np arrays
        img_pred = io.imread(file)
        #apply mask 
        pred = img_pred*mask
        average_pred = pred.sum()/mask.sum()
        
        #compute mse
        mse = (average_pred - NASS)**2
        mse_list.append(mse)
        
    return mse_list

def mse_eval_NASS_North(folder_pred, B_list):
    """
    Takes folders with targets and predictions and compers them
    with MSE. Only taking into account the pixels with value of interest,
    ignoring the padding.
    """
    
    predicted_files=glob.glob(folder_pred+"/*.tif")#finds all the files predicted
    predicted_files = [s.replace('\\', '/') for s in predicted_files] #just in case windows do wierd stuff with paths
    print("all filles:", len(predicted_files))
    generic_route = 'Preprocessing/modis/modis_TorchPoints/MODIS_torch.US.A2020.US245.pt'#fro finding targets
    generic_route_2 = "Preprocessing/CDL/cdl_pad_original_north/original_paded.CDLr.2019.US.US262.tif"
    generic_route = generic_route.split(".") 
    generic_route_2 = generic_route_2.split(".")
    
    mse_list = [] 
    for file in predicted_files:      
        fi = file.split(".")
        #here we find match the corresponding file target-prediction
        target = generic_route[0] + "." + generic_route[1] + "." + fi[1] + "." + fi[2] + ".pt" 
        #find position in list
        index = B_list[0].index(target)
        #find NASS percentage:
        NASS = B_list[2][index]
        
        #Find CDL target just to get the mask:
        target_route = generic_route_2[0]+ "." + generic_route_2[1]+ "." + fi[1][1:] + "." + generic_route_2[3] +"."+fi[2] + ".tif"
        #print(target_route)
        img_orig = io.imread(target_route)
        mask = np.where(img_orig == -1, 0., 1.)
        
        
        #red images as np arrays
        img_pred = io.imread(file)
        #apply mask 
        pred = img_pred*mask
        average_pred = pred.sum()/mask.sum()
        
        #compute mse
        mse = (average_pred - NASS)**2
        mse_list.append(mse)
        
    return mse_list

def acurracy_eval(folder_pred, threshold ):
    """
    Takes folders predictions, resiagns 0 or 1 to pixels acording to threshold
    and evaluates the overall acurracy of prediction and target.
    """
    
    predicted_files=glob.glob(folder_pred+"/*.tif")#finds all the files predicted
    predicted_files = [s.replace('\\', '/') for s in predicted_files] #just in case windows do wierd stuff with paths
    #print("all filles:", len(predicted_files))
    generic_route = "Preprocessing/CDL/cdl_pad_original/original_paded.CDLr.2019.US.US262.tif"#fro finding targets
    w = generic_route.split(".") 
    
    ac_list = [] 
    for file in predicted_files:      
        q = file.split(".")
        #here we find match the corresponding file target-prediction
        target_route = w[0]+ "." + w[1]+ "." + q[1][1:] + "." + w[3] +"."+q[2] + ".tif"
        #red images as np arrays
        img_pred = io.imread(file)
        img_orig = io.imread(target_route)
        #create mask to take into account only no pad values
        mask = np.where(img_orig == -1, 0., 1.)
        #apply mask to both 
        pred = img_pred*mask
        origin = img_orig*mask
        #reasign 0 or 1 according to threshold
        pred_A = np.where(pred<=threshold, 0., 1.)
        origin_A = np.where(origin<=threshold, 0., 1.) 
        #compute acurracy
        x = abs(pred_A - origin_A)
        acurracy = 1 - x.sum()/mask.sum() 
        ac_list.append(acurracy)
        
    return ac_list

def Acurracy_thresholds(folder_predictions, list_thresholds):
    """Calculates average acurracy in different thresholds"""
    average_acurracys = []
    
    for threshold in list_thresholds:
        ac = acurracy_eval(folder_predictions, threshold)
        average_acurracys.append(np.mean(ac))
        
    return average_acurracys



def f1_score(folder_pred, threshold ):
    """
    Takes folders with predictions and returns list of scores
    of image comparation:
    -acurracy
    -precision
    -recall
    -f1
    """
    
    predicted_files=glob.glob(folder_pred+"/*.tif")#finds all the files predicted
    predicted_files = [s.replace('\\', '/') for s in predicted_files] #just in case windows do wierd stuff with paths
    print("all filles:", len(predicted_files))
    generic_route = "Preprocessing/CDL/cdl_pad_original/original_paded.CDLr.2019.US.US262.tif"#fro finding targets
    w = generic_route.split(".") 
    
    acurracy_list = [] 
    precision_list = []
    recall_list = []
    f1_list = []
    
    for file in predicted_files:      
        q = file.split(".")
        #here we find match the corresponding file target-prediction
        target_route = w[0]+ "." + w[1]+ "." + q[1][1:] + "." + w[3] +"."+q[2] + ".tif"
        #red images as np arrays
        img_pred = io.imread(file)
        img_orig = io.imread(target_route)
        #create mask to take into account only no pad values
        mask = np.where(img_orig == -1, 0., 1.)
        #apply mask to both 
        pred = img_pred*mask
        origin = img_orig*mask
        #reasign 0 or 1 according to threshold
        pred_A = np.where(pred<=threshold, 1, 3)
        origin_A = np.where(origin<=threshold, 0., 1.) 
        #compute acurracy
        x = pred_A - origin_A


        #find num true positives, true neg, false pos, false neg
        #2 true positives
        #3 flase positives
        #0 false negatives 
        #1 true negatives 
        tp = (np.where(x == 2., 1., 0.)*mask).sum()
        tn = (np.where(x == 1., 1., 0.)*mask).sum()
        fp = (np.where(x == 3., 1., 0.)*mask).sum()
        fn = (np.where(x == 0., 1., 0.)*mask).sum()
        
        acurracy = (tp+tn)/(tp+tn+fp+fn)
        precision = tp/(tp+fp)
        recall = tp/(tp+fn)
        if precision+recall != 0:
            f1 = ((2 *precision*recall)/(precision+recall))
            f1_list.append(f1)
            
        acurracy_list.append(acurracy)
        precision_list.append(precision)
        recall_list.append(recall)
        
        
    return acurracy_list, precision_list, recall_list, f1_list

def f1_score_cal(folder_pred, threshold ):
    """
    Takes folders with predictions and returns list of scores
    of image comparation:
    -acurracy
    -precision
    -recall
    -f1
    """
    
    predicted_files=glob.glob(folder_pred+"/*.tif")#finds all the files predicted
    predicted_files = [s.replace('\\', '/') for s in predicted_files] #just in case windows do wierd stuff with paths
    print("all filles:", len(predicted_files))
    generic_route = "Preprocessing/CDL/cdl_pad_calibrated/resh.CDLr.2019.US.US262.tif"#fro finding targets
    w = generic_route.split(".") 
    
    acurracy_list = [] 
    precision_list = []
    recall_list = []
    f1_list = []
    
    for file in predicted_files:      
        q = file.split(".")
        #here we find match the corresponding file target-prediction
        target_route = w[0]+ "." + w[1]+ "." + q[1][1:] + "." + w[3] +"."+q[2] + ".tif"
        #red images as np arrays
        img_pred = io.imread(file)
        img_orig = io.imread(target_route)
        #create mask to take into account only no pad values
        mask = np.where(img_orig == -1, 0., 1.)
        #apply mask to both 
        pred = img_pred*mask
        origin = img_orig*mask
        #reasign 0 or 1 according to threshold
        pred_A = np.where(pred<=threshold, 1, 3)
        origin_A = np.where(origin<=threshold, 0., 1.) 
        #compute acurracy
        x = pred_A - origin_A




        #find num true positives, true neg, false pos, false neg
        #2 true positives
        #3 flase positives
        #0 false negatives 
        #1 true negatives 
        tp = (np.where(x == 2., 1., 0.)*mask).sum()
        tn = (np.where(x == 1., 1., 0.)*mask).sum()
        fp = (np.where(x == 3., 1., 0.)*mask).sum()
        fn = (np.where(x == 0., 1., 0.)*mask).sum()
        
        acurracy = (tp+tn)/(tp+tn+fp+fn)
        precision = tp/(tp+fp)
        recall = tp/(tp+fn)
        if precision+recall != 0:
            f1 = ((2 *precision*recall)/(precision+recall))
            f1_list.append(f1)
            
        acurracy_list.append(acurracy)
        precision_list.append(precision)
        recall_list.append(recall)
        
        
    return acurracy_list, precision_list, recall_list, f1_list

print("holis adios")

def f1_score_North(folder_pred, threshold ):
    """
    Takes folders with predictions and returns list of scores
    of image comparation:
    -acurracy
    -precision
    -recall
    -f1
    """
    
    predicted_files=glob.glob(folder_pred+"/*.tif")#finds all the files predicted
    predicted_files = [s.replace('\\', '/') for s in predicted_files] #just in case windows do wierd stuff with paths
    print("all filles:", len(predicted_files))
    generic_route = "Preprocessing/CDL/cdl_pad_original_north/original_paded.CDLr.2019.US.US262.tif"#fro finding targets
    w = generic_route.split(".") 
    
    acurracy_list = [] 
    precision_list = []
    recall_list = []
    f1_list = []
    
    for file in predicted_files:      
        q = file.split(".")
        #here we find match the corresponding file target-prediction
        target_route = w[0]+ "." + w[1]+ "." + q[1][1:] + "." + w[3] +"."+q[2] + ".tif"
        #red images as np arrays
        img_pred = io.imread(file)
        img_orig = io.imread(target_route)
        #create mask to take into account only no pad values
        mask = np.where(img_orig == -1, 0., 1.)
        #apply mask to both 
        pred = img_pred*mask
        origin = img_orig*mask
        #reasign 0 or 1 according to threshold
        pred_A = np.where(pred<=threshold, 1, 3)
        origin_A = np.where(origin<=threshold, 0., 1.) 
        #compute acurracy
        x = pred_A - origin_A
        
        #find num true positives, true neg, false pos, false neg
        #2 true positives
        #3 flase positives
        #0 false negatives 
        #1 true negatives 
        tp = (np.where(x == 2., 1., 0.)*mask).sum()
        tn = (np.where(x == 1., 1., 0.)*mask).sum()
        fp = (np.where(x == 3., 1., 0.)*mask).sum()
        fn = (np.where(x == 0., 1., 0.)*mask).sum()
        
        acurracy = (tp+tn)/(tp+tn+fp+fn)
        precision = tp/(tp+fp)
        recall = tp/(tp+fn)
        if precision+recall != 0:
            f1 = ((2 *precision*recall)/(precision+recall))
            f1_list.append(f1)
            
        acurracy_list.append(acurracy)
        precision_list.append(precision)
        recall_list.append(recall)
        
        
    return acurracy_list, precision_list, recall_list, f1_list

def rmse(list_mse):
    percent_list = []

    for i in list_mse:
        percent_list.append(np.sqrt(i))

    return percent_list

def rmse_in(list_mse):
    percent_list = []

    for i in list_mse:
        percent_list.append(1 - np.sqrt(i))
        
    return percent_list
