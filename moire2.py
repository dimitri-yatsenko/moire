import numpy as np
import matplotlib.pyplot as mp
import scipy.ndimage.filters as ndfilt
import scipy.ndimage.interpolation as ndint

T = 1./40        # grating period as fraction of image width
mag = 2          # image upsamping factor
offset = 1./8    # superposition offset
hsigma = T/4.     # sigma for gaussian smoothing along horizontal dimension

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


# load original images, smooth, upsample, and display
img1 = mp.imread('./images/audrey512.png')
img2 = mp.imread('./images/mona512.png')
height, width, depth = img1.shape    # images are assumed to be equal in size
img1 = ndfilt.gaussian_filter1d(img1, sigma=hsigma*width, axis=1)
img2 = ndfilt.gaussian_filter1d(img2, sigma=hsigma*width, axis=1)
img1 = ndint.zoom(img1,(mag,mag,1))
img2 = ndint.zoom(img2,(mag,mag,1))

fig = mp.figure(figsize=(8,10))
show(321, img1, 'original')
show(322, img2, 'original')

# convert parameters to pixels
height, width, depth = img1.shape
T = round(T*width)  
offset = round(offset*height)

# carrier phase image: horizontal gradient with slope 1/T
g1 = np.fromfunction(lambda y,x,d: x/T, (height+offset, width, depth))
g2 = g1.copy()

# iterative adjustment of gratings to images
L = 0.04       # learning rate
niter = 501    # of iterations
maxCurvature = 0.001/T  # controls grating smoothness

for i in range(niter):
    if i % 25 == 0:
        print "iteration [%4d/%4d]" % (i, niter)

    # update gratings
    err1 = (1-img1)/2 - (g1[:-offset,:,:] - g2[offset:,:,:])
    err2 = (1-img2)/2 - (g2[:-offset,:,:] - g1[offset:,:,:])
    g1[:-offset,:,:] += L*err1
    g2[offset:,:,:] -= L*err1
    g2[:-offset,:,:] += L*err2
    g1[offset:,:,:] -= L*err2

    # enforce grating smoothness by clipping the laplacian
    avg = (g1[2:,:,:]+g1[:-2,:,:])/2
    g1[1:-1,:,:] = g1[1:-1,:,:].clip(avg-maxCurvature, avg+maxCurvature)

print 'saving image...'
g1 = grating(g1)
g2 = grating(g2)

# visualize gratings 
show(323, g1, 'grating 1')
show(324, g2, 'grating 2')

# visualize superpositions
e = np.ones((offset, width, depth))
s1 = np.vstack((e, g1))*np.vstack((g2, e)) 
s2 = np.vstack((e, g2))*np.vstack((g1, e))
show(325, s1, 'superposition 1')
show(326, s2, 'superposition 2')

fig.savefig('./results/moire2.png', dpi=300)
