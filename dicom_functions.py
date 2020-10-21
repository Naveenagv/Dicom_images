import argparse
from pydicom import dcmread
from pydicom.uid import generate_uid
import numpy as np
import json
import os
import matplotlib.pyplot as plt
from skimage import measure, morphology
from skimage.io import show
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

def read_dicom_files(input_path):
    #Get and read all the dcm files in a directory which have SliceLocation attribute
    #TO DO: Check if the file extension has .dcm
    dcm_files = [dcmread(input_path+'/'+file) for file in os.listdir(input_path) if hasattr(dcmread(input_path+'/'+file),"SliceLocation")]

    #Sort the dcm file according to slice location
    sorted_dcm_files = sorted(dcm_files, key=lambda x: x.SliceLocation)

    return sorted_dcm_files

def args_numpy_to_dicom():
    # Create argument parser for receiving path to numpy file, template dicom directory, output dicom directory
    parser = argparse.ArgumentParser(description="Convert numpy to DICOM data file")
    parser.add_argument("--input-npy","-n",help="Path to input numpy file",required=True)
    parser.add_argument("--input-dicom","-d",help="Path to template DICOM directory",required=True)
    parser.add_argument("--output-dicom", "-o",help="Path to output json file",required=True)
    return parser.parse_args()

def args_dicom_to_numpy():
    # Create argument parser for receiving path to input dicom directory, numpy output, json metadata output
    parser = argparse.ArgumentParser(description="Convert DICOM to numpy data file")
    parser.add_argument("--input-dicom","-i",help="Path to input DICOM directory",required=True)
    parser.add_argument("--output-npy","-n",help="Path to output numpy file",required=True)
    parser.add_argument("--output-json", "-j",help="Path to output json file",required=True)
    return parser.parse_args()

def check_folder_path(folder):
    if not os.path.exists(folder):
        print ("Folder does not exist: ",folder)
        raise FileNotFoundError
    else:
        print ("File/Folder Exists: ",folder)
        
def save_pixeldata(path,patient_id,volume):
    print ("Saving pixel data in: ",path)
    np.save(path+"/"+patient_id,volume)

def save_metadata(path,patient_id, pixel_spacing, description, modality):
    print ("Savig metadata in json format in: ",path)
    data = {
            "PixelSpacing":pixel_spacing,
            "SeriesDescription":description,
            "Modality":modality
            }
    with open(path+'/'+patient_id+'_metadata.json', 'w') as outfile:
        json.dump(data, outfile)

def get_pixels_hu(scans):
    print ("Plotting Hounsfield Units")
    image = np.stack([s.pixel_array for s in scans])
    # Convert to int16 (from sometimes int16), 
    # should be possible as values should always be low enough (<32k)
    image = image.astype(np.int16)

    # Set outside-of-scan pixels to 0
    # The intercept is usually -1024, so air is approximately 0
    image[image == -2000] = 0
    
    # Convert to Hounsfield units (HU)
    intercept = scans[0].RescaleIntercept
    slope = scans[0].RescaleSlope
    
    if slope != 1:
        image = slope * image.astype(np.float64)
        image = image.astype(np.int16)
        
    image += np.int16(intercept)
    
    image = np.array(image, dtype=np.int16)

    plt.hist(image.flatten(), bins=80, color='c')
    plt.xlabel("Hounsfield Units (HU)")
    plt.ylabel("Frequency")
    plt.show()

def plot_3d(volume,threshold=-300):
    print ("Plot the 3D image")
    p = volume.transpose(2,1,0)
    p = p[:,:,::-1]
    
    verts, faces, norm, val = measure.marching_cubes_lewiner(p,threshold)
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(111, projection='3d')

    # Fancy indexing: `verts[faces]` to generate a collection of triangles
    mesh = Poly3DCollection(verts[faces], alpha=0.1)
    face_color = [0.5, 0.5, 1]
    mesh.set_facecolor(face_color)
    ax.add_collection3d(mesh)

    ax.set_xlim(0, p.shape[0])
    ax.set_ylim(0, p.shape[1])
    ax.set_zlim(0, p.shape[2])

    plt.show()

def normalize(volume):
    print ("Normalizing the volume")
    MIN_BOUND = -1000.0
    MAX_BOUND = 400.0
    volume = (volume - MIN_BOUND) / (MAX_BOUND - MIN_BOUND)
    volume[volume>1] = 1.
    volume[volume<0] = 0.
    return volume

def numpy_to_dicom(pixel_data,dcm_template):
    series_instance_uid = generate_uid()
    sop_instance_uid = generate_uid()
    data_type = dcm_template[0].pixel_array.dtype
    for i in range(pixel_data.shape[-1]):
        dcm_template[i].PixelData = pixel_data[:,:,i].astype(data_type)
        dcm_template[i].SeriesInstanceUID = series_instance_uid
        dcm_template[i].SOPInstanceUID = sop_instance_uid
    return dcm_template
def dicom_to_numpy(slices):
    print ("Converting dicom datasets to numpy")
    # create 3D array
    img_shape = list(slices[0].pixel_array.shape)
    img_shape.append(len(slices))
    img3d = np.zeros(img_shape)

    # fill 3D array with the images from the files
    for i, s in enumerate(slices):
        img2d = s.pixel_array
        img3d[:, :, i] = img2d
    return img3d
