# USAGE
# MR-SLIC_original
from pyspark.context import SparkContext
from skimage.segmentation import mark_boundaries
from skimage import io
import collections as coll
import time
from scipy import ndimage as ndi
from skimage.segmentation import slic
from PIL import Image
from skimage.util import img_as_float
from ..segmentation._slic import _slic_cythonM
import numpy as np
from ..color import rgb2lab
sc = SparkContext()

#number of partition
partition = 4

#resource file name
k=['house_2_1','house_2_2','house_2_3']
listi = [0,180,360]

# loop over the number of segments
numSegments = 250


#원본 이미지 메타데이터 얻기위한 전처리 
image = Image.open( '/home/wjdrmf314/MR_SLIC_NEW/resource/house.jpg')
image = img_as_float(image)
is_2d = False
if image.ndim == 2:
    # 2D grayscale image
    image = image[np.newaxis, ..., np.newaxis]
    is_2d = True
elif image.ndim == 3 and True:
    # Make 2D multichannel image 3D with depth = 1
    image = image[np.newaxis, ...]
    is_2d = True
elif image.ndim == 3 and not True:
    # Add channel as single last dimension
    image = image[..., np.newaxis]

if True:
    spacing = np.ones(3)
elif isinstance(spacing, (list, tuple)):
    spacing = np.array(spacing, dtype=np.double)
sigma = 5
if not isinstance(sigma, coll.Iterable):
    sigma = np.array([sigma, sigma, sigma], dtype=np.double)
    sigma /= spacing.astype(np.double)
elif isinstance(sigma, (list, tuple)):
    sigma = np.array(sigma, dtype=np.double)
if (sigma > 0).any():
    # add zero smoothing for multichannel dimension
    sigma = list(sigma) + [0]
    image = ndi.gaussian_filter(image, sigma)

convert2lab = None
if True and (convert2lab or convert2lab is None):
    if image.shape[-1] != 3 and convert2lab:
        raise ValueError("Lab colorspace conversion requires a RGB image.")
    elif image.shape[-1] == 3:
        image = rgb2lab(image)

depth, height, width = image.shape[:3]






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
    #k 로 1,2,3 숫자 받는다.
    return segments, distances, start_time, finish_time, k[-1]

#times, segments, distances 를 리턴받는다.
stime = time.time()
datas = sc.parallelize(k,partition).map(Map).collect()
ftime = time.time()

#datas 어레이에서 distance, nearest segments 뽑아내기


#원본 이미지 메타데이터
dimension = [depth,height,width]
dimension = np.array(dimension)

#segments, distances 리스트 만들기
seglist = []
distlist = []
indlist = []
for i in datas:
    seglist += [i[0]]
    distlist += [i[1]]
    indlist += [i[4]]

result = _slic_cythonM(distlist,seglist,indlist,dimension,listi)

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
for i in datas:
    datat.loc[number]=['node '+str(node),i[3]-i[2]]
    
    data.loc[number]=['node '+str(node)+' start',i[2]]
    number += 1
    data.loc[number]=['node '+str(node)+' finish',i[3]]
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


