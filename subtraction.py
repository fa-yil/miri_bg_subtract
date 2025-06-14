import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
from matplotlib.widgets import Slider
import matplotlib.animation as animation

from astropy.visualization import simple_norm
from astropy.visualization import ImageNormalize, LogStretch, LinearStretch

from photutils.datasets import (load_simulated_hst_star_image,
                                make_noise_image)

from photutils.detection import find_peaks # find_peaks to find stars & their positions
from photutils.psf import extract_stars 
from photutils.psf import EPSFBuilder
from astropy.table import Table
from astropy.stats import sigma_clipped_stats # for sigma clipping (subtracring background)
from astropy.nddata import NDData
from astropy.io import fits
from astropy.utils.data import download_file
from astropy.visualization import astropy_mpl_style, simple_norm
from astropy.wcs import WCS

matplotlib.use('TkAgg') # Use TkAgg backend for interactive plotting



path = "/home/fatih/G165_main/G165_miri_bg_subtraction/data/JWST/science/jw03722-o003_t003_miri_ch1-long/jw03722-o003_t003_miri_ch1-long_s3d.fits"
hdul = fits.open(path)

# | HDU | Name      | Description                                                                       |
# | --- | --------- | --------------------------------------------------------------------------------- |
# | 0   | `PRIMARY` | This is just the header — no image data (empty `()` shape).                       |
# | 1   | `SCI`     | Science data cube — a 3D image with shape (45, 45, 1400), stored as `float32`     |
# | 2   | `ERR`     | Error estimates for the science data, same shape.                                 |
# | 3   | `DQ`      | Data quality flags (integers).                                                    |
# | 4   | `WMAP`    | Possibly a weight map or exposure map.                                            |
# | 5   | `HDRTAB`  | Metadata (headers, config). Not image data.                                       |
# | 6   | `ASDF`    | Metadata blob in ASDF format (used by JWST/MIRI pipeline).                        |



image_data = hdul[1].data
header = hdul[1].header
info = hdul.info()
wcs = WCS(header, naxis=2)

print("Image data shape:", image_data.shape)


plt.figure(figsize=(10, 8))
plt.imshow(image_data[200], cmap='inferno')
plt.colorbar(label='Flux')
plt.title('Basic Display - 200th Slice')
plt.tight_layout()
plt.show()


spectrum_at_22_22 = image_data[:, 22, 22]  # Extracting a spectrum from a specific pixel
plt.plot(spectrum_at_22_22)
plt.xlabel("Slice index")
plt.ylabel("Flux")
plt.title("Spectrum at pixel (22, 22)")
plt.grid(True)
plt.show()

"""
fig, ax = plt.subplots()
im = ax.imshow(image_data[0], origin='lower', cmap='gray')

def update(frame):
    im.set_data(image_data[frame])
    ax.set_title(f"Slice {frame}")
    return [im]

ani = animation.FuncAnimation(fig, update, frames=range(0, 1400, 10), interval=100)
plt.show()
"""

initial_index = 0

fig, ax = plt.subplots(subplot_kw={'projection': wcs})
plt.subplots_adjust(bottom=0.2) 

im = ax.imshow(image_data[initial_index], origin='lower', cmap='magma')
cbar = plt.colorbar(im, ax=ax)

ax.set_title(f"Slice {initial_index}")
ax.set_xlabel('RA')
ax.set_ylabel('Dec')

ax_slider = plt.axes([0.25, 0.05, 0.5, 0.03])
slider = Slider(ax_slider, 'Slice', 0, image_data.shape[0] - 1, valinit=initial_index, valstep=1)

def update(val):
    index = int(slider.val)
    im.set_data(image_data[index])
    ax.set_title(f"Slice {index}")
    fig.canvas.draw_idle()

slider.on_changed(update)
plt.show()