""" iCCF """

from .version import __version__

from .bisector import BIS, BISplus, BISminus, BIS_HARPS
from .gaussian import gauss, gaussfit, RV, FWHM, contrast
from .bigaussian import bigauss, bigaussfit
from .vspan import vspan
from .wspan import wspan
from .meta import makeCCF
from .meta_ESPRESSO import calculate_ccf as calculate_ccf_ESPRESSO
from . import utils

from .chromatic import chromaticRV

from .iCCF import EPS, nEPS
from .iCCF import Indicators, indicators_from_files
from_file = Indicators.from_file
