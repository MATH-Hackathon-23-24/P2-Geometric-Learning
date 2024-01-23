import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

import geomstats.backend as gs
from geomstats.geometry.discrete_curves import (
    DiscreteCurvesStartingAtOrigin,
    SRVMetric,
    L2CurvesMetric,
    insert_zeros,
)

def get_SRVMetric_distance(curve_a, curve_b, k_sampling_points):
    curves_r2 = DiscreteCurvesStartingAtOrigin(
        ambient_dim=2, k_sampling_points=k_sampling_points, equip=False
    )

    curve_a0 = curves_r2.projection(curve_a)
    curve_b0 = curves_r2.projection(curve_b)
    
    curves_r2.equip_with_metric(SRVMetric)

    distance = curves_r2.metric.dist(point_a=curve_a0, point_b=curve_b0)
    return distance

def get_L2_norm_two_curves(y1, y2):
    if len(y1) != len(y2):
        raise ValueError("Should have equal lengths!")
    return np.linalg.norm(y1-y2)