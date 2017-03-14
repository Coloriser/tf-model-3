from glob import glob
from os.path import exists, join, basename, splitext

import multiprocessing as mp

# import helper_modules dir
import sys
sys.path.insert(0, './helper_modules')

import pre_works_SIFT_train as pwt
# import pre_works_BRISK_train as pwt



EXTENSIONS = [".jpg",".png"]
MAX_IMAGES_TO_PROCESS = -1
#-1 for complete processing. Else processes the threshold number of images.
DELETE_FILES_AFTER_PROCESSING = False
#If true deletes files that are processed.

def get_image_paths( max_size, path="dataset/train"):
    """Get the list of all image files in the train directory"""
    image_paths = []
    image_paths.extend([join(path, basename(fname))
                    for fname in glob(path + "/*")
                    if splitext(fname)[-1].lower() in EXTENSIONS])
    print("Total IMAGES: ", len(image_paths))
    if(max_size != -1):
        image_paths = image_paths[:max_size]
    # print("SIZE TO Be Processed: ", len(image_paths))
    return image_paths



def begin_threaded_execution():
    image_paths = get_image_paths(MAX_IMAGES_TO_PROCESS)

    No_of_images = len( image_paths )
    No_of_cores = mp.cpu_count()

    # Check if multiprocessing is really necessary
    if No_of_images<No_of_cores:
        No_of_cores = 1
        print("MULTIPROCESSING : OFF")
    else:
        print("MULTIPROCESSING : ON")
        print("No of cores     : " + str(No_of_cores))

        
    images_per_core = No_of_images / No_of_cores
    threads = []

    # Define an output queue
    output = mp.Queue()

    process_list = []
    for ith_core in range(No_of_cores):
        # Building processes list
        start_point = images_per_core * ith_core
        end_point = images_per_core * (ith_core+1)

        if ith_core != No_of_cores-1:
            sub_array = image_paths[start_point:end_point]
        else:
            sub_array = image_paths[start_point:]
        print("Beginning execution of thread " + str(ith_core)  + " with " + str(len(sub_array)) + " images")
        process_list.append(mp.Process(target=pwt.process_images, args=(sub_array, ith_core, DELETE_FILES_AFTER_PROCESSING)))

    for p in process_list:
        p.start()
    for p in process_list:
        p.join()    
    print("Processing done, saving paths.")
    pwt.save_paths( image_paths )
    print(str( len(image_paths) ) + " images processed. Proceed to training.") 
    get_image_paths(-1)

begin_threaded_execution()        
