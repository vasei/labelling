import numpy as np


def closestPoint(keypoints, descriptors, labelX, labelY):

    min_element = 0
    k = 0
    d = 0
    for i in range(len(keypoints)):
        temp = np.sqrt(np.abs((keypoints[i].pt[0] - labelY) ** 2 + (keypoints[i].pt[1] - labelX) ** 2))
        if i == 0:
            min_element = temp
        elif temp < min_element:
            min_element = temp
            k = keypoints[i]
            d = descriptors[i]
    return k, d
