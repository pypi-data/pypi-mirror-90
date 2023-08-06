from .textcloud import (TextCloud, STOPWORDS, random_color_func,
                        get_single_color_func)
from .color_from_image import ImageColorGenerator

__all__ = ['TextCloud', 'STOPWORDS', 'random_color_func',
           'get_single_color_func', 'ImageColorGenerator',
           '__version__']

from ._version import get_versions
__version__ = get_versions()['version']
del get_versions
