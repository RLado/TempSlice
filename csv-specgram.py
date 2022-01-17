import matplotlib.pyplot as plt
import numpy as np
import csv
import argparse
import os


def main():
    # Argument parser
    parser = argparse.ArgumentParser(
        description='Plots the spectrogram of the input slice csv')
    parser._action_groups.pop()
    required = parser.add_argument_group('required arguments')
    optional = parser.add_argument_group('optional arguments')

    # Datasets parameters
    required.add_argument('-f', '--sample_rate', type=float,
                          help='Sample rate in Hz (or fps)', required=True)
    required.add_argument('-i', '--input', type=str,
                          nargs=1, help='List of input files', required=True)
    optional.add_argument('-o', '--output', type=str,
                          help='Path for the output graph')
    optional.add_argument('--dpi', type=int, default=600,
                          help='Output graph dpi')
    optional.add_argument('-c', '--freq_cap', type=float, nargs=2,
                          help='Frequency graph cutoff as: start end', required=False)
    optional.add_argument('-s', '--scale', type=str, choices=[
                          'log', 'mag'], default='mag', help='Enable logarithmic scale on the y axis')
    optional.add_argument('--data_col', type=str, choices=['avg', 'lub', 'ulb'], default='avg',
                          help='Data column to be used for fft, by default averages both columns')
    optional.add_argument('-w', '--window', type=str,
                          choices=['none', 'hamming', 'bartlett', 'blackman', 'hanning'], default='none', help='Apply window before FFT')

    args = parser.parse_args()

    ###
    cmap = 'jet'
    plt.rcParams.update({'font.size': 8})

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

    # Name the plot
    plt.subplot(211)
    plt.title(os.path.basename(args.input[0]))

    # Number of sample points
    N = len(frame_num)

    # Check if windowing is necessary
    if (args.window) == 'hamming':
        w = np.hamming(N)
    elif (args.window) == 'bartlett':
        w = np.bartlett(N)
    elif (args.window) == 'blackman':
        w = np.blackman(N)
    elif (args.window) == 'hanning':
        w = np.hanning(N)
    else:
        w = np.ones(N)

    if args.data_col == 'avg':
        plt.subplot(211)
        plt.plot(np.linspace(0, N/args.sample_rate, N), (lub+ulb)/2)
        plt.subplot(212)
        powerSpectrum, frequenciesFound, time, imageAxis = plt.specgram(
            (lub+ulb)/2*w, Fs=args.sample_rate, cmap=cmap)
    elif args.data_col == 'lub':
        plt.subplot(211)
        plt.plot(np.linspace(0, N/args.sample_rate, N), lub)
        plt.subplot(212)
        powerSpectrum, frequenciesFound, time, imageAxis = plt.specgram(
            lub*w, Fs=args.sample_rate, cmap=cmap)
    elif args.data_col == 'ulb':
        plt.subplot(211)
        plt.plot(np.linspace(0, N/args.sample_rate, N), ulb)
        plt.subplot(212)
        powerSpectrum, frequenciesFound, time, imageAxis = plt.specgram(
            ulb*w, Fs=args.sample_rate, cmap=cmap)

    # Cap axis
    plt.subplot(211)
    ax = plt.gca()
    ax.set_xlim(0, N/args.sample_rate)
    # Cap displayed frequency
    if args.freq_cap != None:
        plt.subplot(212)
        ax = plt.gca()
        ax.set_ylim(args.freq_cap)

    plt.subplot(211)
    plt.xlabel('Time [s]')
    plt.ylabel('Amplitude [px]')
    plt.subplot(212)
    plt.xlabel('Time [s]')
    plt.ylabel('Frequency [Hz]')

    if args.scale == 'log':
        plt.subplot(211)
        plt.semilogy()
        plt.subplot(212)
        plt.semilogy()

    plt.subplot(212)
    plt.colorbar(shrink=0.75, location='top')
    plt.grid()
    plt.grid(visible=True, which='minor', linestyle='--')

    if args.output != None:
        plt.tight_layout()
        plt.savefig(args.output, dpi=args.dpi, bbox_inches='tight')
    else:
        plt.tight_layout()
        plt.show()


if __name__ == '__main__':
    main()
