import argparse
import sys
from params import defaults

DESC='''Calculate volumetric flow performance.

Based on http://www.cnckitchen.com/blog/testing-bimetallic-heat-breaks'''

parser = argparse.ArgumentParser(description=DESC, formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument('--target_flowrates', type=float, nargs='+', default=defaults.FLOW_RATES, help='Target volumetric flow rates (mm^3/s)')
parser.add_argument('--masses', type=float, nargs='+', help='Extruded masses at corresponding target flow rates.')

args = parser.parse_args()

if len(args.target_flowrates) != len(args.masses):
    print('# masses ({num_masses}) do not correspond to # flow rates ({num_flowrates})'.format(num_flowrates=len(args.target_flowrates), num_masses=len(args.masses)))
    sys.exit(1)

percentages = map(lambda x: 100.0 * x / args.masses[0], args.masses)
print('Extrusion Amount [%], Volumetric Flowrate [mm^3/s]')
for flow_rate, percentage in zip(args.target_flowrates, percentages):
    print('{rate:.2f}, {percent:.1f}' .format(rate=flow_rate, percent=percentage))
