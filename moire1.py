"""
Simple moire with a single color image
"""

import moirelib as m

T = 1./40        # grating period

print 'pre-processing images...'
img = m.prepImage('audrey', mag=2, sigma=(0,T/4., 0))
fig = m.figure(figsize=(8,10))
m.show(img, 311, 'original')

print 'generating gratings...'
carrier = m.makeCarrier(img.shape, T)
g1 = carrier-(1-img)/4
g2 = carrier+(1-img)/4

print 'smoothing phase...'
g1 = m.smoothenPhase(g1, 1e-3/T, 50)
g2 = m.smoothenPhase(g2, 1e-3/T, 50)

print 'saving images...'
g1 = m.makeGrating(g1)
g2 = m.makeGrating(g2)
m.show(g1,323, 'grating 1')
m.show(g2,324, 'grating 2')
m.show(g1*g2, 313, 'superposition')

fig.savefig('./results/moire1.png', dpi=300)

