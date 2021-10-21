# TempSlice 
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