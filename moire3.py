import numpy as np
import matplotlib.pyplot as mp
import scipy.ndimage.filters as ndfilt
import scipy.ndimage.interpolation as ndint


fig = mp.figure(figsize=(8,10))
T = 30       # grating period in pixels. 
mag = 3      # magnification factor
offset = 256 # offset in pixels of the altered image


def grating(phaseImage):
    """ 
    Convert phaseImage into grating image scaled between 0 and 1
    """
    return 1/(1+np.exp(5*np.cos(2*np.pi*phaseImage)))


def show(sub, img, title):
    """
    display the image
    """
    mp.subplot(sub)
    mp.imshow(img)
    mp.axis('off')
    mp.title(title)


# load image and magnify
img = mp.imread('./images/audrey512.png')
img = ndfilt.gaussian_filter(img, (T/4.0/mag, T/4.0/mag, 0))
img = ndint.zoom(img,(mag,mag,1))
show(311, img, 'original')
h,w,d = img.shape

# carrier phase image: horizontal gradient with slope 1/T
g = np.tile(np.r_[0.0:w].reshape(1,w,1), (h+offset,1,3))/T

# iterative adjustment of gratings to images
L = 0.04    # learning rate
M = 20      # multi-res iteration period
niter = 1001;  # of iterations
for i in range(niter):
    # randomize offset for smoothness
    err = (1-img)/2 - (g[0:-offset,:,:] - g[offset:,:,:])

    # multires iteration to improve convergence
    if i%M==0:
        print 'Iteration %4d/%5d' % (i,niter) 
        err = M*ndfilt.gaussian_filter1d(err, sigma=T/6.0, axis=0, mode='constant')

    # update gratings
    g[0:-offset,:,:] += L*err
    g[offset:,:,:]   -= L*err

g = grating(g)

# visualize gratings 
show(312, g, 'grating')

# visualize superpositions
e = np.ones((offset,w,d))
s = np.concatenate((e,g),0)*np.concatenate((g,e),0) 
show(313, s, 'superposition')

fig.savefig('./results/moire3.png', dpi=300)
