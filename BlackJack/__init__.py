from __future__ import division
import sys

py_version = sys.version_info[:3]
if py_version < (3, 0):
    pass
from pandas import DataFrame as df
from numpy.random import choice
import numpy as np
from PIL import Image

import cv2
import cvutils
np.set_printoptions(precision=15)


