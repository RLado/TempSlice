# tempslice 
### Produces an image containing a column of pixels for every input frame. The number and location of the pixels is chosen by the user by defining a start and end point over the input images. All images must be the same resolution.

<br />

Use:
```bash
python3 tempslice.py -s 560 584 -e 620 584 -i /home/user/image_directory/*.png -o ./example
```

Help output:
```
usage: tempslice.py [-h] -s START START -e END END -i INPUT [INPUT ...] [-o OUTPUT]

Produces a PIL image containing a column of pixels for every input image. The number and location of the pixels is chosen by the user by defining a start and
end point over the input images. All images must be the same resolution.

required arguments:
  -s START START, --start START START
                        Starting point coordinates of the line as x y
  -e END END, --end END END
                        Ending point coordinates of the line as x,y
  -i INPUT [INPUT ...], --input INPUT [INPUT ...]
                        List of input files

optional arguments:
  -o OUTPUT, --output OUTPUT
                        Path for 2 output files containing the slice and the first frame with the slice location. E.g. /home/user/Documents/output_file_name
                        which will result in /home/user/Documents/output_file_name_loc.png & /home/user/Documents/output_file_name_slice.png
```

# slice2csv
### Utility to convert image slices into a csv by thresholding 2 differently colored regions of the slice

Use:
```bash
python3 slice2csv.py -u 203 5 -l 244 32 -t 16 -i ./../demo_vid_IQS/5Hz_50mV_1_amped_slice.png -o ./../demo_vid_IQS/ -v True
```

Help output:
```
usage: slice2csv.py [-h] -u UPPER UPPER -l LOWER LOWER -t THRESHOLD -i INPUT [INPUT ...] -o OUTPUT [-v VERBOSE] [-vs VERBOSE_SAVE]

Converts a slice into a csv file by thresholding upper and lower color to find a waveform in it's boundary.

required arguments:
  -u UPPER UPPER, --upper UPPER UPPER
                        Upper pixel example coordinates as x y
  -l LOWER LOWER, --lower LOWER LOWER
                        Lower pixel example coordinates as x y
  -t THRESHOLD, --threshold THRESHOLD
                        Maximum colour difference
  -i INPUT [INPUT ...], --input INPUT [INPUT ...]
                        List of input files
  -o OUTPUT, --output OUTPUT
                        Path for csv output files

optional arguments:
  -v VERBOSE, --verbose VERBOSE
                        Shows the waveform detected over the image. Red=upper point, Green=lower point, Blue=average
  -vs VERBOSE_SAVE, --verbose_save VERBOSE_SAVE
                        Saves the waveform detected over the image.(verbose flag must be True)
```