![caitlin grid](dope_logo.png)

Code associated with (1) overlaying a grid and (2) extracting frames from videos for Caitlin.

### `add_grid.py`

`add_grid.py` is the only thing you need to worry about. It takes two arguments:
  - __-i__: the input video
  - __-m__: the number of minutes in between extracted frames

The locations of the lines are hardcoded in the script but this could be easily changed.

To get the example video and generate the output shown in the `examples` folder, do the following:

> `git clone https://github.com/lukereding/caitlin_grid.git` # clone this repo       
`cd caitlin_grid`    # cd into the folder      
`wget https://dl.dropboxusercontent.com/u/20577270/ch08_20161116113000.mp4 ` # download the video        
`mv ch08_20161116113000.mp4 example.mp4 ` # rename the video     

Then run the program like:

`python add_grid.py -i ./example/example.mp4 -m 1`

This line results in frames spaced one minute apart. We can confirm this is the case by looking at the timestamps in the photos in the `example` folder: each is one minute apart. These frame same dimensions as the video and are numbered like `example_0000.jpg`, `example_0001.jpg`, and so on, where `example` is the name of the video. The frames are saved in the directory containing the video file.


To run a bunch of videos in parallel using GNU `parallel`, run:

`ls *.mp4 | gtime parallel -j+0 --eta 'python add_grid.py -i {} -m 1 2>&1 {.}.log'`

Requires OpenCV, numpy, sys, os, and argparse modules (and all dependencies).

### frame_extract.py

`frame_extract.py` is a simpler version of `add_grid.py` that _just_ extracts frames and doesn't add an sort of a grid. Created for Mary to use with her FRI kids.

It takes two arguments:
  - __-i__: the input video
  - __-m__: the number of seconds in between extracted frames. Defaults to 15.


  To run a bunch of videos in parallel using GNU `parallel`, run:

  `ls *.mp4 | gtime parallel -j+0 --eta 'python frame_extract.py -i {} -s 15 2>&1 {.}.log'`


Actually, this is a more efficient way of doing things. It using `find` to look only in folders that match `Grp[0-9]*all` and only takes the `*.mov` files that start with `G` (there are some files named things like `._Group1_femagg_Xnig_SM_obs5_per5_5min.mov` that I don't want to use). 

```{bash}

find . -path "*/Grp[0-9]*all/G*.mov" -maxdepth 2 | parallel -j+0 --eta 'python ~/Documents/caitlin_grid/frame_extract.py -i {} -s 15'

 ```