import argparse
import simple_inference_pipeline
import dicom_filter

if __name__ == "__main__":
    
    # Create argument parser for the path of input dicom directory, input config file, output dicom directory
    parser = argparse.ArgumentParser(description="Pipeline")
    parser.add_argument("--input-npy","-i",help="Path to input diocm directory",required=True)
    parser.add_argument("--config","-c",help="Path to config file",required=True)
    parser.add_argument("--output-dicom", "-o",help="Path to output dicom directory",required=True)
    args = parser.parse_args()


