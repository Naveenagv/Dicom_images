# -*- coding: utf-8 -*-
"""
Created on Sun Sep 20 23:51:18 2020

@author: Jaswitha
"""

from glob import glob
import os
from pydicom import dcmread

def dicom_filter(input_dir: str, config: dict) -> list:
    #Get all dcm files in the current folder and sub folders
    print ("Fetch all the dcm files in current folder and subfolders")
    dcm_files = [dcmread(y) for x in os.walk(input_dir) for y in glob(os.path.join(x[0], '*.dcm'))]
    sorted_series_dict = {}
    #Filter the dataset based on the config file
    print ("Filtering the datasets based on configuration")
    for ds in dcm_files:
        instance_id = ds.SeriesInstanceUID
        try:
            if all(getattr(ds,k) == v for k,v in config.items()):
                if instance_id not in sorted_series_dict:
                    sorted_series_dict[instance_id] = [ds]
                else:
                    sorted_series_dict[instance_id].append(ds)
        except Exception as e:
            continue
    return [{k:v} for k,v in sorted_series_dict.items()]
if __name__ == "__main__":

    path = "./coding_challenge_dicom_data"
    config = {"Modality":"PT"}
    filtered_list = dicom_filter(path,config)
    for fl in filtered_list:
        for k,v in fl.items():
            print (k,len(v))
