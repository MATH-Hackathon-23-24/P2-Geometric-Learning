import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from dtaidistance import dtw, dtw_ndim

import geomstats.backend as gs
from geomstats.geometry.discrete_curves import (
    DiscreteCurvesStartingAtOrigin,
    SRVMetric
)

def get_SRVMetric_distance(curve_a, curve_b, k_sampling_points):
    curves_r2 = DiscreteCurvesStartingAtOrigin(
        ambient_dim=curve_a.shape[1], k_sampling_points=k_sampling_points, equip=False
    )
    curve_a0 = curves_r2.projection(curve_a)
    curve_b0 = curves_r2.projection(curve_b)
    
    curves_r2.equip_with_metric(SRVMetric)
    return curves_r2.metric.dist(point_a=curve_a0, point_b=curve_b0)
    
def get_SRVMetric_aligned_distance(curve_a, curve_b, k_sampling_points):
    curves_r2 = DiscreteCurvesStartingAtOrigin(
        ambient_dim=curve_a.shape[1], k_sampling_points=k_sampling_points, equip=False
    )
    curve_a0 = curves_r2.projection(curve_a)
    curve_b0 = curves_r2.projection(curve_b)
    
    curves_r2.equip_with_metric(SRVMetric)
    curves_r2.equip_with_group_action("reparametrizations")
    curves_r2.equip_with_quotient_structure()
    
    curve_b_aligned = curves_r2.fiber_bundle.align(curve_b0, curve_a0)
    return curves_r2.metric.dist(point_a=curve_a0, point_b=curve_b_aligned)
    
def get_dtw_distance(y1, y2):
    if y1.shape[1]-1 == 1:
        return dtw.distance_fast(y1, y2, use_pruning=True)
    else:
        return dtw_ndim.distance(y1,y2)
    
def get_L2_norm_two_curves(y1, y2):
    if len(y1) != len(y2):
        raise ValueError("Should have equal lengths!")
    return np.linalg.norm(y1-y2)