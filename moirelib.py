from numpy import *
from matplotlib.pyplot import *
import scipy.ndimage.filters as filters
import scipy.ndimage.interpolation as interpolation


def prepImage(name='audrey', mag=4, sigma=(0,1./40,0)):
    """
    read image, smooth with specified sigma, and magnify

    Inputs:
        name - filname or one of {'audrey','mona','lenna','einstein'}
        mag - upsample factor
        sigma - gaussian smoothing in each dimension as fraction of image width
    """

    try:
        path = dict( 
            audrey = './images/audrey512.png',
            mona   = './images/mona512.png',
            lenna =  './images/Lenna.png',
            einstein = './images/einstein512.png'
        )[name]
    except KeyError:
        path = name

    img = imread(path)
    img = filters.gaussian_filter(img, sigma=[x*img.shape[1] for x in sigma])
    img = interpolation.zoom(img, (mag,mag,1)) 
    return img



def makeGrating(phaseImage):
    """ 
    Convert phaseImage into grating image scaled between 0 and 1
    """
    return 1/(1+exp(5*cos(2*pi*phaseImage)))



def show(img, sub=111, plotTitle=''):
    """
    paste image in figure
    """
    subplot(sub)
    imshow(img)
    axis('off')
    title(plotTitle)



def makeCarrier(dims=(800,600,3), period=1./20, axis=1, type='uniform'):
    """
    make the carrier phase image  
    INPUTS:
        dims - dimensions in pixels (y,x), or (y,x,3)
        period - grating period as fraction of dims[1]
        axis - 0=horizontal, 1=vertical grating
        type - only 'uniform' for now
    """
    if type=='uniform':
        g = fromfunction(lambda y,x,d: x/float64(period)/dims[1], dims)
    else:
        raise Exception('unknown carrier type') 
    return g



def smoothenPhase(img, maxLaplacian, niter=1):
    """
    enforce grating smoothness by clipping the laplacian
    of the phase image
    """
    lim = maxLaplacian/img.shape[1]
    for i in range(niter):
        avg = (img[2:,:,:]+img[:-2,:,:])/2
        img[1:-1,:,:] = img[1:-1,:,:].clip(avg-lim, avg+lim)
    return img
