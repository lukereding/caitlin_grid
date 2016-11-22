import cv2
import numpy as np
import sys
import argparse
import os

'''

parameters:
- path to video
- who often to extract frames

steps to be taken:
- check video is the right size
- check that the video can be read
- extract frames at X intervals
- for each extracted video, draw the lines
- save the resulting photos

draw lines:
# 834, 1533 -> 1437, 78
# 363, 519 -> 1878, 1134

written by luke reding
started 21 November 2016
'''



def parse_arguments():
    """Parse arguments."""
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--inputVideo", required = True, help = "path to the video")
    ap.add_argument("-m", "--minutes", required = True, type = int, help = "number of minutes between adjacent output frames")
    args = vars(ap.parse_args())
    video_path = args["inputVideo"]
    minutes = args["minutes"]
    return video_path, minutes

def check(video):
    """Check to make sure the files are as expected."""
    # check to make sure you can read the video
    cap = cv2.VideoCapture(video)
    ret, frame = cap.read()
    # if cap.get(3) != 2048.0 or cap.get(4) != 1536.0:
    #     sys.exit("video is of the wrong dimenisons")
    #     return False
    if ret == False:
        sys.exit("Problem reading the video.")
        return False


def draw_lines(img):
    """Draw each box on img. len(boxes) == # of boxes to draw."""
    cv2.line(img,(834, 1533),(1437, 78),(66,65,172),5)
    cv2.line(img, (363, 519),(1878, 1134),(66,65,172),5)
    return img

if __name__ == "__main__":

    # parse the arguments
    video_path, minutes = parse_arguments()

    # make the vido path absolute
    video_path = os.path.abspath(video_path)

    # error check
    ret = check(video_path)
    if ret == False:
        sys.exit("")

    # change working directory
    if os.path.dirname(video_path) != '':
        os.chdir(os.path.dirname(video_path))

    # set up video reader
    cap = cv2.VideoCapture(video_path)

    # set up video writer
    video_name = os.path.basename(video_path)
    name = video_name.split('.')[0]

    # get size of video
    width = cap.get(3)
    height = cap.get(4)

    # get frame rate
    fps = cap.get(5)
    # get total number of frames
    total_frames = cap.get(7)

    # set variables to use in the loop
    counter = 0
    frame_number = 1

    while frame_number <= total_frames:
        # read in the 1st, minutes * fps * 60th frame, etc. with (I think) cap.set(2) = 1, etc.
        frame_number = (minutes * fps * counter * 60) + 1
        cap.set(1, frame_number)
        _, frame = cap.read()
        # draw the lines
        frame = draw_lines(frame)
        # save the photo
        c = str(counter).zfill(4)
        cv2.imwrite("{}_{}.jpg".format(name, c), frame)
        # increase the counter
        counter += 1
        print total_frames, frame_number

    cap.release()

    print "saved {} frames from {}".format(counter, video_path)
