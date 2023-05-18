#libreries
import torch
import torchvision 
from torch.utils.data import Dataset 
from torch.utils.data import DataLoader
import numpy as np 
import torch 
import torch.nn as nn
import torchvision.transforms as transforms
import matplotlib.pyplot as plt
import torch.nn.functional as F

import matplotlib.pyplot as plt
from torch.utils.tensorboard import SummaryWriter
import time 
from PIL import Image
import modis_read 
from data_generator import Crop_Generator
import Crop_Models as CM 

At = modis_read.read_modis_original('lists_data/list_A_0.txt', 'lists_data/list_A_1.txt', 'lists_data/list_A_2.txt')
A_temporal = At[0]

As = modis_read.read_modis_original('lists_data/list_A_0.txt', 'lists_data/list_A_1.txt', 'lists_data/list_A_2.txt')
A_spatial = As[0]
#test set files

Bt = modis_read.read_modis_original('lists_data/B_temp_0.txt', 'lists_data/B_temp_1.txt', 'lists_data/B_temp_2.txt')
B_temporal = Bt[0]


Bb2 = modis_read.read_modis_original('lists_data/list_B_0.txt', 'lists_data/list_B_1.txt', 'lists_data/list_B_2.txt')
B_spatial = Bb2[0]

if torch.cuda.is_available():
    device = torch.device("cuda:3")
    print("running on the GPU", device)
else:
    device = torch.device("cpu")
    print("running on the CPU")

def predictor(model_path, test_list, folder_out, device, dic):
    """
    Takes a model, makes predictions and save output in folder
    default model save as diccionary
    """
    
    if dic == True:
        model_nass = CM.Crop_model_nasa().to(device)
        checkpoint = torch.load(model_path)
        model_nass.load_state_dict(checkpoint['model_state_dict'])
        
        for file in test_list:
            with torch.no_grad():
                test = model_nass(torch.load(file).float())
                test = test.detach().numpy()
                #print(test.shape)
                test = test[0, 0, :, :]
                #print(test.shape)
            name_out =  "prediction."+  file.split(".")[2] + "."+ file.split(".")[3] #prediction.A2017.US35637 <- example
            name_out = folder_out + "/" + name_out + '.tif'
            print(name_out)
            #matplotlib.image.imsave(name_out, test)
            test = Image.fromarray(test)
            test.save(name_out)
    else:
        model = torch.load(model_path, map_location=torch.device(device))
        model.eval()
        for file in test_list:
            with torch.no_grad():
                test = model(torch.load(file).float())
                test = test.detach().numpy()
                #print(test.shape)
                test = test[0, 0, :, :]
                #print(test.shape)
            name_out =  "prediction."+  file.split(".")[2] + "."+ file.split(".")[3] #prediction.A2017.US35637 <- example
            name_out = folder_out + "/" + name_out + '.tif'
            print(name_out)
            #matplotlib.image.imsave(name_out, test)
            test = Image.fromarray(test)
            test.save(name_out)


#NASS spatial predictions on train set
predictor("nice_models_results/NASS_spatial.pth",A_spatial ,"Predictions/Train_set/NASS_spatial", device, True)
print("NASS spatial predictions complited")
#NASS temporal predictions on train set
predictor("nice_models_results/NASS_temporal.pth",A_temporal ,"Predictions/Train_set/NASS_temporal", device, True)
print("NASS temporal predictions complited")
#CDL temporal predictions on train set
predictor("nice_models_results/CDL_temporal.pth",A_temporal ,"Predictions/Train_set/CDL_temporal", device, True)
print("CDL temporal predictions complited")
#CDL spatial predictions on train set
predictor("nice_models_results/CDL_spatial.pth",A_spatial ,"Predictions/Train_set/CDL_spatial", device, True)
print("CDL spatial predictions complited")

###########  test

#NASS spatial predictions on train set
predictor("nice_models_results/NASS_spatial.pth",B_spatial ,"Predictions/Test_set/NASS_spatial", device, True)
print("NASS spatial predictions complited")
#NASS temporal predictions on train set
predictor("nice_models_results/NASS_temporal.pth",B_temporal ,"Predictions/Test_set/NASS_temporal", device, True)
print("NASS temporal predictions complited")
#CDL temporal predictions on train set
predictor("nice_models_results/CDL_temporal.pth",B_temporal ,"Predictions/Test_set/CDL_temporal", device, True)
print("CDL temporal predictions complited")
#CDL spatial predictions on train set
predictor("nice_models_results/CDL_spatial.pth",B_spatial ,"Predictions/Test_set/CDL_spatial", device, True)

print("CDL spatial predictions complited")
