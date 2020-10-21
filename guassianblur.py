# -*- coding: utf-8 -*-
"""
Created on Sun Sep 20 23:58:39 2020

@author: Jaswitha
"""

import numpy as np

def gaussian_kernel(a, sigma):
    
    ax = np.arange(-a // 2 + 1., a // 2 + 1.)
    aa, bb = np.meshgrid(ax, ax)
    kernel = np.exp(-(aa**2 + bb**2) / (2. * sigma**2))
    return kernel / np.sum(kernel)

def gaussian_blur3d(input_3d: np.ndarray, meta_data: dict,
                    config: dict) -> np.array:
    '''Performs 3D Gaussian blur on the input volume
    :param input_3d: input volume in 3D numpy array
    :param meta_data: a dict object with the following key(s):
        'spacing': 3-tuple of floats, the pixel spacing in 3D
    :param config: a dict object with the following key(s):
        'sigma': a float indicating size of the Gaussian kernel
    :return: the blurred volume in 3D numpy array, same size as input_3d
    '''
    (a,b,c) = meta_data['spacing']
    sigma = config['sigma']
    np.empty((a,b,c))

    # create guassian kernel
    kernel = gaussian_kernel(a, sigma)
    if c-1 > 0:
        kernel = kernel.reshape([1,kernel.shape[0],kernel.shape[1]])
        kernel = np.concatenate([kernel]*c, axis=0)

    # applying kernel to image
    output = []
    for i in range(b):
        temp = np.copy(input_3d)
        temp = np.roll(temp, i - 1, axis=0)
        for j in range(a):
            temp_x = np.copy(temp)
            temp_x = np.roll(temp_x, j - 1, axis=1) * kernel[i, j]
            output.append(temp_x)

    output = np.array(output)
    output = np.sum( output, axis=0)
    return output
