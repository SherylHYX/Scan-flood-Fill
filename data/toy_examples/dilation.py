import numpy as np
import cv2
import os

INPUT_PATH = 'F:/Scan-flood-Fill/data/ toy_examples/ input_200'
OUTPUT_PATH_FILL = 'F:/Scan-flood-Fill/data/ toy_examples/input_toy/'
colorThreshold = 30

def dilation(inputPath, savePath, boundaryColor, d):
    #print(inputPath)
    img = cv2.imread(inputPath, 0)
    height, width = img.shape[:2]
    result = np.zeros([height * d, width * d])
    for x in range(height):
        for y in range(width):
            if abs(img[x,y] - boundaryColor) < colorThreshold:
                #fill the rectangle
                for i in range(d*x, d*(x+1)):
                    for j in range(d*y, d*(y+1)):
                        result[i,j] = boundaryColor
    cv2.imwrite(savePath, result, [int(cv2.IMWRITE_JPEG_QUALITY), 100])

def dilation_main():
    boundaryColor = 255
    for d, n in enumerate(range(200, 2200, 200)):
        output_folder_name = 'input_' + str(n)
        input_folder_name = 'input_' + str(200)
        input_path = os.path.join(INPUT_PATH, input_folder_name)
        output_path_fill = os.path.join(OUTPUT_PATH_FILL, output_folder_name)
        for root, dirs, files in os.walk(input_path):
            for f in files:
                dilation(os.path.join(input_path, f), os.path.join(output_path_fill, f), boundaryColor, d+1)

if __name__ == '__main__':
    dilation_main()