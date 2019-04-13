# coding: utf-8
import numpy as np
import cv2
import time
import os

OUTPUT_PATH_TEMP = 'F:/fill_boundary/output_images_temp/'
INPUT_PATH = 'F:/fill_boundary/input_images0320/'
OUTPUT_PATH_FILL = 'F:/fill_boundary/output_holes_0413/'
colorThreshold = 35

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

def inverse_img(croppedImg, height, width, backGroundColor, labelColor, fillColor, maskColor):
    for x in range(height-2):
        for y in range(width-2):
            # label is the color that is temporarily used to fill exterior
            if croppedImg[x,y] == labelColor:
                croppedImg[x,y] = backGroundColor
            if croppedImg[x, y] == fillColor:
                croppedImg[x, y] = maskColor
    return croppedImg

def cvFloodFill(img, height, width, seedPosition, fillColor):
    mask = np.zeros([height+2, width +2], np.uint8)
    cv2.floodFill(img, mask, seedPosition, newVal = fillColor, loDiff = 50, upDiff = 50, flags = 4)

def holesInHoles(imgPath, savePath, backGroundColor, boundaryColor, labelColor, fillColor, maskColor):
    padImg, height, width = readAndPad(imgPath, backGroundColor)
    seedPosition = (0, 0)
    cvFloodFill(padImg, height, width, seedPosition, labelColor)
    padImg = np.delete((np.delete(padImg, [0, width-1], axis=1)), [0, height-1], axis=0) #crop
    for x in range(height-2):
        for y in range(width-2):
            pixelValue = padImg[x, y]
            if abs(pixelValue - backGroundColor) < colorThreshold:
                seedPosition = (y,x)
                i = 1
                while abs(padImg[x, y-i] - boundaryColor) < colorThreshold:
                    i = i + 1
                if abs(padImg[x, y-i] - labelColor) < colorThreshold:
                    cvFloodFill(padImg, height-2, width-2, seedPosition, fillColor)
                else:
                    cvFloodFill(padImg, height-2, width-2, seedPosition, labelColor)

    resultImg = inverse_img(padImg, height, width, backGroundColor, labelColor, fillColor, maskColor)
    cv2.imwrite(savePath, resultImg, [int(cv2.IMWRITE_JPEG_QUALITY), 100])
def scan_flood_Fill_main():
    fill_time = np.zeros([10])
    boundaryColor = 255
    fillColor = 128
    labelColor = 80
    backGroundColor = 0
    maskColor = 255
    for i, n in enumerate(range(200, 2200, 200)):
        output_folder_name = 'improved_size_' + str(n)
        input_folder_name = 'input_' + str(n)
        input_path = os.path.join(INPUT_PATH, input_folder_name)
        output_path_fill = os.path.join(OUTPUT_PATH_FILL, output_folder_name)
        #os.mkdir(output_path_fill)
        # delete previous files
        del_file(output_path_fill)
        start = time.clock()
        for root, dirs, files in os.walk(input_path):
            for f in files:
                holesInHoles(os.path.join(input_path, f), os.path.join(output_path_fill, f), backGroundColor, boundaryColor, labelColor, fillColor, maskColor)
        elapsed = (time.clock() - start)
        print("Scan-flood fill time used for height=width= {} is:".format(str(n)))
        print(elapsed)
        fill_time[i] = elapsed
    print(fill_time)
    np.savetxt("scan_flood_Fill_time_size.csv", fill_time, delimiter=",")


if __name__ == '__main__':
    scan_flood_Fill_main()


