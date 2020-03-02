#cython: cdivision=True
#cython: boundscheck=False
#cython: nonecheck=False
#cython: wraparound=False
from libc.float cimport DBL_MAX
from cpython cimport bool

import numpy as np
cimport numpy as cnp

from ..util import regular_grid


def _slic_cythonM(list distancep, list nearest_segmentsp, Py_ssize_t[::1] index, long[::1] dimension, Py_ssize_t[::1] listi):
    cdef Py_ssize_t depth, height, width
    depth = dimension[0]
    height = dimension[1]
    width = dimension[2]
    cdef Py_ssize_t[:, :, ::1] nearest_segmentsO \
        = np.empty((depth, height, width), dtype=np.intp)
    cdef double[:, :, ::1] distanceO \
        = np.empty((depth, height, width), dtype=np.double)
    cdef Py_ssize_t i,z,y,x,z_min, y_min, x_min
    distanceO[:, :, :] = DBL_MAX
    cdef Py_ssize_t n_node = index.shape[0]
   
    #인덱스 생성 
    cdef Py_ssize_t 
    cdef Py_ssize_t[::1] startpixel = np.empty(3, dtype=np.intp) 
    
    for i in range(n_node):
        index[i] = listi[index[i]-1]
    
    #노드 수 만큼의 Data객체 생성하기 
    cdef Data data0,data1,data2,data3,data4


    for i in range(1):
        data0 = Data(np.asarray(distancep[0]),np.asarray(nearest_segmentsp[0]))
        if n_node ==1:
            break
        data1 = Data(np.asarray(distancep[1]),np.asarray(nearest_segmentsp[1]))
        if n_node == 2:
            break
        data2 = Data(np.asarray(distancep[2]),np.asarray(nearest_segmentsp[2]))
        if n_node == 3:
            break
        data3 = Data(np.asarray(distancep[3]),np.asarray(nearest_segmentsp[3]))
        if n_node == 4:
            break
        data4 = Data(np.asarray(distancep[4]),np.asarray(nearest_segmentsp[4]))
        if n_node == 5:
            break
        
        
    #직접 입력하기
    with nogil: 
        for i in range(0,n_node):
            z_min = 0
            y_min = index[i]
            
            if i==0:
                for z in range(z_min,z_min+data0.distance.shape[0]):
                    for y in range(y_min,y_min+data0.distance.shape[1]):
                        for x in range(0, width):
                            if distanceO[z,y,x] > data0.distance[z,y-y_min,x]:
                                distanceO[z,y,x] = data0.distance[z,y-y_min,x]
                                nearest_segmentsO[z,y,x] = data0.nearest_segments[z,y-y_min,x]
                                
            if i==1:
                for z in range(z_min,z_min+data1.distance.shape[0]):
                    for y in range(y_min,y_min+data1.distance.shape[1]):
                        for x in range(0, width):
                            if distanceO[z,y,x] > data1.distance[z,y-y_min,x]:
                                distanceO[z,y,x] = data1.distance[z,y-y_min,x]
                                nearest_segmentsO[z,y,x] = data1.nearest_segments[z,y-y_min,x]
                                
            if i==2:
                for z in range(z_min,z_min+data2.distance.shape[0]):
                    for y in range(y_min,y_min+data2.distance.shape[1]):
                        for x in range(0, width):
                            if distanceO[z,y,x] > data2.distance[z,y-y_min,x]:
                                distanceO[z,y,x] = data2.distance[z,y-y_min,x]
                                nearest_segmentsO[z,y,x] = data2.nearest_segments[z,y-y_min,x]
                                
            if i==3:
                for z in range(z_min,z_min+data3.distance.shape[0]):
                    for y in range(y_min,y_min+data3.distance.shape[1]):
                        for x in range(0, width):
                            if distanceO[z,y,x] > data3.distance[z,y-y_min,x]:
                                distanceO[z,y,x] = data3.distance[z,y-y_min,x]
                                nearest_segmentsO[z,y,x] = data3.nearest_segments[z,y-y_min,x]
                                
            if i==4:
                for z in range(z_min,z_min+data4.distance.shape[0]):
                    for y in range(y_min,y_min+data4.distance.shape[1]):
                        for x in range(0, width):
                            if distanceO[z,y,x] > data4.distance[z,y-y_min,x]:
                                distanceO[z,y,x] = data4.distance[z,y-y_min,x]
                                nearest_segmentsO[z,y,x] = data4.nearest_segments[z,y-y_min,x]
                                
            
            
            

    return np.asarray(nearest_segmentsO)