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



def load_image(path):
    """
    Load a FITS image from the specified path.
    
    Parameters:
    path (str): Path to the FITS file.
    
    Returns:
    hdul (HDUList): The HDU list containing the FITS data.
    image_data (ndarray): The image data from the FITS file.
    header (Header): The header information from the FITS file.
    wcs (WCS): World Coordinate System information for the image.
    """
    # | HDU | Name      | Description                                                                       |
    # | --- | --------- | --------------------------------------------------------------------------------- |
    # | 0   | `PRIMARY` | This is just the header — no image data (empty `()` shape).                       |
    # | 1   | `SCI`     | Science data cube — a 3D image with shape (45, 45, 1400), stored as `float32`     |
    # | 2   | `ERR`     | Error estimates for the science data, same shape.                                 |
    # | 3   | `DQ`      | Data quality flags (integers).                                                    |
    # | 4   | `WMAP`    | Possibly a weight map or exposure map.                                            |
    # | 5   | `HDRTAB`  | Metadata (headers, config). Not image data.                                       |
    # | 6   | `ASDF`    | Metadata blob in ASDF format (used by JWST/MIRI pipeline).                        |

    hdul = fits.open(path)

    image_data = hdul[1].data
    header = hdul[1].header
    info = hdul.info()
    wcs = WCS(header, naxis=2)
    
    return hdul, image_data, header, info, wcs

def slice_visualizer(image_data, slice_index, cmap='inferno'):
    """
    Visualize a specific slice of the 3D image data.
    
    Parameters:
    image_data (ndarray): The 3D image data.
    slice_index (int): The index of the slice to visualize.
    
    Returns:
    None
    """
    plt.figure(figsize=(10, 8))
    plt.imshow(image_data[slice_index], cmap=cmap)
    plt.colorbar(label='Flux')
    plt.title(f'Basic Display - Slice {slice_index}')
    plt.tight_layout()
    plt.show()

def spectrum_visualizer(image_data, pixel_coords):
    """
    Visualize the spectrum at a specific pixel location.
    
    Parameters:
    image_data (ndarray): The 3D image data.
    pixel_coords (tuple): The (x, y) coordinates of the pixel.
    
    Returns:
    None
    """
    x, y = pixel_coords
    spectrum = image_data[:, y, x]  # Extracting a spectrum from a specific pixel
    plt.plot(spectrum)
    plt.xlabel("Slice index")
    plt.ylabel("Flux")
    plt.title(f"Spectrum at pixel ({x}, {y})")
    plt.grid(True)
    plt.show()

def cube_viewer(image_data, wcs, initial_index=0, cmap="inferno"):
    initial_index = 0
    fig, ax = plt.subplots(subplot_kw={'projection': wcs})
    plt.subplots_adjust(bottom=0.2) 

    im = ax.imshow(image_data[initial_index], origin='lower', cmap=cmap)
    cbar = plt.colorbar(im, ax=ax)

    ax.set_title(f"Slice {initial_index}")
    ax.set_xlabel('RA')
    ax.set_ylabel('Dec')

    ax_slider = plt.axes([0.25, 0.05, 0.5, 0.03])
    slider = Slider(
        ax_slider,
        'Slice',
        0,
        image_data.shape[0] - 1,
        valinit=initial_index,
        valstep=1
    )

    def update(val):
        index = int(slider.val)
        im.set_data(image_data[index])
        ax.set_title(f"Slice {index}")
        fig.canvas.draw_idle()

    slider.on_changed(update)
    plt.show()

def multiple_cube_viewer(cubes, wcs_list=None, axis=0, cmap='magma', layout='vertical'):
    """
    Create multiple interactive viewers for 3D FITS data cubes, each with its own slider.

    Parameters:
    - cubes (list of ndarray): List of 3D FITS data cubes.
    - wcs_list (list of WCS or None): List of WCS objects for each cube. Can be None for no WCS projection.
    - axis (int): Axis to slice along (default is 0).
    - cmap (str): Colormap for image display.
    - layout (str): 'vertical' or 'horizontal' layout of viewers.
    """
    num_cubes = len(cubes)
    if wcs_list is None:
        wcs_list = [None] * num_cubes

    # Determine subplot arrangement
    if layout == 'horizontal':
        fig, axes = plt.subplots(1, num_cubes, subplot_kw={'projection': wcs_list[0]} if wcs_list[0] else {}, figsize=(5 * num_cubes, 5))
        if num_cubes == 1:
            axes = [axes]
    else:
        fig, axes = plt.subplots(num_cubes, 1, subplot_kw={'projection': wcs_list[0]} if wcs_list[0] else {}, figsize=(6, 4 * num_cubes))
        if num_cubes == 1:
            axes = [axes]

    fig.subplots_adjust(bottom=0.05 * num_cubes + 0.15)

    sliders = []

    for i, (cube, wcs, ax) in enumerate(zip(cubes, wcs_list, axes)):
        if axis != 0:
            cube = cube.swapaxes(0, axis)

        im = ax.imshow(cube[0], origin='lower', cmap=cmap)
        ax.set_title(f"Cube {i+1} – Slice 0")
        ax.set_xlabel('RA' if wcs else 'X')
        ax.set_ylabel('Dec' if wcs else 'Y')
        plt.colorbar(im, ax=ax)

        # Create a unique slider axis for each cube
        slider_ax = fig.add_axes([0.2, 0.05 + 0.05 * i, 0.6, 0.02])
        slider = Slider(slider_ax, f'Cube {i+1} Slider', 0, cube.shape[0] - 1, valinit=0, valstep=1)
        sliders.append((slider, im, ax, cube))

    def make_update_func(slider, im, ax, cube, index):
        def update(val):
            idx = int(slider.val)
            im.set_data(cube[idx])
            ax.set_title(f"Cube {index+1} – Slice {idx}")
            fig.canvas.draw_idle()
        return update

    for i, (slider, im, ax, cube) in enumerate(sliders):
        slider.on_changed(make_update_func(slider, im, ax, cube, i))

    plt.show()