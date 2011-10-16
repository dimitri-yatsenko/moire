"""
A simple moire encoding a single image with two identical gratings 
"""

import moirelib as m

T = 1./40        # grating period
offset = 1./8    # superposition offset

print 'pre-processing images...'
img = m.prepImage('audrey', mag=4, sigma=(0,T/4., 0))
fig = m.figure(figsize=(8,10))
m.show(img, 311, 'original')

# carrier phase image: horizontal gradient with slope 1/T
offset = round(offset*img.shape[0])  # convert to pixels
dims = (img.shape[0]+offset, img.shape[1], img.shape[2])
g = m.makeCarrier(dims, T)

print 'computing gratings...'
L = 0.04    # learning rate
niter = 501   # of iterations

for i in range(niter):
    if i % 25 == 0:
        print "iteration [%4d/%4d]" % (i, niter)

    # update grating
    err = (1-img)/2 - (g[0:-offset,:,:] - g[offset:,:,:])
    g[0:-offset,:,:] += L*err
    g[offset:,:,:]   -= L*err
    g = m.smoothenPhase(g, 1e-4/T)

print 'saving image...'
g = m.makeGrating(g)

# visualize gratings 
m.show(g, 312, 'grating')

# visualize superpositions
e = m.ones((offset, img.shape[1], img.shape[2]))
s = m.vstack((e, g))*m.vstack((g, e)) 
m.show(s, 313, 'superposition')

fig.savefig('./results/moire3.png', dpi=300)
