import argparse
import sys
from params import defaults

DESC='''Dump out GCode for calibrating E-step (i.e. How many steps per mm?).

Based on https://mattshub.com/blogs/blog/extruder-calibration.'''

GCODE_TEMPLATE ='''; Don't forget to:
; 1. Mark {md}mm of filament
; 2. Take note of initial e-step (M503 on Marlin)
G28 ; Go home
G90 ; Absolute mode
G1 Z50 ; Move to Z = 50mm to make space for extruded material
M83 ; Relative mode
M109 S{temp} T{idx}; Set and wait for target temperature
G1 F50 ; Decrease feed rate to remove slip from equation
G1 E{ed} ; Try to extrude {ed}mm
M104 S0 T{idx} ; Turn off hotend
; Now, measure leftover distance'''

parser = argparse.ArgumentParser(description=DESC, formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument('--target_temp', type=int, required=True, help='Extrusion temperature to calibrate at.')
parser.add_argument('--tool_index', type=int, default=0, help='Index of the extruder to use.')
parser.add_argument('--extrusion_distance', type=int, default=defaults.EXTRUDE_MM, help='Distance to extrude.')
parser.add_argument('--mark_distance', type=int, default=defaults.MARK_MM, help='Distance to mark the filament at.')

args = parser.parse_args()
if args.mark_distance < args.extrusion_distance:
    print('Marked distance ({md}mm) cannot be smaller than extrusion distance ({ed}mm)'.format(md=args.mark_distance, ed=args.extrusion_distance))
    sys.exit(1)

print(GCODE_TEMPLATE.format(md=args.mark_distance, idx=args.tool_index, temp=args.target_temp, ed=args.extrusion_distance))
