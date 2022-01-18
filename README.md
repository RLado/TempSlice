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

# csv-fft
### Utility to plot an unrefined fft from slice2csv files

Help output:
```
usage: csv-fft.py [-h] -f SAMPLE_RATE -i INPUT [INPUT ...] [-o OUTPUT] [-od OUTPUT_DATA] [--dpi DPI] [-c FREQ_CAP FREQ_CAP] [-m {abs,imag}] [-s {log,mag}] [--data_col {avg,lub,ulb}] [-w {none,hamming,bartlett,blackman,hanning}]

Plots the fft(s) of the input slices csv

required arguments:
  -f SAMPLE_RATE, --sample_rate SAMPLE_RATE
                        Sample rate in Hz (or fps)
  -i INPUT [INPUT ...], --input INPUT [INPUT ...]
                        List of input files

optional arguments:
  -o OUTPUT, --output OUTPUT
                        Path for the output graph
  -od OUTPUT_DATA, --output_data OUTPUT_DATA
                        Path for csv output files
  --dpi DPI             Output graph dpi
  -c FREQ_CAP FREQ_CAP, --freq_cap FREQ_CAP FREQ_CAP
                        Frequency graph cutoff as: start end
  -m {abs,imag}, --mode {abs,imag}
                        Path for the output graph
  -s {log,mag}, --scale {log,mag}
                        Enable logarithmic scale on the y axis
  --data_col {avg,lub,ulb}
                        Data column to be used for fft, by default averages both columns
  -w {none,hamming,bartlett,blackman,hanning}, --window {none,hamming,bartlett,blackman,hanning}
                        Apply window before FFT
```

# threshold-slice
### Thresholds a slice to black and white, to improve wave detection

Help output:
```
usage: threshold-slice.py [-h] -t THRESHOLD -i INPUT -o OUTPUT [-v VERBOSE]

Thresholds a slice to black and white, to improve wave detection

required arguments:
  -t THRESHOLD, --threshold THRESHOLD
                        Grayscale limit for thresholding
  -i INPUT, --input INPUT
                        Input file
  -o OUTPUT, --output OUTPUT
                        Path for output file

optional arguments:
  -v VERBOSE, --verbose VERBOSE
                        Shows both the original and the thresholded images
```

# csv-specgram
### Plots the spectrogram of the input slice csv

Help output:
```
usage: csv-specgram.py [-h] -f SAMPLE_RATE -i INPUT [-o OUTPUT] [--dpi DPI] [-c FREQ_CAP FREQ_CAP] [-s {log,mag}] [--data_col {avg,lub,ulb}] [-w {none,hamming,bartlett,blackman,hanning}]

Plots the spectrogram of the input slice csv

required arguments:
  -f SAMPLE_RATE, --sample_rate SAMPLE_RATE
                        Sample rate in Hz (or fps)
  -i INPUT, --input INPUT
                        List of input files

optional arguments:
  -o OUTPUT, --output OUTPUT
                        Path for the output graph
  --dpi DPI             Output graph dpi
  -c FREQ_CAP FREQ_CAP, --freq_cap FREQ_CAP FREQ_CAP
                        Frequency graph cutoff as: start end
  -s {log,mag}, --scale {log,mag}
                        Enable logarithmic scale on the y axis
  --data_col {avg,lub,ulb}
                        Data column to be used for fft, by default averages both columns
  -w {none,hamming,bartlett,blackman,hanning}, --window {none,hamming,bartlett,blackman,hanning}
                        Apply window before FFT

```

# csv-smooth
### Smoothes data from a csv using a cubic spline approximation

```
usage: csv-smooth.py [-h] -i INPUT [-o OUTPUT] [--data_col {avg,lub,ulb}] [-s SMOOTH] [-p PLOT]

Smoothens data from a csv using a cubic spline approximation

required arguments:
  -i INPUT, --input INPUT
                        List of input files

optional arguments:
  -o OUTPUT, --output OUTPUT
                        Path for the output file
  --data_col {avg,lub,ulb}
                        Data column to be used for fft, by default averages both columns
  -s SMOOTH, --smooth SMOOTH
                        Smoothing factor [0-1]. Defaults to 0.85.
  -p PLOT, --plot PLOT  Plot the resulting function
```