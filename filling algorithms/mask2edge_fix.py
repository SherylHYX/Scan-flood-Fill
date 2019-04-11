# coding: utf-8
import numpy as np
import cv2
import os
from skimage import measure,draw,data,filters,feature
import matplotlib.pyplot as plt

INPUT_PATH = 'F:/fill_boundary/MSRA10K_Imgs_GT/MSRA10K_Imgs_GT/Imgs_fix'
OUTPUT_PATH = 'F:/fill_boundary/MSRA10K_Imgs_GT/MSRA10K_Imgs_GT/Imgs_boundary_fix'
colorThreshold = 20


def del_file(path):
    # delete files
    for i in os.listdir(path):
        path_file = os.path.join(path, i)
        if os.path.isfile(path_file):
            os.remove(path_file)
        else:
            del_file(path_file)


def fixBoundary(img, startPoint, direction, length, boundaryColour, isEdge = False):
    currentPoint = startPoint
    #isEdge = False
    for index in range(0, length):
        if isEdge:
            if img[currentPoint[0], currentPoint[1]] == boundaryColour:
                isEdge = False
                pass
            else:
                img[currentPoint[0], currentPoint[1]] = boundaryColour
        elif img[currentPoint[0], currentPoint[1]] == boundaryColour:
            isEdge = True
        currentPoint = [currentPoint[0] + direction[0], currentPoint[1] + direction[1]]


def mask2edge(inputPath, outputPath):
    img = cv2.imread(inputPath, 0)
    row, column = img.shape
    contours = measure.find_contours(img, 0.5)
    result = np.zeros([row, column])

    for n,contour in enumerate(contours):
        for point in contour:
            result[int(point[0]), int(point[1])] = 255
    #move counterclockwise
    isEdge = False
    fixBoundary(result, [0, 0], [1, 0], row, 255, isEdge)
    fixBoundary(result, [row - 1, 0], [0, 1], column, 255, isEdge)
    fixBoundary(result, [row - 1, column - 1], [-1, 0], row, 255, isEdge)
    fixBoundary(result, [0, column - 1], [0, -1], column, 255, isEdge)
    cv2.imwrite(outputPath, result.astype('uint8'), [int(cv2.IMWRITE_PNG_COMPRESSION), 0])



def mask2edge_main():
    input_path = INPUT_PATH
    output_path = OUTPUT_PATH
    # delete previous files
    del_file(OUTPUT_PATH)
    for root, dirs, files in os.walk(input_path):
        for f in files:
            mask2edge(os.path.join(input_path, f), os.path.join(output_path, f))


if __name__ == '__main__':
    mask2edge_main()


