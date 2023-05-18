#libraries
import torch
from torch.utils.data import Dataset 
from torch.utils.data import DataLoader
import numpy as np 
import torch 
import torch.nn as nn
import torchvision.transforms as transforms
import matplotlib.pyplot as plt
import torch.nn.functional as F

#anas fuctions
#import anas_fuctions as aCDL

#########################################_______________

#secuencer to call data
class Crop_Generator(torch.utils.data.Dataset):
    'Characterizes a dataset for PyTorch'
    def __init__(self, data_list, validation = False, target = "CDL"): #dat list will be A_list or B_list
        self.model_imgs = data_list
        print(f'num ims: {len(data_list[0])}')
        self.target = target
        if validation:
            self.type='validation'
        else:
            self.type='train'
            
    def __len__(self):
        # Denotes the number of batches per epoch
        return len(self.model_imgs[0])
    
    def __getitem__(self, index):
        # Generate one sample of data
        #print(index ,"index")
        file_name = self.model_imgs[0][index] #modis load
        X = torch.load(file_name)
        #find CDL:
        target_name = self.model_imgs[1][index]
        Y_cdl = torch.load(target_name)
        Y_cdl = Y_cdl[None,:, :, :] #add extra chanel to match modis
        if self.target == "CDL":
            return X, Y_cdl
        elif self.target == "NASS":
            Y_nass = self.model_imgs[2][index]
            Y_nass = torch.from_numpy(np.asarray(Y_nass)) #save this step go direct to torch           
            return X, Y_cdl, Y_nass