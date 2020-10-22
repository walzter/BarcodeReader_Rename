#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 27 20:00:52 2019

@author: Eric Walzthöny (WalzthE)
"""
#importing our dependancies
import time #to time the script
from os import listdir #to list directories in os
import shutil #used to copy files
from os.path import join #to join paths
import cv2 #allows us to "read"/scan the image for barcodes
import pyzbar.pyzbar as pyzbar #ability to decode barcodes/QR 

start = time.time() #timer start

mypath = '' #path to Error Folder
output = '' #output Folder


#.Ds_Store is a temporary file created by the OS to track files being modified
def mylistdir(directory):
    """A specialized version of os.listdir() that ignores files that
    start with a leading period."""
    filelist = listdir(directory)
    return [x for x in filelist
            if not (x.startswith('.'))]
    
    

file_path = [join(mypath,f) for f in mylistdir(mypath)] #file path
log1 = [] #list with barcodes that do not match criteria 
img_brcde_dict = {} #dictionary: keep track of which barcodes are from which file


def decode(im) :
    '''
    Decodes barcodes after being read through cv2. 
    It appends to dictionary and creates log. 
    '''
  # decoding barcodes found in image 
    decodedObjects = pyzbar.decode(im)
  #iterating through the decoded barcodes
    for obj in decodedObjects:
        try: 
            #barcode meeting criteria of length 13?
            if len(str(int(obj.data))) == 13:
                #adding the barcodes to the corresponding value
                img_brcde_dict[key].append(int(obj.data))
        #anything other than length 13, such as 3rd party barcodes
        except Exception as e:
            #add it to our log1 list
            log1.append(str(e) + " found in file: " + str(img[25:]))
    return decodedObjects #returns barcodes

def rename():
    '''
    Looping through dictionary. 
    Renaming and copying files to output folder
    n-times depending on how many barcodes it contains.
    '''
    for filename, barcodes in img_brcde_dict.items(): 
        if len(barcodes) > 0:
        #checks for multiple barcodes and makes a new file from each
            for barcde in barcodes:
                dst = str(barcde) + ".jpg"
                dst = output + dst
                src = mypath + filename
                shutil.copy(src,dst)
#                print(dst)
        else:
            dst = "CLARIFY__" + str(filename) + "__.jpg"
            dst = output + dst
            src = mypath + filename
            shutil.copy(src,dst)
#            print(dst)
# Main 
if __name__ == '__main__':
  # Read image
  for img in file_path: #looping through file_path
      key = img[len(mypath):] 
      img_brcde_dict.setdefault(key, []) #setting the dictionary to take a list instead of only one value 
      im = cv2.imread(img) #reading the image (.jpg)
      print(img)
      decodedObjects = decode(im) #applying the decode function created earlier
      
  #Renaming and move function
  #rename()
  
  #Filtering dictionary with specific criteria
  only_lrf = {k: v for k, v in img_brcde_dict.items() if  len(v) > 0}
  
  #Non-LRF dictionary
  clarify = {k: v for k, v in img_brcde_dict.items() if  len(v) == 0}
  

end = time.time()
duration = end - start
print("The script ran in: " + ("%.2f" % duration) + " seconds")  
