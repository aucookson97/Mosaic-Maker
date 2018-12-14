import cv2
import csv
import numpy as np
from math import ceil, sqrt

# INPUTS
mosaic_width_inches = 24
color_palette = ("BLACK", "BLUE (III)", "BLUE-GREEN", "BLUE_VIOLET",
                    "BROWN", "CARNATION PINK", "GREEN", "ORANGE",
                    "RED", "RED-ORANGE", "RED-VIOLET", "VIOLET",
                    "WHITE", "YELLOW", "YELLOW-GREEN", "YELLOW-ORANGE")


CRAYON_DIMENSIONS = (3.625, .3125) # Length, Diameter in Inches
MIN_CRAYON_LENGTH = .4 # Tip Length in Inches

file_crayola = "crayons.csv"
file_color = "RealSenseImages\\testImage2_Color.png"
file_depth = "RealSenseImages\\testImage2_Depth.png"

img_rgb = cv2.imread(file_color)
img_depth = cv2.imread(file_depth)

color_buckets = {}

def generateMosaic():

    aspect_ratio = img_rgb.shape[1] / img_rgb.shape[0]
    mosaic_height_inches = mosaic_width_inches / aspect_ratio

    mosaic_dimensions = (ceil(mosaic_width_inches / CRAYON_DIMENSIONS[1]), # Width, Height
                         ceil((mosaic_height_inches / CRAYON_DIMENSIONS[1]) * sqrt(3)*(2.0/3.0)))

    print (img_rgb.shape)
    print (mosaic_dimensions)

    img_depth_hsv = cv2.cvtColor(img_depth, cv2.COLOR_BGR2HSV)
    img_rgb_hsv = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2HSV)

    img_preview = cv2.imread(file_depth)#np.ones((720, 1280, 3), np.uint8) * 255


    radius = (img_rgb.shape[1] / mosaic_dimensions[0]) / 2.0

##        print (radius)
    for i in range(mosaic_dimensions[0]):
        for j in range(mosaic_dimensions[1]):
            
            if (j % 2 == 0):
                if (i == mosaic_dimensions[0] - 1):
                    continue
                center = (int(radius + i * radius * 2.0), int(radius + j * radius * sqrt(3)))
            else:
                center = (int(radius*(2) + i * radius * 2.0), int(radius + j * radius * sqrt(3)))
            cv2.circle(img_preview, center, int(radius), 1, thickness = 1)
####            img = np.zeros((720, 1280, 3), np.uint8)
####            #mask = cv2.circle(img, center, int(radius), 1, thickness = -1)
##            mask = mask.astype('uint8')
##            masked_data = cv2.bitwise_and(img_depth, img_depth, mask=mask)
##            cv2.imshow("mask", masked_data)
##            cv2.waitKey(0)

    
    cv2.imshow("Preview", img_preview)
    cv2.resizeWindow("Preview", (1280, 720))


def loadColors():
    with open(file_crayola, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')

        for row in reader:
            if (row[0].upper() in color_palette):
                color_buckets[row[0].upper()] = hexToRGB(row[1][1:])

def hexToRGB(hex_num):
    hex_num = int(hex_num, 16)
    r = int((hex_num >> 16) & 0xFF)
    g = (hex_num >> 8) & 0xFF
    b = (hex_num) & 0xFF

    return (r, g, b)

if __name__=="__main__":
    loadColors()
    generateMosaic()
