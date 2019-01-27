#importing libraries
import pandas as pd
import numpy as np
from sklearn.neural_network import BernoulliRBM
from scipy.cluster import hierarchy
import matplotlib.pyplot as plt
from os import path
import os
import csv




#All the pathfiles used in the code below can be set to the same directory as the output directory of the J_site_descriptor.


#This first for loop loops around all the ligand files present in the given path directory.
#To use this loop, first we need to save the output files obtained from the
# J_site_descriptor numerically( i.e. 1,2,3,4) with .txt extension
#Regex can also be used instead of numbering the files. But we still need to change the extension for python to work on it.
num_of_pmdesc_files=2 

#This variable accounts for the number of pm_desc files present in the given directory.
 
#This first for loop saves the given text files with CSV extension so that it can be processed further
for x in range (1,num_of_pmdesc_files+1):
    #filepath specifies the directory of the files
    filepath= os.path.normpath(r'C:\Users\DELL\Desktop\Intern\binaries\test results\1bmd\{}.txt'.format(x))
    with open(filepath,'r') as in_file:
     stripped= (line.strip() for line in in_file)
     lines=(line.split(",") for line in stripped if line)
     with open(r'C:\Users\DELL\Desktop\Intern\binaries\test results\1bmd\log{}.csv'.format(x),'w') as out_file:
        writer = csv.writer(out_file)
        writer.writerows(lines)

#This loop trains the models and generate the output for all the files present in the directory in single execution
for x in range(1,num_of_pmdesc_files+1):
    
  #datapath of the individual files.  
  datapath=r"C:\Users\DELL\Desktop\Intern\binaries\test results\1bmd\log{}.csv.".format(x)
  data = pd.read_csv(datapath, sep=" ")
  tarr= np.array(data)

  index=[] #empty list for storing indexes of elements
  XYZ=[] #empth list for storing the binned dataset

#Output from the J_site_descriptor has 120 sets of distant elements, which are passes seperately into an RBM
#So, binning the dataset into 120 differnt bins and saving it as an array for futher use.
#This for loop is used to determine the indexes of different bins.
#if statement used here is used to seperate the float values from int values. Int values are used to specify the number of distant elements in the bin.
  for i in range(0,len(tarr)):
    if ((tarr[i]%1)==0):
        index.append(i)
        
#This loop uses the above obtained index and seperates the original numpy array into 120 bins        
  for j in range(0,len(index)):
     b= index[j]
     l=j+1
     if(l==120):
        XYZ.append([])
     else:     
       c= index[l]
       XYZ.append([])                        
       for k in range(b+1,c):
          XYZ[j].append(tarr[k])
# saving the list as an array
  XYZ= np.asarray(XYZ)



# saves the binned array as an output excel file. 
  df = pd.DataFrame(XYZ)
  filepath= r"C:\Users\DELL\Desktop\Intern\binaries\test results\1bmd\clean{}.xlsx".format(x)    
  df.to_excel(filepath, index=False)      



#training RBM 
#Given RBM has 3 hidden layer which inturn produces vector embeddings from the given input.

  model= BernoulliRBM(n_components=3, learning_rate=0.2, n_iter=500,batch_size=10,verbose=1)
  from sklearn.preprocessing import StandardScaler
  sc = StandardScaler()
  Y_predicted=[]
# Y_predicted is used to save the predicted values from  the RBM into a list of arrays.
#loops over 120 bins for fitting the model to each bin  
  for t in range(0,120):
    X_train= XYZ[t]
    if(len(X_train)>5): #removing length of bins with less than 5 elements
      X_train = np.reshape(X_train,(len(X_train),1))
      X_train= sc.fit_transform(X_train) # applying normalisation
      Y=model.fit_transform(X_train)
      Y_predicted.append(Y) #list consisting of predictions

#Saves the vector embeddings as a excel file.      
  df = pd.DataFrame(Y_predicted)
  filepath= r"C:\Users\DELL\Desktop\Intern\binaries\test results\1bmd\Y_predicted{}.xlsx".format(x)    
  df.to_excel(filepath, index=False)  

  
     


#makedir is the variable used to make new directories for the storage of dendrograms plotted on predicted data    

  makedir=r"C:\Users\DELL\Desktop\Intern\binaries\test results\1bmd\figure{}".format(x)
#path of the directory where the folder for storing dendrograms is to be made  
  os.makedirs(makedir)
#loops over each output from the RBM stored in the variable Y_predicted
  for l in range(0,len(Y_predicted)):
   ytdist=Y_predicted[l]   
   Z = hierarchy.linkage(ytdist, 'single')
   plt.figure()
   dn = hierarchy.dendrogram(Z)
   plt.savefig(path.join(makedir,"dendrogram_{0}.png".format(l))) 
   # saving graphs as png format
   
 
 
