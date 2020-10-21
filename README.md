# Subtle_Medical Coding challenge
Multiple files were uploaded according to the task mentioned in the document

# Converting from Dicom to numPY and reverse
1. dicom_functions.py                             
 The file dicom_function.py has all the functions mentioned below (in order)                                  
 a) Convert DICOM to Numpy format         
 b) Sorting the Dicom image files based on the slice location in the ascending order
 c) Build a 3D volume using slice images.
 d) Nomalization using Minimum and Maximum bound values.                                                                   
 e) Convert CT data to HU units which helps in normalizing and creation of 3D volume with the help of slices
 f) Export pixel data with numpy and the following meta data to a JSON 
 
  
    parser = argparse.ArgumentParser(description="Convert DICOM to numpy data file")
    parser.add_argument("--input-dicom","-i",help="Path to input DICOM directory",required=True)
    parser.add_argument("--output-npy","-n",help="Path to output numpy file",required=True)
    parser.add_argument("--output-json", "-j",help="Path to output json file",required=True)
    return parser.parse_args()
 
 2.dicom1.2.py, Tasks accomplished:
  a) Implemented required command line interface(CLI) for converting DICOM to Numpy
  b) Replaced pixel data inside DICOM data sets.
  c) Rescaled the pixel data to the dynamic range of datatype used by the template DICOM files
  d) Assigned a new Series Instance UID, SOP Instance UID to each of the files.
  
    parser = argparse.ArgumentParser(description="Convert numpy to DICOM data file")
    parser.add_argument("--input-npy","-n",help="Path to input numpy file",required=True)
    parser.add_argument("--input-dicom","-d",help="Path to template DICOM directory",required=True)
    parser.add_argument("--output-dicom", "-o",help="Path to output json file",required=True)
 
 All function are wrapped in dicom_functions.py and the main/calling of action is implemented in seperate scripts(dicom1.1.py, dicom1.2.py,dicom1.3.py).
 
 # Code Structure for dicom filter
 
 3.dicom1.3.py
   a) A dicom filter is implemented using the skeleton:"dicom_filter(input_dir: str, config: dict)"
   b) This function will read all DICOM files from the input directory and sub-directories
   c) Filters the DICOM series based on the configuration and return a list of all matching DICOM series.
   
