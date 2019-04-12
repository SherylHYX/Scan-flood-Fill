# coding: utf-8
import numpy as np
import cv2
import os

INPUT_PATH = 'F:/fill_boundary/pig_input'
OUTPUT_PATH_FILL = 'F:/fill_boundary/pig_output'
colorThreshold = 20

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

def cropAndReverse(img, height, width, backGroundColor, labelColor):
    croppedImg = np.delete((np.delete(img, [0, width-1], axis=1)), [0, height-1], axis=0)
    cv2.imwrite(os.path.join(OUTPUT_PATH_FILL, 'pig_after_cropping.png'), croppedImg.astype('uint8'),[int(cv2.IMWRITE_PNG_COMPRESSION), 0])

    for x in range(height-2):
        for y in range(width-2):
            # label is the color that is temporarily used to fill exterior
            if croppedImg[x,y] == labelColor:
                croppedImg[x,y] = backGroundColor
            if croppedImg[x, y] == 128:
                croppedImg[x, y] = 255
    return croppedImg

def cvFloodFill(img, height, width, seedPosition, fillColor):
    mask = np.zeros([height+2, width +2], np.uint8)
    cv2.floodFill(img, mask, seedPosition, newVal = fillColor, loDiff = 20, upDiff = 20, flags = 4)

def holesInHoles(imgPath, savePath, backGroundColor, boundaryColor, labelColor, fillColor):
    padImg, height, width = readAndPad(imgPath, backGroundColor)
    for x in range(height):
        for y in range(width):
            if abs(padImg[x, y] - backGroundColor) < 50:
                padImg[x, y] = backGroundColor
            else:
                padImg[x, y] = boundaryColor
    cv2.imwrite(os.path.join(OUTPUT_PATH_FILL, 'pig_before_first_fill.png'), padImg.astype('uint8'), [int(cv2.IMWRITE_PNG_COMPRESSION), 0])
    seedPosition = (0, 0)
    cvFloodFill(padImg, height, width, seedPosition, labelColor)
    j= 1
    fname = 'pig_after_' + str(j) + 'main_filling.png'
    cv2.imwrite(os.path.join(savePath, fname), padImg.astype('uint8'),[int(cv2.IMWRITE_PNG_COMPRESSION), 0])
    for x in range(height):
        for y in range(width):
            pixelValue = padImg[x, y]
            if abs(pixelValue - backGroundColor) < colorThreshold:
                seedPosition = (y,x)
                i = 1
                while abs(padImg[x, y-i] - boundaryColor) < colorThreshold:
                    i = i + 1
                if abs(padImg[x, y-i] - labelColor) < colorThreshold:
                    #print(padImg[x, y-i])
                    cvFloodFill(padImg, height, width, seedPosition, fillColor)
                else:
                    #print(padImg[x, y-i])
                    cvFloodFill(padImg, height, width, seedPosition, labelColor)
                j = j + 1
                fname = 'pig_after_' + str(j) + 'main_filling.png'
                cv2.imwrite(os.path.join(savePath, fname), padImg.astype('uint8'), [int(cv2.IMWRITE_PNG_COMPRESSION), 0])

    resultImg = cropAndReverse(padImg, height, width, backGroundColor, labelColor)
    cv2.imwrite(os.path.join(savePath, 'pig_final.png'), resultImg.astype('uint8'), [int(cv2.IMWRITE_PNG_COMPRESSION), 0])

def holeFill_main():
    boundaryColor = 255
    fillColor = 128  # for practice
    labelColor = 80
    backGroundColor = 0
    input_path = INPUT_PATH
    output_path_fill = OUTPUT_PATH_FILL
    for root, dirs, files in os.walk(input_path):
        for f in files:
            holesInHoles(os.path.join(input_path, f), output_path_fill, backGroundColor, boundaryColor, labelColor, fillColor)



if __name__ == '__main__':
    holeFill_main()


