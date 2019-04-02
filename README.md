# PixEdit

This is a simple image editor to fill a particular need. It currently has two
mode of editing: individual pixel and selected region of interest (defined as
ROI). The basic workflow is:
* select a pixel or a region of interest
* replace it with a new RGB value
* save the image

What not OpenCV? OpenCV has a function call `selectROI()` which allow you to
select a rectangle of region of interest as well. However, the multiple ROI
operation doesn't seem to work, and it also doesn't support `single pixel`
operation, thus warrant this simple DIY script.


## Set it up

This utility has two dependencies: Python 3 and OpenCV (3.x). The version
dependency is not critical: it can work under Python 2 with a bit tweak. 
Here is one way to set it up using Anaconda:

* Install [anaconda](https://www.anaconda.com/)
* Install OpenCV: `conda install opencv`
* Activate either the base or whatever the new environment you desire.


## Operations

To run it:

    python pixel.py rabbit.jpg

You need to switch between image window and console window for most operations:

|     Select ROI      | Replace with new value |
| :-----------------: | :--------------------: |
| ![](rabbit-roi.jpg) |  ![](rabitt-new.jpg)   |
|                     |    ![](console.jpg)    |

* To quit: `ESC` key on the image window
* To select a point: left click mouse button
* To select a region of interest: left click and drag 
* Click elsewhere to deselect previous
* Once a selection is made and ready to replace, on the image window, key in `r`
  or `R`, then go back to console window to type in new RGB value, such as `255
  0 0` and `Enter` to confirm.
* To save the image, key in `s` or `S` on the image window, console window will
  display the new image name, which is composed by old image base name, suffixed
 by `-new`.






