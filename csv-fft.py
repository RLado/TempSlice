import matplotlib.pyplot as plt
import numpy as np
import csv
import argparse
import os


def main():
    # Argument parser
    parser = argparse.ArgumentParser(
        description='Plots the fft(s) of the input slices csv')
    parser._action_groups.pop()
    required = parser.add_argument_group('required arguments')
    optional = parser.add_argument_group('optional arguments')

    # Datasets parameters
    required.add_argument('-f', '--sample_rate', type=float,
                          help='Sample rate in Hz (or fps)', required=True)
    required.add_argument('-i', '--input', type=str,
                          nargs='+', help='List of input files', required=True)
    optional.add_argument('-o', '--output', type=str,
                          help='Path for the output graph')
    optional.add_argument('--dpi', type=int, default=300,
                          help='Output graph dpi')
    optional.add_argument('-c', '--freq_cap', type=float, nargs=2,
                          help='Frequency graph cutoff as: start end', required=False)
    optional.add_argument('-m', '--mode', type=str,
                          choices=['abs', 'imag'], default='abs', help='Path for the output graph')
    optional.add_argument('--data_col', type=str, choices=['avg', 'lub', 'ulb'], default='avg', help='Data column to be used for fft, by default averages both columns')

    args = parser.parse_args()

    ###

    legend = []

    for infile in args.input:
        frame_num = []
        ulb = []
        lub = []
        with open(infile, 'r', newline='') as csvfile:  # args.input()
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

        # Number of sample points
        N = len(frame_num)
        # sample spacing
        T = 1.0 / args.sample_rate

        if args.data_col == 'avg':
            yf = np.fft.fft((lub+ulb)/2)
        elif args.data_col == 'lub':
            yf = np.fft.fft(lub)
        elif args.data_col == 'ulb':
            yf = np.fft.fft(ulb)

        xf = np.fft.fftfreq(N, T)[:N//2]

        if args.freq_cap != None:
            sc = 0
            ec = args.sample_rate
            for j in range(len(xf)):
                if xf[j] <= args.freq_cap[0]:
                    sc = j
                if xf[j] >= args.freq_cap[1]:
                    ec = j
                    break
            xf = xf[sc:ec]
            yf = yf[sc:ec]

        if args.mode == 'abs':
            plt.plot(xf, 2.0/N * np.abs(yf[0:N//2]), linewidth=1)
        elif args.mode == 'imag':
            plt.plot(xf, 2.0/N * np.imag(yf[0:N//2]), linewidth=1)

        legend.append(os.path.basename(infile))

    plt.legend(legend, bbox_to_anchor=(0, 1, 1, 0), ncol=1)
    plt.grid()
    plt.grid(b=True, which='minor', linestyle='--')

    if args.output != None:
        plt.savefig(args.output, dpi=args.dpi, bbox_inches='tight')
    else:
        plt.show()


if __name__ == '__main__':
    main()
