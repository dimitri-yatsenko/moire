import numpy as np
import matplotlib.pyplot as mp
import scipy.ndimage.filters as ndfilt
import scipy.ndimage.interpolation as ndint


fig = mp.figure(figsize=(8,10))
T = 30       # grating period in pixels. 
mag = 2      # magnification factor
offset = 128 # offset in pixels of the altered image


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
img1 = mp.imread('./images/audrey512.png')
img2 = mp.imread('./images/mona512.png')
img1 = ndint.zoom(img1,(mag,mag,1))
img2 = ndint.zoom(img2,(mag,mag,1))
img1 = ndfilt.gaussian_filter(img1, (T/4,T/4,0))
img2 = ndfilt.gaussian_filter(img2, (T/4,T/4,0))
show(321, img1, 'original')
show(322, img2, 'original')
h,w,d = img1.shape

# carrier phase image: horizontal gradient with slope 1/T
carrier = np.tile(np.r_[0.0:w].reshape(1,w,1), (h+offset,1,3))/T
g1 = carrier
g2 = carrier.copy()

# iterative adjustment of gratings to images
L = 0.01    # learning rate
M = 16      # multi-res iteration period
for i in range(5001):
    # randomize offset for smoothness
    err1 = (1-img1)/2 - (g1[0:-offset,:,:] - g2[offset:,:,:])
    err2 = (1-img2)/2 - (g2[0:-offset,:,:] - g1[offset:,:,:])

    # smooth error occasinally to ensure smootheness of gratings
    if i%M==0:
        print 'Iteration', i
        err1 = M*ndfilt.gaussian_filter1d(err1, sigma=T/6.0, axis=0, mode='constant')
        err2 = M*ndfilt.gaussian_filter1d(err2, sigma=T/6.0, axis=0, mode='constant')

    # update gratings
    g1[0:-offset,:,:] += L*err1
    g2[offset:,:,:]   -= L*err1
    g2[0:-offset,:,:] += L*err2
    g1[offset:,:,:]   -= L*err1

g1 = grating(g1)
g2 = grating(g2)

# visualize gratings 
show(323, g1, 'grating 1')
show(324, g2, 'grating 2')

# visualize superpositions
e = np.ones((offset,w,d))
s1 = np.concatenate((e,g1),0)*np.concatenate((g2,e),0) 
s2 = np.concatenate((e,g2),0)*np.concatenate((g1,e),0)
show(325, s1, 'superposition 1')
show(326, s2, 'superposition 2')

fig.savefig('./results/moire2.png', dpi=600)
fig.savefig('./results/moire2.pdf', dpi=600)
