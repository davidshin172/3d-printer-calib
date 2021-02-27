import argparse
import sys

DESC='''Calibrate flow rate to your printer and filament.

1. Print cube without top, bottom, or infill.
2. Note target extrusion width and number of walls.
3. Measure actual widths of walls. Don't measure from bottom, which may have elephant's foot.
4. Run this tool.

Based on https://www.thingiverse.com/thing:3397997.'''

parser = argparse.ArgumentParser(description=DESC, formatter_class=argparse.RawTextHelpFormatter)

parser.add_argument('--extrusion_width', type=float, required=True, help='Target extrusion width.')
parser.add_argument('--num_walls', type=int, required=True, help='Number of walls.')
parser.add_argument('--measurements', type=float, required=True, nargs='+', help='Number of walls.')

args = parser.parse_args()

if args.num_walls <= 0 or args.extrusion_width <= 0:
    print('Nonsensical width or # walls: {}, {}'.format(args.extrusion_width, args.num_walls))

measured_average = sum(args.measurements) / len(args.measurements)
print('Average thickness: {:.2f}mm'.format(measured_average))
target_thickness = args.extrusion_width * args.num_walls
print('Target thickness: {:.2f}mm'.format(target_thickness))

flow_rate = target_thickness / measured_average
print('Flow rate: {:.0f}%'.format(flow_rate * 100))
