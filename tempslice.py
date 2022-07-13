from PIL import Image, ImageDraw
import argparse


def bresenham(start, end):
    """Bresenham's Line Algorithm
    Produces a list of tuples from start and end

    Parameters:
        start (tuple): Start point of the line
        end (tuple): End point of the line

    Returns:
        list: Returns a list containing the coordinates of all the pixels of the
            chosen line. Coordinates are contained in tuples.

    """

    # Setup initial conditions
    x1, y1 = start
    x2, y2 = end
    dx = x2 - x1
    dy = y2 - y1

    # Determine how steep the line is
    is_steep = abs(dy) > abs(dx)

    # Rotate line
    if is_steep:
        x1, y1 = y1, x1
        x2, y2 = y2, x2

    # Swap start and end points if necessary and store swap state
    swapped = False
    if x1 > x2:
        x1, x2 = x2, x1
        y1, y2 = y2, y1
        swapped = True

    # Recalculate differentials
    dx = x2 - x1
    dy = y2 - y1

    # Calculate error
    error = int(dx / 2.0)
    ystep = 1 if y1 < y2 else -1

    # Iterate over bounding box generating points between start and end
    y = y1
    points = []
    for x in range(x1, x2 + 1):
        coord = (y, x) if is_steep else (x, y)
        points.append(coord)
        error -= abs(dy)
        if error < 0:
            y += ystep
            error += dx

    # Reverse the list if the coordinates were swapped
    if swapped:
        points.reverse()
    return points


def tempslice(start, end, imgs):
    """
    Produces a PIL image containing a column of pixels for every input frame. 
    The number and location of the pixels is chosen by the user by defining a 
    start and end point over the input images. All images must be the same 
    resolution.

    Parameters:
        start (tuple): Start point of the line
        end (tuple): End point of the line
        imgs (tuple): List of the image files to be processed

    Returns:
        PIL.Image: PIL image containing a column of pixels for every input frame.

    """

    line_coord = bresenham(start, end)
    slc_g = Image.new('RGBA', (len(imgs), len(line_coord)), (0, 0, 0, 255))
    for i, img in enumerate(imgs):
        im = Image.open(img)
        for gc, ic in enumerate(line_coord):
            slc_g.putpixel((i, gc), im.getpixel(ic))

    return slc_g


def main(args):
    # Slice
    slc = tempslice(args.start, args.end, args.input)
    if args.output != None:
        slc.save(args.output + '_slice.png')
    else:
        slc.show()

    # Draw line over the first frame
    img = Image.open(args.input[0])
    draw = ImageDraw.Draw(img)
    draw.line((args.start[0], args.start[1], args.end[0], args.end[1]), fill=(
        255, 0, 0), width=4)  # width for extra visibility
    if args.output != None:
        img.save(args.output + '_loc.png')
    else:
        img.show()
    
    img.close()


# Main ==========================================================================
if __name__ == '__main__':
    # Argument parser
    parser = argparse.ArgumentParser(description='Produces a PIL image containing a column of pixels for every input image.\
                                     The number and location of the pixels is chosen by the user by defining a\
                                     start and end point over the input images. All images must be the same\
                                     resolution.')
    parser._action_groups.pop()
    required = parser.add_argument_group('required arguments')
    optional = parser.add_argument_group('optional arguments')

    # Datasets parameters
    required.add_argument('-s', '--start', type=int, nargs=2,
                          help='Starting point coordinates of the line as x y', required=True)
    required.add_argument('-e', '--end', type=int, nargs=2,
                          help='Ending point coordinates of the line as x,y', required=True)
    required.add_argument('-i', '--input', type=str,
                          nargs='+', help='List of input files', required=True)
    optional.add_argument('-o', '--output', type=str, help='Path for 2 output files containing the slice and the first frame with the slice location. E.g. /home/user/Documents/output_file_name which will result in /home/user/Documents/output_file_name_loc.png & /home/user/Documents/output_file_name_slice.png')

    args = parser.parse_args()
    
    main(args)
