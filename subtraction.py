import matplotlib
import matplotlib.pyplot as plt
from matplotlib.widgets import Button

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

matplotlib.use('TkAgg') # Use TkAgg backend for interactive plotting

