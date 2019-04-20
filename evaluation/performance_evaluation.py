# coding: utf-8
import numpy as np
import cv2
import os

GT_PATH = 'F:/Scan-flood-Fill/data/public_dataset_MSRA10K_Imgs_GT/Imgs_gt'
EFCI_PATH  = 'F:/Scan-flood-Fill/data/public_dataset_MSRA10K_Imgs_GT/EFCI_results'
SCAN_PATH = 'F:/Scan-flood-Fill/data/public_dataset_MSRA10K_Imgs_GT/Scan_flood_Fill_results'

def evaluation_details(gtPath, scanPath, efciPath):
    gt = cv2.imread(gtPath, 0)
    height, width = gt.shape[:2]
    scan = cv2.imread(scanPath, 0)
    efci = cv2.imread(efciPath, 0)
    scan_diff = np.zeros([height, width])#for MAE
    efci_diff = np.zeros([height, width])
    scan_true_positive = 0 #for F1
    efci_true_positive = 0
    for x in range(height):
        for y in range(width):
            if gt[x, y] > 200:
                if scan[x, y] < 50:#for MAE
                    scan_diff[x,y] = -1
                if efci[x, y] < 50:
                    efci_diff[x,y] = -1
                if scan[x, y] > 200:#for F1
                    scan_true_positive = scan_true_positive + 1
                if efci[x, y] > 200:
                    efci_true_positive = efci_true_positive + 1
            if gt[x, y] < 50:#for MAE
                if scan[x, y] > 200:
                    scan_diff[x, y] = 1
                if efci[x, y] > 200:
                    efci_diff[x, y] = 1
    #F1 score below
    scan_nonzero = np.count_nonzero(scan)
    efci_nonzero = np.count_nonzero(efci)
    gt_nonzero = np.count_nonzero(gt)
    scan_precision = scan_true_positive/scan_nonzero
    efci_precision = efci_true_positive/efci_nonzero
    scan_recall = scan_true_positive/gt_nonzero
    efci_recall = efci_true_positive/gt_nonzero
    scan_f1 = 2 * scan_precision * scan_recall/(scan_precision + scan_recall)
    efci_f1 = 2 * efci_precision * efci_recall/(efci_precision + efci_recall)
    #MAE below
    num_of_elements = height * width
    efci_mae = 1.0*np.count_nonzero(efci_diff)/ num_of_elements
    scan_mae = 1.0*np.count_nonzero(scan_diff)/ num_of_elements
    return efci_mae, scan_mae, efci_f1, scan_f1


def evaluation_main():
    mae_full = np.zeros([9918, 3])
    f1_full = np.zeros([9918, 3])
    for root, dirs, files in os.walk(SCAN_PATH):
        for i, f in enumerate(files):
            efci_mae, scan_mae, efci_f1, scan_f1 = evaluation_details(os.path.join(GT_PATH, f), os.path.join(SCAN_PATH, f), os.path.join(EFCI_PATH, f))
            filepath, fullflname = os.path.split(f)
            fname, ext = os.path.splitext(fullflname)
            mae_full[i, 0] = fname
            mae_full[i, 1] = efci_mae
            mae_full[i, 2] = scan_mae
            f1_full[i, 0] = fname
            f1_full[i, 1] = efci_f1
            f1_full[i, 2] = scan_f1
    mae = [np.mean(mae_full[:, 1]), np.mean(mae_full[:, 2])]
    print("MAE for EFCI and Scan-flood Fill is respectively: ")
    print(mae)
    np.savetxt("mae_full.csv", mae_full, delimiter=",")

    f1 = [np.mean(f1_full[:, 1]), np.mean(f1_full[:, 2])]
    print("F1 score for EFCI and Scan-flood Fill is respectively: ")
    print(f1)
    np.savetxt("F1_score_full.csv", f1_full, delimiter=",")


if __name__ == '__main__':
    evaluation_main()


