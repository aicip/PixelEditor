#
# Pixel editor
#
# Copyright (C) 2019
#
#
import sys
import cv2
import numpy as np
from enum import Enum

class Shape(Enum):
    POINT   = 1
    RECT    = 2
    POLYGON = 3

shape = Shape.POINT     # default
drawing = False         # enable drawing
img, img2 = None, None
x1, y1, x2, y2 = None, None, None, None
polypoints = []
polyclosed = False

def reset(default_shape=Shape.POLYGON):
    global img, img2, x1, x2, y1, y2, shape, polypoints, polyclosed
    x1, y1, x2, y2 = None, None, None, None
    polypoints.clear()
    shape = default_shape
    drawing = False
    polyclosed = False
    
def im_rect(event, x, y, flags, param):
    """ Event handler """
    global x1, y1, x2, y2, polypoints, drawing, polyclosed
            
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        if shape == Shape.POLYGON:
            # if the new point (x,y) differ from last point
            # recorded, mark the start point for this segment
            if len(polypoints) == 0 or (x, y) != polypoints[-1]:
                polypoints.append([x, y])

        x1, y1 = x, y
        x2, y2 = None, None


    if event == cv2.EVENT_MOUSEMOVE and drawing:

        # for rectangle selection, we force starting point to be top left
        if shape == Shape.RECT and x1 and y1 and x > x1 and y > y1:
            x2 = x
            y2 = y
        
        # for polygon selection, we don't force
        # x2, y2 is the transient point
        if shape == Shape.POLYGON:
            x1, y1 = x2, y2
            x2, y2 = x, y
            
    if event == cv2.EVENT_LBUTTONUP:
                
        if x1 == x and y1 == y and shape == Shape.POINT:
            print("Point selected: ({}, {})".format(x, y))
        
        if x1 and y1 and x > x1 and y > y1 and shape == Shape.RECT: 
            x2, y2 = x, y
            print("BBox selected: ({}, {}), ({}, {})".format(x1, y1, x2, y2))
            drawing = False 

        # mark 
        # if shape == Shape.POLYGON:
        #     x1, y1 = x2, y2

    if event == cv2.EVENT_RBUTTONUP:
        # only useful in POLYGON
        # get the first point
        if len(polypoints) < 2: return
        x_origin, y_origin = polypoints[0]
        if abs(x - x_origin) > 5 and abs(y - y_origin) > 5:
            # current point is far from origin
            # add new point
            polypoints.append([x,y])

        print("Polygon closed:", polypoints)
        polyclosed = True
        drawing = False

def main():
    
    global img, img2, x1, x2, y1, y2, shape, polypoints, polyclosed

    key = 0
    if len(sys.argv) != 2:
        print("\n please provide a filename!")
        sys.exit(1)

    img = cv2.imread(sys.argv[1], cv2.IMREAD_COLOR)
    img2 = img.copy()
    cv2.namedWindow("image")
    cv2.setMouseCallback('image', im_rect)

    # end with ESC (27)
    while not (key == 27):

        if shape == Shape.POINT and x1 and y1:
            cv2.circle(img2, (x1, y1), 3, (255,0,0))
            
        if shape == Shape.RECT and x1 and x2 and y1 and y2:
            cv2.rectangle(img2, (x1, y1), (x2, y2), (255, 0, 0), 2)

        if shape == Shape.POLYGON and x2 and y2 and len(polypoints) > 0:
            
            if polyclosed:
                pts = np.array(polypoints, np.int32)
            else:
                pts = np.array(polypoints + [[x2, y2]], np.int32)

            pts = pts.reshape((-1, 1, 2))
            cv2.polylines(img2, [pts], polyclosed, (255, 0, 0), 2)

            
        # show image with bounding box
        cv2.imshow('image', img2)

        # reset image
        img2 = img.copy()

        key = cv2.waitKey(10) & 0xFF 

        if key == ord('p'):
            print("Drawing mode: point")
            shape = Shape.POINT

        if key == ord('P'):
            print("Drawing mode: polygon")
            shape = Shape.POLYGON

        if key == ord('r'):
            print("Drawing mode: rectangle")
            x1, y1, x2, y2 = None, None, None, None
            shape = Shape.RECT

        if key == ord('c'):
            print("Reset current selection")
            reset()

        if key == ord('R'):
            print("BBox selected: (x1={}, y1={}), (x2={}, y2={})".format(x1,y1,x2,y2))
            while True:
                try:
                    bgr = [int(x) for x in input("Please input replacement value (RGB): ").split()]
                    bgr.reverse()
                    assert (len(bgr)==3)
                except:
                    print("Invalid input")
                else:
                    print("Input Received As: B({}), G({}), R({})".format(bgr[0], bgr[1], bgr[2]))
                    break

            if shape == Shape.POINT:
                img[y1, x1] = bgr 
            
            if shape == Shape.RECT:
                img[y1:y2, x1:x2] = bgr

            if shape == Shape.POLYGON:
                pts = np.array(polypoints, np.int32)
                pts = pts.reshape((-1, 1, 2))
                cv2.fillPoly(img, [pts], bgr)

            reset(default_shape=Shape.POINT)
                               
        if key == ord('s') or key == ord('S'):
            base,ext = sys.argv[1].split('.')
            newfile = base + "-new." + ext
            cv2.imwrite(newfile, img)
            print("Image saved in: ", newfile)
            
        if key == ord('c') or key == ord('C'):
            # cancel selection
            x1,y1,x2,y2=None, None, None, None            
        
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()