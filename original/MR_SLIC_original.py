# USAGE
# MR-SLIC_original
from pyspark.context import SparkContext
from skimage.segmentation import mark_boundaries
from skimage import io

import time
from skimage.segmentation import slic
from PIL import Image
from skimage.util import img_as_float

sc = SparkContext()

#number of partition
partition = 4

#resource file name
k=['house1','house2','house3','house4']



# loop over the number of segments
numSegments = 500




def Map(k):
    #time check
    start_time = time.time()
    #read imagez
    img = Image.open('gs://dataproc-c0ca77ba-126c-45b8-a839-82019a5cdd13-asia-east1/resource/' + k +'.jpg')
    
    image = img_as_float(img)
    
    segments = slic(image, n_segments = numSegments, sigma = 5)
    
    finish_time = time.time()
    print(finish_time-start_time)
    return finish_time-start_time
stime = time.time()
ttime = sc.parallelize(k,partition).map(Map).collect()
ftime = time.time()
print(ttime)
print(ftime-stime)