#
# Pixel editor
#
# Copyright (C) 2019

import sys
import cv2

img, img2 = None, None
x1, y1, x2, y2 = None, None, None, None
drawing = False
point_click = False

def im_rect(event, x, y, flags, param):
    """ Event handler """
    global x1, y1, x2, y2, drawing, point_click
            
    if event == cv2.EVENT_LBUTTONDOWN:
        x1, y1 = x, y
        x2, y2 = None, None 
        drawing = True 

    if event == cv2.EVENT_MOUSEMOVE and drawing:
        if x1 and y1 and x > x1 and y > y1:
            x2 = x
            y2 = y

    if event == cv2.EVENT_LBUTTONUP:
        x2, y2 = x, y
        if x1 == x2 and y1 == y2:
            point_click = True
            print("Point selected: ({}, {})".format(x, y))
        else:
            point_click = False 
        drawing = False


def main():
    global img, img2, x1,x2,y1,y2,point_click
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

        # draw if valid bounding box is set
        if (x1 and x2 and y1 and y2):
            cv2.rectangle(img2, (x1, y1), (x2, y2), (255, 0, 0), 2)
        
        # show image with bounding box
        cv2.imshow('image', img2)

        # reset image
        img2 = img.copy()

        key = cv2.waitKey(10) & 0xFF 
        
        if key == ord('r') or key == ord('R'):
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

            if point_click:
                img[y1, x1] = bgr 
            else: 
                img[y1:y2, x1:x2] = bgr

            x1, x2, y1, y2 = None, None, None, None
                                   
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