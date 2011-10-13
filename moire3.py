import numpy as np
import matplotlib.pyplot as mp
import scipy.ndimage.filters as ndfilt
import scipy.ndimage.interpolation as ndint


T = 1./40        # grating period as fraction of image width
mag = 2          # image upsamping factor
offset = 1./8    # superposition offset
hsigma = T/4     # sigma for gaussian smoothing along horizontal dimension


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


# load original image, smooth, upsample, and display
img = mp.imread('./images/audrey512.png')
height, width, depth = img.shape
img = ndfilt.gaussian_filter1d(img, sigma=hsigma*width, axis=1)
img = ndint.zoom(img,(mag,mag,1))

fig = mp.figure(figsize=(8,10))
show(311, img, 'original')

# convert parameters to pixels
height, width, depth = img.shape
T = round(T*width)
offset = round(offset*height)

# carrier phase image: horizontal gradient with slope 1/T
g = np.fromfunction(lambda y,x,d: x/T, (height+offset,width,3))

# iterative adjustment of gratings to images
L = 0.04    # learning rate
niter = 501   # of iterations
maxCurvature = 0.001/T

for i in range(niter):
    if i % 25 == 0:
        print "iteration [%4d/%4d]" % (i, niter)

    # update grating
    err = (1-img)/2 - (g[0:-offset,:,:] - g[offset:,:,:])
    g[0:-offset,:,:] += L*err
    g[offset:,:,:]   -= L*err

    # enforce grating smoothness by clipping the laplacian
    avg = (g[2:,:,:]+g[:-2,:,:])/2
    g[1:-1,:,:] = g[1:-1,:,:].clip(avg-maxCurvature, avg+maxCurvature)

print 'saving image...'
g = grating(g)

# visualize gratings 
show(312, g, 'grating')

# visualize superpositions
e = np.ones((offset, width, depth))
s = np.vstack((e, g))*np.vstack((g, e)) 
show(313, s, 'superposition')

fig.savefig('./results/moire3.png', dpi=300)
