import matplotlib.pyplot as plt
import numpy as np
import csv
import argparse
import os
import csaps


def main():
    # Argument parser
    parser = argparse.ArgumentParser(
        description='Smoothens data from a csv using a cubic spline approximation')
    parser._action_groups.pop()
    required = parser.add_argument_group('required arguments')
    optional = parser.add_argument_group('optional arguments')

    # Datasets parameters
    required.add_argument('-i', '--input', type=str,
                          nargs=1, help='List of input files', required=True)
    optional.add_argument('-o', '--output', type=str,
                          help='Path for the output file')
    optional.add_argument('--data_col', type=str, choices=['avg', 'lub', 'ulb'], default='avg',
                          help='Data column to be used for fft, by default averages both columns')
    optional.add_argument('-s', '--smooth', type=float, default=0.85, help='Smoothing factor [0-1]. Defaults to 0.85.')
    optional.add_argument('-p', '--plot', type=bool, default=False, help='Plot the resulting function')

    args = parser.parse_args()

    ###

    frame_num = []
    ulb = []
    lub = []
    with open(args.input[0], 'r', newline='') as csvfile:  # args.input()
        csvreader = csv.reader(
            csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)

        # Skip headings
        csvreader.__next__()

        # Read file to memory
        for i in csvreader:
            frame_num.append(float(i[0]))
            ulb.append(float(i[1]))
            lub.append(float(i[2]))
        ulb = np.array(ulb)
        lub = np.array(lub)
    
    x=frame_num
    if args.data_col == 'avg':
        y=(lub+ulb)/2
        ys = csaps.csaps(x,y,x,smooth=args.smooth)
    elif args.data_col == 'lub':
        y=lub
        ys = csaps.csaps(x,y,x,smooth=args.smooth)
    elif args.data_col == 'ulb':
        y=ulb
        ys = csaps.csaps(x,y,x,smooth=args.smooth)
    
    if args.output != None:
        with open(args.output, 'w', newline='') as csvfile:
            csvwriter = csv.writer(
                csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            csvwriter.writerow(
                ['time', 'upper lower band pixel', 'lower upper band pixel'])
            for i in range(len(x)):
                csvwriter.writerow([x[i],ys[i],ys[i]])

    if args.plot:
        plt.plot(x,y,x,ys)
        plt.legend(['original','smoothed'])
        plt.show()

if __name__ == '__main__':
    main()
