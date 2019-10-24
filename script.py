import os
import glob
import argparse
from argparse import RawTextHelpFormatter
from subprocess import call
import imageio as imgio
from swc_to_tiff_stack import swc_to_tiff_stack
from .node_sorter import swc_node_sorter
from .node_sorter import findchildren

parser = argparse.ArgumentParser(add_help=True, \
                                 description='Trace filaments in input images', \
                                 formatter_class=RawTextHelpFormatter)
parser.add_argument('--infld', help='input folder', required=True)
parser.add_argument('--outfld', help='output folder', required=True)
# UNCOMMENT THE NEXT TWO LINES AFTER ADDING THE WORKFLOW TO BIAFLOWS
parser.add_argument('--threshold_value', help='threshold intensity value', required=True)
parser.add_argument('--quality_run', \
                    help='outputs trace with higher quality (or not)', \
                    required=True)
args = parser.parse_args()
in_path = args.infld + '/'
out_path = args.outfld + '/'

print(out_path + ' is the output file path')
# Functional parameters UNCOMMENT THE NEXT TWO LINES AFTER ADDING THE WORKFLOW TO BIAFLOWS
#Add a test to see if the threshold parameter value is None (Default value is zero but somehow 0 is changed to None)
if args.threshold_value is not None:
    threshold_value=0
else:
    threshold_value = float(args.threshold_value) # default: 0
quality_run = bool(args.quality_run) # defalut: False 
# temporary attribute values to test locally COMMENT THE FOLLOWING TWO LINES AFTER ADDING THE WORKFLOW TO BIAFLOWS
# threshold_value = '5'
# quality_run = True

print("Starting workflow!")
#print(os.listdir(in_path))
images = (glob.glob(in_path+"/*.tif"))
listdir = os.listdir(in_path)
in_images = [f for f in listdir if f.endswith('.' + 'tif')]
# out_file_path = [out_path + '/' + item for item in in_images]

for neubias_input_image in in_images:
    # set input and output file path
    in_file_path = in_path + neubias_input_image
    out_file_path = out_path + neubias_input_image

    print('---------------------------')
    #print('Doing '+ in_path + neubias_input_image + \
    #    ' and saving the output to ' + \
    #    out_path)
    print("Doing {}{} and saving the output to {}".format(in_path,neubias_input_image,out_path))

    #Compute the neuron tracing with set parameters
    if quality_run is True:
        command = "rtrace -f {} -o {}.swc --threshold {} --quality".format(in_file_path,
                                                                            out_file_path[:-4],
                                                                            threshold_value)
      #command = "rtrace -f " + in_file_path + \
      #" -o " + out_file_path[:-4] + ".swc --threshold " + threshold_value + " --quality"
    else:
        command = "rtrace -f {} -o {}.swc --threshold {}".format(in_file_path,
                                                                  out_file_path[:-4],
                                                                  threshold_value)
      #command = "rtrace -f " + in_file_path + \
      #" -o " + out_file_path[:-4] + ".swc --threshold " + threshold_value

    print("Run tracing workflow:"+command)
    return_code = call(command, shell=True, cwd="/") # waits for the subprocess to return
    print("Finished running :"+command)

    #im_size = imgio.imread(os.path.join(out_path, filename)).shape
    im_size = imgio.volread(in_file_path).shape #Size is Depth,Height,Width
    im_size = im_size[::-1] #Invert the size order to Width,Height,Depth
    print('size of the image is: ' + str(im_size))

    #Needed for some vaa3d workflow where the output path is not taken into account.
    #os.rename(out_file_path[:-4]+".tif_ini.swc", out_file_path[:-4]+ ".swc")
    print("Run:"+' swc_to_tiff_stack('+ out_file_path[:-4] + \
        '.swc, '+ out_path +','+ str(im_size)+')')

    # call node_sorter functions to order swc and saves it with the same name and path
    swc_node_sorter(out_file_path[:-4]+".swc")
    
    # Convert the .swc tracing result to tiff stack files
    swc_to_tiff_stack(out_file_path[:-4]+".swc", out_path, im_size)
    print('Finished converting swc files to image stacks')
    #TODO: error handling...
print("Done")
