# -*- coding: utf-8 -*-
"""
Created on Sun Sep 20 18:53:58 2020

@author: Jaswitha
"""

from dicom_functions import *
import numpy as np
import pydicom

def main(pixel_data,dcm_files_template,output_dicom_path):
    if not output_dicom_path[-1] == '\\' or not output_dicom_path[-1] == '/':
        output_dicom_path += '/'
    #Convert the numpy data to 
    new_dcm_files = numpy_to_dicom(pixel_data,dcm_files_template)

    #Write the new dicom files to the output dicom directory
    print ("Create the new DICOM dataset files")
    file_prefix = 'NEW_{0}.dcm'
    for i,ds in enumerate(new_dcm_files,start=1):
        ds.save_as(output_dicom_path+file_prefix.format(str(i)))
    print ("Finished")

if __name__ == "__main__":
    
    args = args_numpy_to_dicom()
    input_npy_path = args.input_npy
    input_dicom_path = args.input_dicom
    output_dicom_path = args.output_dicom

    #Check if numpy file path exists
    check_folder_path(input_npy_path)

    #Check if dicom template directory exists
    check_folder_path(input_dicom_path)

    #Read pixel data from numpy file
    print ("Reading pixel data from numpy file:")
    pixel_data = np.load(input_npy_path)

    #Read dicom template files from the directory
    dcm_files_template = read_dicom_files(input_dicom_path)

    main(pixel_data,dcm_files_template,output_dicom_path)
