import os
import numpy as np

__eigen_dir__ = "include/gtsam/3rdparty/Eigen/"

def get_includes(include_eigen=True):
    root = os.path.dirname(__file__)
    parent = os.path.join(root, "..")
    path = [root, parent, np.get_include()]
    if include_eigen:
        path.append(os.path.join(root, __eigen_dir__))
    return path

