import sys
from subprocess import call
from cytomine.models import Job
from neubiaswg5 import CLASS_TRETRC
from neubiaswg5.helpers import NeubiasJob, prepare_data, upload_data, upload_metrics

def main(argv):
    # 0. Initialize Cytomine client and job
    with NeubiasJob.from_cli(argv) as nj:
        nj.job.update(status=Job.RUNNING, progress=0, statusComment="Initialisation...")
        problem_cls = CLASS_TRETRC
        is_2d = False
        # 1. Create working directories on the machine
        # 2. Download the images
        in_images, gt_images, in_path, gt_path, out_path, tmp_path = prepare_data(problem_cls, nj, is_2d=is_2d,
                                                                                  **nj.flags)
        # 3. Call the image analysis workflow using the run script
        nj.job.update(progress=25, statusComment="Launching workflow...")

        #But with the threshold value
        #print("DEBUG TO REMOVE Threshold param value: {}".format(nj.parameters.threshold_value))

        # UNCOMMENT THE NEXT LINE (WITH \ ) WHEN THE WORKFLOW IS ADDED TO BIAFLOWS 
        command = "python script.py --infld {} --outfld {} \
                   --threshold_value {} --quality_run {}".format(in_path, out_path, nj.parameters.threshold_value,
                                                                 nj.parameters.quality_run)
        # Command to test the workflow before it is added to biaflows, which does 
        #   not accept the desciptor.json parameters 
        # command = "python script.py --infld {} --outfld {}".format(in_path, out_path)
        print(command)
        return_code = call(command, shell=True, cwd="/app")  # waits for the subprocess to return

        # 4. Upload the annotation and labels to Cytomine 
        #    (annotations are extracted from the mask using
        # the AnnotationExporter module)
        upload_data(problem_cls, nj, in_images, out_path, **nj.flags, is_2d=is_2d, monitor_params={
             "start": 60, "end": 90,
             "period": 0.1,
             "prefix": "Extracting and uploading polygons from masks"
        })
        # # 5. Compute and upload the metrics
        nj.job.update(progress=80, statusComment="Computing and uploading metrics (if necessary)...")
        upload_metrics(problem_cls, nj, in_images, gt_path, out_path, tmp_path, **nj.flags)
        nj.job.update(status=Job.TERMINATED, progress=100, statusComment="Finished.")
        
if __name__ == "__main__":
    main(sys.argv[1:])
