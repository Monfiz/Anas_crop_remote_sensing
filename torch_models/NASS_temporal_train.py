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

import modis_read 
from data_generator import Crop_Generator
import Crop_Models as CM 

print("Check point 1: Libraries imported :) ")

#Find data:

A = modis_read.read_modis_original('lists_data/A_temp_0.txt', 'lists_data/A_temp_1.txt', 'lists_data/A_temp_2.txt')

print("Check point 2: data found")
print("Length data: ", len(A[0]))

#Set divice: 

if torch.cuda.is_available():
    device = torch.device("cuda:3")
    print("running on the GPU", device)
else:
    device = torch.device("cpu")
    print("running on the CPU")

train_set = Crop_Generator(A, validation = False, target ="NASS")
train_gen = torch.utils.data.DataLoader(train_set, batch_size=3, shuffle=True, num_workers=0) 

print("Check point 3: Data successfully loaded by sequencer")

model = CM.Crop_model_nasa().to(device)

#hyper parameters
learning_rate = 0.001
loss_fn = nn.MSELoss()
optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)
num_epoch = 20
epochs_schedule = 8
scheduler = torch.optim.lr_scheduler.OneCycleLR(optimizer, max_lr=0.01, 
                                                steps_per_epoch=len(train_gen), epochs=epochs_schedule)
                                    
#
print(f'learning rate: {learning_rate}, num epoch: {num_epoch}')
print("Check point 4: Model loaded, starting training.....")


#track of performance
epoch_list = []
mse_list = []
lrs = [] 
# Epoch loop
for epoch in range(1, num_epoch + 1):
    
    # Reset metrics
    train_loss = 0.0
    start_time = time.time()

    # Training loop
    model.train()
    for i, [inputs, cdl, nass] in enumerate(train_gen):

        inputs = inputs.to(device).float()
        cdl = cdl.to(device).float()
        nass = nass.to(device).float()
        # create mask to control for nan values
        mask = torch.where(cdl == -1, 0., 1.)
        

        optimizer.zero_grad() # clear gradients
        output = model(inputs) # forward pass: predict outputs for each image outputs
        # apply masking to output and target
        output = output*mask
        percent = output.sum(dim = [1, 2, 3, 4]) / mask.sum(dim = [1, 2, 3, 4])

        loss = loss_fn(percent, nass) # calculate loss
        loss.backward() # backward pass: compute gradient of the loss wrt model parameters
        optimizer.step() # update parameters

        lrs.append(optimizer.param_groups[0]["lr"])

        train_loss += loss.item() * inputs.size(0)# update training loss 

        if i % 50 == 0:
            print("Epoch:", epoch,"Batch:", i, "Loss mse:", loss.item())

        if epoch <=epochs_schedule:
            scheduler.step() 
        else:
            continue
    train_loss = train_loss/len(train_gen.sampler)#average of the error in epoch 

    # Display metrics at the end of each epoch. 
    epoch_list.append(epoch)
    mse_list.append(train_loss)
    
    print(f'Epoch: {epoch} \tTraining Loss: {train_loss}', "________ _________ _______ ")
    print(" epoch time --- %s seconds ---" % (time.time() - start_time))

#save model
print("Saving model...")
PATH = "nice_models_results/NASS_temporal.pth"
torch.save(model, PATH)
torch.save({
            'epoch':epoch_list[-1] ,
            'model_state_dict': model.state_dict(),
            'optimizer_state_dict': optimizer.state_dict(),
            'loss': train_loss,
            }, PATH)


plt.plot(epoch_list, mse_list)
plt.xlabel("Epoch")
plt.ylabel("MSE")
plt.title("NASS Training Loss")
plt.savefig('nice_models_results/loss_NASS_temporal.png')

plt.plot(list(range(len(lrs))), lrs)
plt.xlabel("Batches")
plt.ylabel("Learning rate")
plt.title("Evolution of Learning Rate")
plt.savefig('nice_models_results/lr_NASS_temporal.png')

with open("nice_models_results/list_loss_NASS_temporal.txt", 'w') as f:
    for s in mse_list:
        f.write(str(s) + '\n')


print("Muy bien!!! Sehr shoon :)")