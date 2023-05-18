import tensorflow as tf
from skimage import io
import numpy as np
sys.path.append('/home/denise/Desktop/Lutz/pyLib')
from modis_lib import modisDataConverter as dataConv
imp.reload(dataConv)

class rasterPredictionGenerator(tf.keras.utils.Sequence) :
  
    def __init__(self, filePaths, batch_size)
      	self.filePaths = filePaths
      	self.batch_size = batch_size
                
    def __len__(self) :
        return (int(np.ceil(len(self.filePaths) / float(self.batch_size))))
  
  
    def __getitem__(self, idx) :
        
        batch_filePaths = self.filePaths[idx * self.batch_size : (idx+1) * self.batch_size]
  	
  	prediction_data=dataConv.preparePredictionData(prediction_data_path)
	prediction_reshaped=dataConv.reshapeFiles(prediction_data,img_width,img_height,img_depth)
	x_ds =tf.stack(prediction_reshaped)      
    
        return x_ds
