from PIL import Image, ImageDraw
import argparse
import csv
import math
import os


def main():
    # Argument parser
    parser = argparse.ArgumentParser(
        description='Converts a slice into a csv file by thresholding upper and lower color to find a waveform in it\'s boundary.')
    parser._action_groups.pop()
    required = parser.add_argument_group('required arguments')
    optional = parser.add_argument_group('optional arguments')

    # Datasets parameters
    required.add_argument('-u', '--upper', type=int, nargs=2,
                          help='Upper pixel example coordinates as x y', required=True)
    required.add_argument('-l', '--lower', type=int, nargs=2,
                          help='Lower pixel example coordinates as x y', required=True)
    #required.add_argument('-z', '--zero', type=int, help='Mid point of the wave in pixels as y', required=True)
    required.add_argument('-t', '--threshold', type=float,
                          help='Maximum colour difference', required=True)
    required.add_argument('-i', '--input', type=str,
                          nargs='+', help='List of input files', required=True)
    required.add_argument('-o', '--output', type=str,
                          help='Path for csv output files', required=True)
    optional.add_argument('-v', '--verbose', type=bool, default=False,
                          help='Shows the waveform detected over the image. Red=upper point, Green=lower point, Blue=average')
    optional.add_argument('-vs', '--verbose_save', type=bool, default=False,
                          help='Saves the waveform detected over the image.(verbose flag must be True)')

    args = parser.parse_args()

    ###

    for img in args.input:
        im = Image.open(img)
        im_width, im_height = im.size
        upper_c = im.getpixel(tuple(args.upper))
        lower_c = im.getpixel(tuple(args.lower))

        if args.verbose:
            im_d = im.copy()
            draw = ImageDraw.Draw(im_d)

        with open(f'{os.path.join(args.output, os.path.basename(img))}.csv', 'w', newline='') as csvfile:
            csvwriter = csv.writer(
                csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            csvwriter.writerow(
                ['time', 'upper lower band pixel', 'lower upper band pixel'])

            # Column by column get a point of the waveform.
            #   Getting the upermost pixel of the lower band and the lowermost pixel of the upper band and average the result
            for x in range(im_width):
                # uppermost lower band (upper left corner is 0,0)
                ulb = im_height
                lub = 0  # lowermost upper band
                for y in range(im_height):
                    pixc = im.getpixel((x, y))
                    if math.dist(pixc, upper_c) <= args.threshold:
                        if lub < y:
                            lub = y
                    if math.dist(pixc, lower_c) <= args.threshold:
                        if ulb > y:
                            ulb = y
                # Write waveform point in csv
                csvwriter.writerow([x, ulb, lub])

                # Draw if necessary
                if args.verbose:
                    draw.point((x, ulb), fill="red")
                    draw.point((x, lub), fill="green")
                    draw.point((x, (ulb+lub)/2), fill="blue")
        if args.verbose:
            im_d.show()
        if args.verbose and args.verbose_save:
            im_d.save(
                f'{os.path.join(args.output, os.path.basename(img))}_slice2csv.png')
        im.close()

    return 0


if __name__ == '__main__':
    main()
