import argparse
import sys
import math
from params import defaults

DESC='''Generate GCode for volumetric flow rate performance.

Based on https://mattshub.com/blogs/blog/extruder-calibration://www.cnckitchen.com/blog/testing-bimetallic-heat-breaks'''

GCODE_HEADER_TEMPLATE ='''; Flow rates: {rates}
G28 ; Go home
G90 ; Absolute mode
G1 Z50 ; Move to Z = 50mm to make space for extruded material
M83 ; Relative mode
M109 S{temp} T{idx}; Set and wait for target temperature
G1 E{init_prime} F{prime_rate}; Prime
G4 S10 ; Wait for primed material to clear
'''

GCODE_BODY_UNRETRACT_TEMPLATE='''G1 E{retract} F{retract_rate}; Unretract
'''
GCODE_BODY_PRIME_TEMPLATE='''G1 E{prime} F{prime_rate}; Prime
G4 S10 ; Wait for primed material to clear
'''

GCODE_BODY_TEMPLATE = '''G1 F{rate} ; Set extrusion speed
G1 E{dist} ; Extrude {dist}mm
G4 S0 ; Brief wait
G1 E-{retract} F{retract_rate} ; Retract
'''

GCODE_FOOTER_TEMPLATE='''M104 S0 T{idx} ; Turn off hotend'''

def calculate_feedrate(flow_rate, diameter, distance):
    cross_section = math.pi * pow(diameter / 2, 2)
    return round(flow_rate * 60 / cross_section)

parser = argparse.ArgumentParser(description=DESC, formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument('--target_temp', type=int, required=True, help='Extrusion temperature to calibrate at.')
parser.add_argument('--tool_index', type=int, default=0, help='Index of the extruder to use.')

parser.add_argument('--target_flowrates', type=float, nargs='+', default=defaults.FLOW_RATES, help='Target volumetric flow rates (mm^3/s)')
parser.add_argument('--filament_diameter', type=float, default=1.75, help='Filament diameter (mm)')
parser.add_argument('--extrusion_distance', type=float, default=100, help='Extrusion distance (mm)')

parser.add_argument('--retract_distance', type=int, required=True, help='Retract distance.')
parser.add_argument('--retract_rate', type=int, default=1000, help='Retract feedrate.')
parser.add_argument('--initial_prime_distance', type=int, default=10, help='Initial prime distance.')
parser.add_argument('--prime_distance', type=int, default=0, help='Prime distance between different rates.')
parser.add_argument('--prime_rate', type=int, default=25, help='Prime feedrate.')

args = parser.parse_args()

print(GCODE_HEADER_TEMPLATE.format(temp=args.target_temp, idx=args.tool_index, init_prime=args.initial_prime_distance, prime_rate=args.prime_rate, rates=args.target_flowrates))
target_speeds = map(lambda x: calculate_feedrate(x, args.filament_diameter, args.extrusion_distance), args.target_flowrates)

for i, s in enumerate(target_speeds):
    print('; Feedrate: {} mm/s'.format(s))
    if i != 0:
        print(GCODE_BODY_UNRETRACT_TEMPLATE.format(retract=args.retract_distance, retract_rate=args.retract_rate))
        if args.prime_distance != 0:
            print(GCODE_BODY_PRIME_TEMPLATE.format(prime=args.prime_distance, prime_rate=args.prime_rate))
    print(GCODE_BODY_TEMPLATE.format(rate=s, dist=args.extrusion_distance, retract=args.retract_distance, retract_rate=args.retract_rate))

print('; Footer')
print(GCODE_FOOTER_TEMPLATE.format(idx=args.tool_index))
