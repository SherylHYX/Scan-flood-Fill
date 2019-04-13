
# coding: utf-8
import numpy as np
import cv2
import time
import os

INPUT_PATH = 'F:/fill_boundary/input_images0320/'
OUTPUT_PATH_FILL = 'F:/fill_boundary/output_no_holes0413/'
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
    # Home made flood fill
    #floodFill(padImg, height, width, 0, 0, 255, 0, 128)

    cvFloodFill(padImg, height, width, 128)
    #cv2.imwrite(cvPath,padImg, [int(cv2.IMWRITE_JPEG_QUALITY),100])
    filledImg = cropAndReverse(padImg, height, width, 255, 0, 128)
    cv2.imwrite(savePath, filledImg, [int(cv2.IMWRITE_JPEG_QUALITY),100])
    #padImg.fill(0)
    #filledImg.fill(0)


def fillBoundary_main():
    fill_time = np.zeros([10])
    for i, n in enumerate(range(200, 2200, 200)):
        output_folder_name = 'original_size_' + str(n)
        input_folder_name = 'input_' + str(n)
        input_path = os.path.join(INPUT_PATH, input_folder_name)
        output_path_fill = os.path.join(OUTPUT_PATH_FILL, output_folder_name)
        # delete previous files
        #os.mkdir(output_path_fill)
        del_file(output_path_fill)
        start = time.clock()
        for root, dirs, files in os.walk(input_path):
            for f in files:
                fillBoundaryMain(os.path.join(input_path, f), os.path.join(output_path_fill, f))
        elapsed = (time.clock() - start)
        print("Time used for size {} is:".format(str(n)))
        print(elapsed)
        fill_time[i] = elapsed
    print(fill_time)
    np.savetxt("EFCI_time_size.csv", fill_time, delimiter=",")

if __name__ == '__main__':
    fillBoundary_main()
