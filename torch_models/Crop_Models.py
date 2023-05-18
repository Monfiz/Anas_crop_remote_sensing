
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
###############
#Models:

class Crop_model_100(nn.Module):

    def __init__(self):
        super(Crop_model_100, self).__init__()

        self.conv1 = nn.Conv3d(in_channels = 1, out_channels = 8, kernel_size=(3,1,1))#padding='valid'
        
        self.conv2 = nn.Conv3d(in_channels = 8, out_channels = 8, kernel_size=(3,1,1))
        
        self.pool = nn.MaxPool3d((2,1,1)) #pool_size=(1,1,2),padding='valid'
        
        self.conv3 = nn.Conv3d(in_channels = 8, out_channels = 16, kernel_size=(3,1,1))
        
        self.conv4 = nn.Conv3d(in_channels = 16, out_channels = 16, kernel_size=(3,1,1))
        
        self.conv5 = nn.Conv3d(in_channels = 16, out_channels = 1, kernel_size=(5,1,1))
        
        self.drop = nn.Dropout(p=0.2)
        
        
    def forward(self, x):
        x = F.relu(self.conv1(x))
        x = self.pool(F.relu(self.conv2(x)))
        x = F.relu(self.conv3(x))
        x = F.relu(self.conv4(x))
        #x = F.relu(self.conv5(x))
        x = self.drop(x)
        
        x_image = torch.sigmoid(self.conv5(x))*100. # TODO: Why sigmoid here?
                           
        return x_image
    


class Crop_model(nn.Module):

    def __init__(self):
        super(Crop_model, self).__init__()

        self.conv1 = nn.Conv3d(in_channels = 1, out_channels = 8, kernel_size=(3,1,1))#padding='valid'
        
        self.conv2 = nn.Conv3d(in_channels = 8, out_channels = 8, kernel_size=(3,1,1))
        
        self.pool = nn.MaxPool3d((2,1,1)) #pool_size=(1,1,2),padding='valid'
        
        self.conv3 = nn.Conv3d(in_channels = 8, out_channels = 16, kernel_size=(3,1,1))
        
        self.conv4 = nn.Conv3d(in_channels = 16, out_channels = 16, kernel_size=(3,1,1))
        
        self.conv5 = nn.Conv3d(in_channels = 16, out_channels = 1, kernel_size=(5,1,1))
        
        self.drop = nn.Dropout(p=0.2)
        
        
    def forward(self, x):
        x = F.relu(self.conv1(x))
        x = self.pool(F.relu(self.conv2(x)))
        x = F.relu(self.conv3(x))
        x = F.relu(self.conv4(x))
        #x = F.relu(self.conv5(x))
        x = self.drop(x)
        
        x_image = torch.sigmoid(self.conv5(x)) # TODO: Why sigmoid here?
                           
        return x_image
    
class Crop_model_nasa(nn.Module):

    def __init__(self):
        super(Crop_model_nasa, self).__init__()

        self.conv1 = nn.Conv3d(in_channels = 1, out_channels = 8, kernel_size=(3,1,1))#padding='valid'
        
        self.conv2 = nn.Conv3d(in_channels = 8, out_channels = 8, kernel_size=(3,1,1))
        
        self.pool = nn.MaxPool3d((2,1,1)) #pool_size=(1,1,2),padding='valid'
        
        self.conv3 = nn.Conv3d(in_channels = 8, out_channels = 16, kernel_size=(3,1,1))
        
        self.conv4 = nn.Conv3d(in_channels = 16, out_channels = 16, kernel_size=(3,1,1))
        
        self.conv5 = nn.Conv3d(in_channels = 16, out_channels = 1, kernel_size=(5,1,1))
        
        self.drop = nn.Dropout(p=0.2)
        
        
    def forward(self, x):
        x = F.relu(self.conv1(x*0.0001)) # We add the factor of sacling according to NASA documentation MODIS
        x = self.pool(F.relu(self.conv2(x)))
        x = F.relu(self.conv3(x))
        x = F.relu(self.conv4(x))
        #x = F.relu(self.conv5(x))
        x = self.drop(x)
        
        x_image = torch.sigmoid(self.conv5(x)) # TODO: Why sigmoid here?
                           
        return x_image
