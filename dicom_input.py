# -*- coding: utf-8 -*-
"""
Created on Sun Sep 20 18:51:36 2020

@author: Jaswitha
"""
from dicom_functions import args_dicom_to_numpy,check_folder_path,dicom_to_numpy,normalize,save_metadata,save_pixeldata,read_dicom_files
import numpy as np

def main(dicom_input,output_path_numpy="",output_path_json=""):
    #Get hounsfield units
    #get_pixels_hu(sorted_dcm_files)

    volume_3d = dicom_to_numpy(dicom_input)
    volume_3d = volume_3d.astype(np.float32)

    #Normalize the 3D
    normalized_volume = normalize(volume_3d)

    #Save json metadata and numpy pixel data
    patient = sorted_dcm_files[0]
    pixel_spacing = [patient.PixelSpacing[0],patient.PixelSpacing[1],patient.SliceThickness]
    if output_path_json == "" and output_path_numpy == "":
        meta_data = {
            "PixelSpacing":pixel_spacing,
            "SeriesDescription":patient.SeriesDescription,
            "Modality":patient.Modality
            }
        print ("Finished")
        return normalized_volume,meta_data
        
    else:
        save_pixeldata(output_path_numpy,patient.PatientID,normalized_volume)
        save_metadata(output_path_json,
                    patient.PatientID,
                    pixel_spacing,
                    patient.SeriesDescription,
                    patient.Modality)
        print ("Finished")
        return
    #3d plot the data
    #plot_3d(volume_3d,0)

if __name__ == "__main__":
    
    args = args_dicom_to_numpy()
    input_path = args.input_dicom
    output_path_numpy = args.output_npy
    output_path_json = args.output_json

    #Check file path
    check_folder_path(input_path)
    sorted_dcm_files = read_dicom_files(input_path)
    main(sorted_dcm_files,output_path_numpy,output_path_json)
