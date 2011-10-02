import numpy as np
import scipy.signal as sig
import matplotlib.pyplot as mp


fig = mp.figure(figsize=(8,10))
T = 20     # grating period in pixels


def grating(phaseImage):
    """ 
    Convert phaseImage into grating image scaled between 0 and 1
    """
    return 1/(1+np.exp(5*np.cos(2*np.pi*phaseImage)))

def show(sub, img, title):
    mp.subplot(sub)
    mp.imshow(img)
    mp.axis('off')
    mp.title(title)
    mp.gray()


# load image
img = mp.imread('./images/mona512.png')

# convert to grayscale and smooth
img = img.mean(2)    # RGB to grayscale
h,w = img.shape
kernel = sig.gaussian(T+1,T/2) 
kernel = np.outer(kernel,kernel)
kernel = kernel/kernel.sum()
img = sig.convolve2d(img, kernel, mode='same', boundary='symm')
show(311, img, 'preprocessed')

# generate gratings
carrier = np.tile(np.r_[0.0:w],(h,1))/T  # horizontal gradient with slope 1/T
grating1 = grating(carrier-(1-img)/4)
grating2 = grating(carrier+(1-img)/4)

# visualize gratings and their superposition
grating1 = grating1.reshape(h,w,1)
grating2 = grating2.reshape(h,w,1)

grating1 = np.concatenate((grating1,0.2+0.8*grating1,grating1),2)   # green
grating2 = np.concatenate((0.2+0.8*grating2,grating2,0.2+0.8*grating2),2)   # magenta
show(323, grating1, 'grating 1')
show(324, grating2, 'grating 2')
show(313, grating1*grating2, 'superposition')

fig.savefig('./results/moire1.png')
fig.savefig('./results/moire1.pdf')
