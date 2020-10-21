import dicom_filter
import dicom_input
import dicom_output
import guassianblur

def pipeline(dicom_input,config_file,dicom_output_path):

    #Preprocessing
    normalized_volume, metadata = dicom_input.main(dicom_input)

    #Processing
    blurred_volume = guassianblur.gaussian_blur3d(normalized_volume,
                    {'spacing':metadata['PixelSpacing']},
                    {'sigma':config_file['sigma']})
    
    #Postprocessing
    dicom_output.main(blurred_volume,dicom_input,dicom_output_path)

if __name__ == "__main__":
    print ("Welcome to the Pipeline")
