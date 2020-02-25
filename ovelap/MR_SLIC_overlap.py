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
    #submit image with job 
    img = Image.open( k +'.jpg')
    
    image = img_as_float(img)
    #슬레이브 노드로 작업 분배
    #각 노드에서 이미지 읽고 작업
    segments,distances = slic(image, n_segments = numSegments, sigma = 5)
    #segments(lable(nesre_segments))데이터와 distance 데이터를 둘다 받는다.
    
    
    finish_time = time.time()
    return start_time, finish_time

#times, segments, distances 를 리턴받는다.
stime = time.time()
times = sc.parallelize(k,partition).map(Map).collect()
ftime = time.time()

#cython 파일을 실행한다.

#전체 이미지 크기의 label을 생성한다.(메타데이터)

#전달받은 nearest_segments 데이터와 distance 데이터를 이용해 새로운 label을 갱신한다.

#마스터로 리턴받는다.





#time check
import pandas as pd
data = pd.DataFrame(columns=['node','time'])
number = 0
node = 1
datat = pd.DataFrame(columns=['node','time'])
pd.options.display.float_format = '{:.6f}'.format
for i in times:
    datat.loc[number]=['node '+str(node),i[1]-i[0]]
    
    data.loc[number]=['node '+str(node)+' start',i[0]]
    number += 1
    data.loc[number]=['node '+str(node)+' finish',i[1]]
    number += 1
    node+=1

#network time
for i in [0,2,4,6]:
    print('network_ in_time : '+str(data['time'][i]-stime))
for i in [1,3,5,7]:
    print('network_ out_time : '+str(ftime-data['time'][i]))
    
    
data = data.sort_values(by=['time'], axis=0)

#print
#slave time
print('slave node time')
print(data)

print(datat)

#whole time
print('whole_time : '+str(ftime-stime))


