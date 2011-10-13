import numpy as np
import matplotlib.pyplot as mp
import scipy.ndimage.filters as ndfilt
import scipy.ndimage.interpolation as ndint

T = 1./40        # grating period as fraction of image width
mag = 2          # image upsamping factor
hsigma = T/4.   # sigma for gaussian smoothing along horizontal dimension

def grating(phaseImage):
    """
    Convert phaseImage into grating image scaled between 0 and 1
    """
    return 1/(1+np.exp(5*np.cos(2*np.pi*phaseImage)))

def show(sub, img, title):
    """
    paste image in figure
    """
    mp.subplot(sub)
    mp.imshow(img)
    mp.axis('off')
    mp.title(title)

# load image and magnify
print 'pre-processing images...'
img = mp.imread('./images/audrey512.png')
img = ndint.zoom(img, (mag, mag, 1))
T = T*img.shape[1]   # convert to pixels
img = ndfilt.gaussian_filter1d(img, sigma=hsigma*img.shape[1], axis=1)

fig = mp.figure(figsize=(8,10))
show(311, img, 'original')

# generate gratings
print 'generating gratings...'
carrier = np.fromfunction(lambda y,x,d: x/T, img.shape) 
g1 = carrier-(1-img)/4
g2 = carrier+(1-img)/4

# enforce grating smoothness by clipping the laplacian
print 'smoothing...'
maxCurvature = 1e-3/T
for i in range(100):
    avg = (g1[2:,:,:]+g1[:-2,:,:])/2
    g1[1:-1,:,:] = g1[1:-1,:,:].clip(avg-maxCurvature, avg+maxCurvature)
    avg = (g2[2:,:,:]+g2[:-2,:,:])/2
    g2[1:-1,:,:] = g2[1:-1,:,:].clip(avg-maxCurvature, avg+maxCurvature)

g1 = grating(g1)
g2 = grating(g2)

# visualize gratings and their superposition
print 'saving images...'
show(323, g1, 'grating 1')
show(324, g2, 'grating 2')
show(313, g1*g2, 'superposition')

fig.savefig('./results/moire1.png', dpi=300)
