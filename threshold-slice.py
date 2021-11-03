from PIL import Image
import argparse
import os


def main():
    # Argument parser
    parser = argparse.ArgumentParser(
        description='Thresholds a slice to black and white, to improve wave detection')
    parser._action_groups.pop()
    required = parser.add_argument_group('required arguments')
    optional = parser.add_argument_group('optional arguments')

    # Datasets parameters
    required.add_argument('-t', '--threshold', type=float,
                          help='Grayscale limit for thresholding', required=True)
    required.add_argument('-i', '--input', type=str,
                          help='Input file', required=True)
    optional.add_argument('-o', '--output', type=str,
                          help='Path for output file')
    optional.add_argument('-v', '--verbose', type=bool, default=False,
                          help='Shows both the original and the thresholded images')

    args = parser.parse_args()

    ###

    img = Image.open(args.input)
    def fn(x): return 255 if x > args.threshold else 0
    r = img.convert('L').point(fn, mode='1')

    if args.output != None:
        r = r.convert('RGBA')
        r.save(args.output)
        if args.verbose:
            r.show()
            img.show()
    else:
        r.show()
        if args.verbose:
            img.show()
    
    return 0

if __name__ == '__main__':
    main()
