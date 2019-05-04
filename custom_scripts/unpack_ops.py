
import matplotlib

import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import optparse
matplotlib.use('Agg')
import numpy as np
import sys
import os
import json

parser = optparse.OptionParser()

# PATH opts:
parser.add_option('-D', '--root', action='store', dest='rootdir', default='/n/coxfs01/2p-data', help='source dir (root project dir containing all expts) [default: /n/coxfs01/2p-data]')
parser.add_option('-i', '--animalid', action='store', dest='animalid', default='', help='Animal ID')
parser.add_option('-S', '--session', action='store', dest='session', default='', help='session dir (format: YYYMMDD_ANIMALID') 
parser.add_option('-A', '--acq', action='store', dest='acquisition', default='', help="acquisition folder (ex: 'FOV1_zoom3x')")
parser.add_option('-R', '--run', action='store', dest='run', default='', help='name of run to process') 
parser.add_option('-Y', '--analysis', action='store', dest='analysis_header', default='', help='Analysis to process. [ex: suite2p_analysis001]')


(options, args) = parser.parse_args() 

#get options
rootdir = options.rootdir
animalid = options.animalid
session = options.session
acquisition = options.acquisition
run = options.run
analysis_header = options.analysis_header

 
#figure out directories to search
data_dir = os.path.join(rootdir,animalid,session,acquisition,run)
analysis_dir = os.path.join(data_dir,analysis_header)
ops_dir = os.path.join(analysis_dir,'suite2p')
output_dir = os.path.join(analysis_dir,'suite2p','plane0')

#make figure directory
fig_dir = ops_dir
#get file
ops_file = os.path.join(ops_dir,'ops1.npy')
ops_data = np.load(ops_file)


#get rid of images in dictionary
tmp = ops_data[0].copy()
for x in ops_data[0]:
    if isinstance(tmp[x],np.ndarray):
        if tmp[x].size > 100:
            print(x)
            del tmp[x]
        else:
            tmp[x] = tmp[x].tolist()
    elif isinstance(tmp[x],np.int32):
        tmp[x] = int(tmp[x])

#dump to json
with open(os.path.join(ops_dir,'ops1.json'), 'w') as fp:
	json.dump(tmp, fp, indent=4)


#saving some images to dictionary

#MEAN IMAGE
M = ops_data[0]['meanImg']

dpi = 80
szY,szX = M.shape
# What size does the figure need to be in inches to fit the image?
figsize = szX / float(dpi), szY / float(dpi)

# Create a figure of the right size with one axes that takes up the full figure
f = plt.figure(figsize=figsize)
ax = f.add_axes([0, 0, 1, 1])

# Hide spines, ticks, etc.
ax.axis('off')

ax.imshow(M,'gray')
f.savefig(os.path.join(fig_dir,'meanImg.png'), dpi=dpi, transparent=True)
plt.close()

#MEAN IMAGE ENHANCED
M = ops_data[0]['meanImgE']

dpi = 80
szY,szX = M.shape
# What size does the figure need to be in inches to fit the image?
figsize = szX / float(dpi), szY / float(dpi)

# Create a figure of the right size with one axes that takes up the full figure
f = plt.figure(figsize=figsize)
ax = f.add_axes([0, 0, 1, 1])

# Hide spines, ticks, etc.
ax.axis('off')

ax.imshow(M,'gray')
f.savefig(os.path.join(fig_dir,'meanImgE.png'), dpi=dpi, transparent=True)
plt.close()

#CORRELATION IMAGE
M = ops_data[0]['Vcorr']

dpi = 80
szY,szX = M.shape
# What size does the figure need to be in inches to fit the image?
figsize = szX / float(dpi), szY / float(dpi)

# Create a figure of the right size with one axes that takes up the full figure
f = plt.figure(figsize=figsize)
ax = f.add_axes([0, 0, 1, 1])

# Hide spines, ticks, etc.
ax.axis('off')

ax.imshow(M,'gray')
f.savefig(os.path.join(fig_dir,'Vcorr.png'), dpi=dpi, transparent=True)
plt.close()
