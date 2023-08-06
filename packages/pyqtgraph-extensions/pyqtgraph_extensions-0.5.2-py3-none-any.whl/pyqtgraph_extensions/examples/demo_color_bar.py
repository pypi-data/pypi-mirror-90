"""Illustrate ColorBarItem, a MATLAB-like color bar suited for non-interactive
publication plots."""
import sys
import numpy as np
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph_extensions as pgx

if QtGui.QApplication.instance() is None:
    qapp=QtGui.QApplication(sys.argv)
else:
    # Presumably running in a GUI with event QApplication already created
    qapp=None

# import logging
# logging.basicConfig(level=logging.DEBUG)
# logging.getLogger(pgx.__name__).setLevel(level=logging.DEBUG)

# Generate 2D Gaussian distribution
x=np.arange(100)-50
y=np.arange(110)[:,None]-55
z_0=np.exp(-(x**2+y**2)/100.0)

glw=pg.GraphicsLayoutWidget()
glw.addLabel('ColorBarItem is linked to two images (on different axes), both being updated live.')
glw.nextRow()
gl=glw.addLayout()
def make_image():
    plt=gl.addPlot(labels={'left':'y','bottom':'x'})
    im=pgx.ImageItem()
    im.setLookupTable(pgx.get_colormap_lut())
    plt.addItem(im)
    return im

ims = [make_image() for _ in range(2)]

# Add a color bar, linked to the image. It can go anywhere but we place it in
# the next column.
cb=pgx.ColorBarItem(images=ims,label='intensity')
gl.addItem(cb)

def update():
    t=pg.time()
    for im, phase in zip(ims, (0, np.pi/2)):
        # Create amplitude-modulated noisy Gaussian
        z=np.sin(t - phase)**2*z_0+np.random.random(z_0.shape)*0.1
        levels=im.levels
        im.setImage(z,autoLevels=False)
update()
# The first setImage disables autorange.
cb.vb.enableAutoRange(1)
glw.show()


timer = QtCore.QTimer()
timer.timeout.connect(update)
timer.start(50)

if qapp is not None:
    sys.exit(qapp.exec_())