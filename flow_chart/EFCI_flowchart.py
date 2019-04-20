
# coding: utf-8
import numpy as np
import cv2
import time
import os

INPUT_PATH = 'F:/Scan-flood-Fill/flow_chart/multi_input'
OUTPUT_PATH_FILL = 'F:/Scan-flood-Fill/flow_chart/multi_output'
background_threshold = 50
# pixel with difference less than this value with the background colour is seen as background colour

def del_file(path):
    # delete files
    for i in os.listdir(path):
        path_file = os.path.join(path, i)
        if os.path.isfile(path_file):
            os.remove(path_file)
        else:
            del_file(path_file)

def pad_with(vector, pad_width, iaxis, kwargs):
    pad_value = kwargs.get('padder', 0)
    vector[:pad_width[0]] = pad_value
    vector[-pad_width[1]:] = pad_value
    return vector

def readAndPad(imagePath, backGroundColour):
    img = cv2.imread(imagePath, 0)
    padImg = np.pad(img,1,pad_with, padder=backGroundColour)
    height, width = padImg.shape[:2]
    return padImg, height, width

def floodFill(img, height, width, x, y, boundaryColour, backGroundColour, fillColour):
    img[x, y] = fillColour
    if (x>0 and img[x-1, y] == backGroundColour):
        floodFill(img, height, width, x-1, y, boundaryColour, backGroundColour, fillColour)
    if (y>0 and img[x, y-1] == backGroundColour):
        floodFill(img, height, width, x, y-1, boundaryColour, backGroundColour, fillColour)
    if (x<(height-1) and img[x+1, y] == backGroundColour):
        floodFill(img, height, width, x+1, y, boundaryColour, backGroundColour, fillColour)
    if (y<(width-1) and img[x, y+1] == backGroundColour):
        floodFill(img, height, width, x, y+1, boundaryColour, backGroundColour, fillColour)

def cvFloodFill(img, height, width, fillColour):
    mask = np.zeros([height+2, width +2], np.uint8)
    cv2.floodFill(img, mask, (0, 0), newVal = fillColour, loDiff = 50, upDiff = 50, flags = 4)

def cropAndReverse(img, height, width, maskColour, backGroundColour, fillColour):
    croppedImg = np.delete((np.delete(img, [0, width-1], axis=1)), [0, height-1], axis=0)
    cv2.imwrite(os.path.join(OUTPUT_PATH_FILL, 'multi_after_cropping.png'), croppedImg.astype('uint8'),[int(cv2.IMWRITE_PNG_COMPRESSION), 0])
    for x in range(height-2):
        for y in range(width-2):
            # fillColour is the colour that is temporarily used to fill exterior
            # maskColour is for the final result (interior)
            if croppedImg[x,y] == fillColour:
                croppedImg[x,y] = backGroundColour
            elif abs(croppedImg[x,y] - backGroundColour) < background_threshold:
                croppedImg[x,y] = maskColour
    return croppedImg

def fillBoundaryMain(imagePath ,savePath):

    padImg, height, width = readAndPad(imagePath, backGroundColour = 0)
    cv2.imwrite(os.path.join(OUTPUT_PATH_FILL, 'multi_after_padding.png'), padImg.astype('uint8'),[int(cv2.IMWRITE_PNG_COMPRESSION), 0])
    cvFloodFill(padImg, height, width, 128)
    cv2.imwrite(os.path.join(OUTPUT_PATH_FILL, 'multi_before_cropping.png'), padImg.astype('uint8'),[int(cv2.IMWRITE_PNG_COMPRESSION), 0])
    filledImg = cropAndReverse(padImg, height, width, 255, 0, 128)
    cv2.imwrite(os.path.join(OUTPUT_PATH_FILL, 'multi_final.png'), filledImg.astype('uint8'),[int(cv2.IMWRITE_PNG_COMPRESSION), 0])



def fillBoundary_main():
    input_path = INPUT_PATH
    output_path_fill = OUTPUT_PATH_FILL
    # delete previous files
    #os.mkdir(output_path_fill)
    del_file(output_path_fill)
    for root, dirs, files in os.walk(input_path):
        for f in files:
            fillBoundaryMain(os.path.join(input_path, f), os.path.join(output_path_fill, f))


if __name__ == '__main__':
    fillBoundary_main()
