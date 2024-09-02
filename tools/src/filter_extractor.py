# ################################################################################
# Reconhecimento pela contribuição de Mark Setchell
# https://stackoverflow.com/questions/66150060/how-to-read-photoshop-curves-acv-files-in-python

# Realizou as funções loadCurvesFilter, loadHSLFilter e loadFilter

# fauxtoshop - does some things like Adobe Photoshop

# Mark Setchell (mark@thesetchells.com)

# Reads, interprets and possibly applies Photoshop files:

# - Curves files (*.acv)
# - Hue Saturation files (*.ahu)
# ################################################################################

import sys
#import numpy
from struct import unpack

def loadFilter(filename):

    if filename.lower().endswith('.acv'):
        loadCurvesFilter(filename)
        return

    if filename.lower().endswith('.alv'):
        loadLevelsFilter(filename)
        return

    if filename.lower().endswith('.acf'):
        loadKernelFilter(filename)
        return

    if filename.lower().endswith('.ahu'):
        loadHSLFilter(filename)
        return

    sys.exit(f'ERROR: Unknown file extension {filename}')

def loadCurvesFilter(filename):

    with open(filename, 'rb') as f:
       
       version, ncurves = unpack('>HH', f.read(4))
       print(f'File: {filename}')
       print(f'Version: {version}')
       if version != 4:
          sys.exit('ERROR: Cowardly refusing to read version other than 4')
       print(f'Curve count: {ncurves}')
       curves = []
       for c in range(ncurves):
          npoints, = unpack('>H', f.read(2))

          print(f'Curve: {c}, {npoints} points follow:')
          curve = []
          for p in range(npoints):
             y, x = unpack('>HH', f.read(4))
             print(f'Curve: {c}, point: {p}, x={x}, y={y}')
             curve.append((x,y))
          curves.append(curve)
    return curves

def loadLevelsFilter(filename):
    with open(filename, 'rb') as f:
        version, min_balck_tons = unpack('>HH', f.read(4))
        print(f'File: {filename}')
        print(f'Version: {version}')
        print(f'Black tons: {min_balck_tons}')
        if version != 2:
          sys.exit('ERROR: Cowardly refusing to read version other than 2')
        min_white_tons, _ = unpack('>hh', f.read(4))
        print(f'White tons: {min_white_tons}')
        floor_value_x, gamma, floar_value_y = unpack('>hhh', f.read(6))
        print(f'Out values: {(floor_value_x,floar_value_y )}')
        print(f'Gamma: {gamma}')

    return #levels

def loadKernelFilter(filename):
    sys.exit("ERROR: Kernel filter not yet implemeted")

def loadHSLFilter(filename):

    with open(filename, 'rb') as f:
       version, usage, pad = unpack('>HBB', f.read(4))
       print(f'File: {filename}')
       print(f'Version: {version}')
       if version != 2:
          sys.exit('ERROR: Cowardly refusing to read version other than 2')
       if usage == 0:
           print('Usage: Hue adjustment')
       else:
           print('Usage: Colorization')
           sys.exit(f'ERROR: Cowardly refusing to apply colorization rather than Hue adjustment')
       MasterHue, MasterSaturation, MasterLightness = unpack('>HHH', f.read(6))
       print(f'Master Hue: {MasterHue}')
       print(f'Master Saturation: {MasterSaturation}')
       print(f'Master Lightness: {MasterLightness}')
       # There follow 6 hextants, each with 4 range values and 3 settings values
       for h in range(6):
           ranges = unpack('>HHHH',f.read(8))
           settings = unpack('>HHH', f.read(6))
           print(f'Hextant: {h}, ranges: {ranges}, settings: {settings}')
           
if __name__ == '__main__':

   if len(sys.argv) not in set([2,3]):
      print('Usage: {sys.argv[0]} filter.[acv|ahu|alv|acf] [image]', file=sys.stderr)
      sys.exit(1)

   if len(sys.argv) == 2:
      loadFilter(sys.argv[1])