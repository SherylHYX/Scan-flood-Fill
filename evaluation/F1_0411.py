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


def f1_details(gtPath, scanPath, efciPath):
    gt = cv2.imread(gtPath, 0)
    scan = cv2.imread(scanPath, 0)
    efci = cv2.imread(efciPath, 0)
    height, width = gt.shape[:2]
    scan_true_positive = 0
    efci_true_positive = 0
    for x in range(height):
        for y in range(width):
            if gt[x, y] > 200:
                if scan[x, y] > 200:
                    scan_true_positive = scan_true_positive + 1
                if efci[x, y] > 200:
                    efci_true_positive = efci_true_positive + 1
    scan_nonzero = np.count_nonzero(scan)
    efci_nonzero = np.count_nonzero(efci)
    gt_nonzero = np.count_nonzero(gt)
    scan_precision = scan_true_positive/scan_nonzero
    efci_precision = efci_true_positive/efci_nonzero
    scan_recall = scan_true_positive/gt_nonzero
    efci_recall = efci_true_positive/gt_nonzero
    scan_f1 = 2 * scan_precision * scan_recall/(scan_precision + scan_recall)
    efci_f1 = 2 * efci_precision * efci_recall/(efci_precision + efci_recall)
    return efci_f1, scan_f1


def f1_main():
    f1_full = np.zeros([9918, 3])
    for root, dirs, files in os.walk(SCAN_PATH):
        for i, f in enumerate(files):
            efci_f1, scan_f1 = f1_details(os.path.join(GT_PATH, f), os.path.join(SCAN_PATH, f), os.path.join(EFCI_PATH, f))
            filepath, fullflname = os.path.split(f)
            fname, ext = os.path.splitext(fullflname)
            f1_full[i, 0] = fname
            f1_full[i, 1] = efci_f1
            f1_full[i, 2] = scan_f1
    f1 = [np.mean(f1_full[:, 1]), np.mean(f1_full[:, 2])]
    print("F1 score for EFCI and Scan-flood Fill is respectively: ")
    print(f1)
    np.savetxt("F1_score_full.csv", f1_full, delimiter=",")


if __name__ == '__main__':
    f1_main()


