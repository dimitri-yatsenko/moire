import numpy as np
import matplotlib.pyplot as mp
import scipy.ndimage.filters as ndfilt
import scipy.ndimage.interpolation as ndint


fig = mp.figure(figsize=(8,10))
T = 20     # grating period in pixels
mag = 2    # magnification factor


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
img = mp.imread('./images/audrey512.png')
img = ndint.zoom(img,(mag,mag,1))
img = ndfilt.gaussian_filter(img, (T/4,T/4,0))
show(311, img, 'original')
h,w,d = img.shape

# generate gratings
carrier = np.tile(np.r_[0.0:w].reshape(1,w,1), (h,1,3))/T
grating1 = grating(carrier-(1-img)/4)
grating2 = grating(carrier+(1-img)/4)

# visualize gratings and their superposition
show(323, grating1, 'grating 1')
show(324, grating2, 'grating 2')
show(313, grating1*grating2, 'superposition')

fig.savefig('./results/moire1.png', dpi=300)
