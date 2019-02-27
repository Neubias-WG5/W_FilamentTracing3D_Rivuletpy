import sys
from subprocess import call
from cytomine.models import Job
from neubiaswg5 import CLASS_TRETRC
from neubiaswg5.helpers import NeubiasJob, prepare_data, upload_data, upload_metrics

# these dependencies were initially in workflow.py
import os
import time
import imageio as imgio
from swc_to_tiff_stack import swc_to_tiff_stack

def main(argv):
    # 0. Initialize Cytomine client and job
    with NeubiasJob.from_cli(argv) as nj:
        nj.job.update(status=Job.RUNNING, progress=0, statusComment="Initialisation...")
        problem_cls = CLASS_TRETRC
        is_2d = False
        # 1. Create working directories on the machine
        # 2. Download the images
        in_images, gt_images, in_path, gt_path, out_path, tmp_path = prepare_data(problem_cls, nj, is_2d=is_2d, **nj.flags)
        # 3. Call the image analysis workflow using the run script
        nj.job.update(progress=25, statusComment="Launching workflow...")
        
        for neubias_input_image in in_images:
            print('---------------------------')
            print('---------------------------')
            print('---------------------------')
            file_path=neubias_input_image.filepath
            filename = neubias_input_image.filename
            out_file_path = os.path.join(out_path, filename)
            print('doing '+file_path)
            #Compute the neuron tracing
        
            command = "rtrace -f " + \
            out_file_path + " -o " + out_file_path[:-4]+ ".swc --quality"
            return_code = call(command, shell=True, cwd="/") # waits for the subprocess to return
            time.sleep(2)#Wait 2 seconds because it can't process all the images for some reason
            #os.system(command)
            print("Finished running :"+command)
            #im_size = imgio.imread(os.path.join(out_path, filename)).shape
            im_size = imgio.volread(out_file_path).shape #Size is Depth,Height,Width
            im_size = im_size[::-1] #Invert the size order to Width,Height,Depth
            print(im_size)
            #Rename the swc file form *.tif_ini.swc to *.swc
            #Needed for some vaa3d workflow where the output path is not taken into account.
            #os.rename(out_file_path[:-4]+".tif_ini.swc", out_file_path[:-4]+ ".swc")
            print("Run:"+' swc_to_tiff_stack('+ out_file_path[:-4] +'.swc, '+ out_path +','+ str(im_size)+')')
        
            # Convert the .swc tracing result to tiff stack files
            swc_to_tiff_stack(out_file_path[:-4] + ".swc", out_path, im_size)
            #TODO: error handling...
        
    print("Done")    
        #shArgs = ["python ", "/app/workflow.py ", in_path, out_path]
        #return_code = call(" ".join(shArgs), shell=True, cwd="./")
        #command = "python /workflow.py" \"\"input={},output={}\"\".format(in_path, out_path)
        #return_code = call(command, shell=True, cwd="/")  # waits for the subprocess to return
        #if return_code != 0:
        #    err_desc = "Failed to execute the Vaa3D (return code: {})".format(return_code)
        #    nj.job.update(progress=50, statusComment=err_desc)
        #    raise ValueError(err_desc)       
        # 4. Upload the annotation and labels to Cytomine (annotations are extracted from the mask using
        # the AnnotationExporter module)
        # upload_data(problem_cls, nj, in_images, out_path, **nj.flags, is_2d=is_2d, monitor_params={
        #     "start": 60, "end": 90,
        #     "period": 0.1,
        #     "prefix": "Extracting and uploading polygons from masks"
        # })
        # # 5. Compute and upload the metrics
        # nj.job.update(progress=80, statusComment="Computing and uploading metrics (if necessary)...")
        # upload_metrics(problem_cls, nj, in_images, gt_path, out_path, tmp_path, **nj.flags)
        # nj.job.update(status=Job.TERMINATED, progress=100, statusComment="Finished.")
if __name__ == "__main__":
    main(sys.argv[1:])

