import cv2
import sys
import argparse
import os

'''

Program to extract a frame from a video every -s seconds.

parameters:
-i path to video
-s how often to extract frames, in seconds


Run like: `python frame_extract.py -i example.mp4 -s 15`
to extract frames every 15 seconds.

'''

def parse_arguments():
    """Parse arguments."""
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--inputVideo", required = True, help = "path to the video")
    ap.add_argument("-s", "--seconds", required = True, default = 15, type = int, help = "number of seconds between adjacent output frames")
    args = vars(ap.parse_args())
    video_path = args["inputVideo"]
    seconds = args["seconds"]
    return video_path, seconds

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


if __name__ == "__main__":

    # parse the arguments
    video_path, seconds = parse_arguments()

    # make the vido path absolute
    video_path = os.path.abspath(video_path)

    # error check
    ret = check(video_path)
    if ret == False:
        sys.exit("problem reading in the video file")

    # change working directory
    if os.path.dirname(video_path) != '':
        os.chdir(os.path.dirname(video_path))

    # set up video reader
    cap = cv2.VideoCapture(video_path)

    # set up video writer
    video_name = os.path.basename(video_path)
    name = video_name.split('.')[0]

    # create new dirctory to store frames in
    n = os.path.splitext(video_path)[0]
    if not os.path.exists('{}/'.format(name)):
        os.makedirs('{}/'.format(name))
    os.chdir('{}/'.format(name))

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
        # read in the 1st, seconds * fps frame, etc. with (I think) cap.set(2) = 1, etc.
        frame_number = int(seconds * fps * counter) + 1
        cap.set(1, frame_number)
        # read in the frame
        _, frame = cap.read()
        # save the photo
        c = str(counter).zfill(4)
        cv2.imwrite("{}_{}.jpg".format(name, c), frame)
        # increase the counter
        counter += 1
        print total_frames, frame_number

    cap.release()

    print "saved {} frames from {}".format(counter, video_path)
