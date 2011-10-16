"""
Simple moire with two gratings encoding two color images
"""
import moirelib as m

T = 1./40  # grating period as fraction of image width
offset = 1./8  # offset as a fraction of the image height

print 'Loading images...'
img = (
    m.prepImage('audrey', mag=4, sigma=(0,T/4,0)), 
    m.prepImage('mona',   mag=4, sigma=(0,T/4,0))
    )
fig = m.figure(figsize=(8,10))
m.show(img[0], 321, 'original')
m.show(img[1], 322, 'original')

print 'generating gratings...'
offset = round(offset*img[0].shape[0])  # convert to pixels
dims = img[0].shape
dims = (dims[0]+offset,dims[1],dims[2])
g1 = m.makeCarrier(dims, T)
g2 = g1.copy()

# iterative adjustment of gratings to images
L = 0.04       # learning rate
niter = 501    # of iterations

for i in range(niter):
    if i % 25 == 0:
        print "iteration [%4d/%4d]" % (i, niter)

    # update gratings
    err1 = (1-img[0])/2 - (g1[:-offset,:,:] - g2[offset:,:,:])
    err2 = (1-img[1])/2 - (g2[:-offset,:,:] - g1[offset:,:,:])
    g1[:-offset,:,:] += L*err1
    g2[offset:,:,:] -= L*err1
    g2[:-offset,:,:] += L*err2
    g1[offset:,:,:] -= L*err2

    # enforce grating smoothness by clipping the laplacian
    g1 = m.smoothenPhase(g1, 1e-4/T)

print 'saving image...'
g1 = m.makeGrating(g1)
g2 = m.makeGrating(g2)

# visualize gratings 
m.show(g1, 323, 'grating 1')
m.show(g2, 324, 'grating 2')

# visualize superpositions
e = m.ones((offset, dims[1], dims[2]))
s1 = m.vstack((e, g1))*m.vstack((g2, e)) 
s2 = m.vstack((e, g2))*m.vstack((g1, e))
m.show(s1, 325, 'superposition 1')
m.show(s2, 326, 'superposition 2')

fig.savefig('./results/moire2.png', dpi=300)
