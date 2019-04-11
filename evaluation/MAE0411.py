# coding: utf-8
import numpy as np
import cv2
import os

GT_PATH = 'F:/fill_boundary/MSRA10K_Imgs_GT/MSRA10K_Imgs_GT/Imgs_gt'
EFCI_PATH = 'F:/fill_boundary/MSRA10K_Imgs_GT/MSRA10K_Imgs_GT/EFCI_results'
SCAN_PATH = 'F:/fill_boundary/MSRA10K_Imgs_GT/MSRA10K_Imgs_GT/Scan_flood_fill_results'
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
    for x in range(height-2):
        for y in range(width-2):
            # label is the color that is temporarily used to fill exterior
            if croppedImg[x,y] == labelColor:
                croppedImg[x,y] = backGroundColor
            if croppedImg[x, y] == 128:
                croppedImg[x, y] = 255
    return croppedImg
    #return np.delete((np.delete(img, [0, width-1], axis=1)), [0, height-1], axis=0)

def cvFloodFill(img, height, width, seedPosition, fillColor):
    mask = np.zeros([height+2, width +2], np.uint8)
    cv2.floodFill(img, mask, seedPosition, newVal = fillColor, loDiff = 20, upDiff = 20, flags = 4)

def mae_details(gtPath, scanPath, efciPath):
    gt = cv2.imread(gtPath, 0)
    height, width = gt.shape[:2]
    scan = cv2.imread(scanPath, 0)
    efci = cv2.imread(efciPath, 0)
    scan_diff = scan - gt
    efci_diff = efci - gt
    num_of_elements = height * width
    efci_mae = 1.0*np.count_nonzero(efci_diff)/ num_of_elements
    scan_mae = 1.0*np.count_nonzero(scan_diff)/ num_of_elements
    return efci_mae, scan_mae


def mae_main():
    mae_full = np.zeros([9918, 3])
    for root, dirs, files in os.walk(SCAN_PATH):
        for i, f in enumerate(files):
            efci_mae, scan_mae = mae_details(os.path.join(GT_PATH, f), os.path.join(SCAN_PATH, f), os.path.join(EFCI_PATH, f))
            filepath, fullflname = os.path.split(f)
            fname, ext = os.path.splitext(fullflname)
            mae_full[i, 0] = fname
            mae_full[i, 1] = efci_mae
            mae_full[i, 2] = scan_mae
    mae = [np.mean(mae_full[:, 1]), np.mean(mae_full[:, 2])]
    print("MAE for EFCI and Scan-flood Fill is respectively: ")
    print(mae)
    np.savetxt("mae_full.csv", mae_full, delimiter=",")


if __name__ == '__main__':
    mae_main()


