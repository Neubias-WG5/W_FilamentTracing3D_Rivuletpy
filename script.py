import os
import time
import sys
import glob
import imageio as imgio
import argparse
from argparse import RawTextHelpFormatter
from subprocess import call
from cytomine.models import Job
from swc_to_tiff_stack import swc_to_tiff_stack

parser = argparse.ArgumentParser(add_help=True, description='Trace filaments in input images', formatter_class=RawTextHelpFormatter)
parser.add_argument('--infld', help='input folder', required=True)
parser.add_argument('--outfld', help='output folder', required=True)
parser.add_argument('--threshold_value', help='threshold intensity value', required=True)
parser.add_argument('--quality_run', help='outputs trace with higher quality (or not)', required=True)
args = parser.parse_args()

in_path = args.infld # 
out_path = args.outfld # 

# Functional parameters
threshold_value = float(args.threshold_value) # default: 0
quality_run = bool(args.quality_run) # default: False

print("Starting workflow!")
#print(os.listdir(in_path))
images = (glob.glob(in_path+"/*.tif"))
in_images = [f for f in os.listdir(in_path) if f.endswith('.' + 'tif')]
out_file_path = [out_path + item for item in in_images]

for neubias_input_image in images:
    print('---------------------------')
    out_file_path = os.path.join(out_path, neubias_input_image)
    print('doing '+file_path)

    #Compute the neuron tracing with set parameters
    if quality_run == True
        command = "rtrace -f " + neubias_input_image + " -o " + out_file_path[:-4] + ".swc --threshold " + threshold_value + " --quality"
    else
        command = "rtrace -f " + neubias_input_image + " -o " + out_file_path[:-4] + ".swc --threshold " + threshold_value 

    print("Run tracing workflow:"+command)
    return_code = call(command, shell=True, cwd="/") # waits for the subprocess to return   
    print("Finished running :"+command)
    
    #im_size = imgio.imread(os.path.join(out_path, filename)).shape
    im_size = imgio.volread(out_file_path).shape #Size is Depth,Height,Width
    im_size = im_size[::-1] #Invert the size order to Width,Height,Depth
    print('size of the image is: ' + im_size)
    
    #Needed for some vaa3d workflow where the output path is not taken into account.
    #os.rename(out_file_path[:-4]+".tif_ini.swc", out_file_path[:-4]+ ".swc")
    print("Run:"+' swc_to_tiff_stack('+ out_file_path[:-4] +'.swc, '+ out_path +','+ str(im_size)+')')
    
    # Convert the .swc tracing result to tiff stack files
    swc_to_tiff_stack(out_file_path[:-4]+ ".swc", out_path, im_size)
    print('Finished converting swc files to image stacks')
    #TODO: error handling...
    
print("Done")    

