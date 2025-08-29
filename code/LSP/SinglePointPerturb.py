import numpy as np
from LSP.SingleInfluenceCal import SingleInfluCal
def SingePerturb(point,influence_points,point_next_direction,alpha):

    total_influence = np.array([0.0, 0.0])
    for candidate_point in influence_points:
        single_influence = SingleInfluCal(point, candidate_point, point_next_direction, alpha)
        total_influence += single_influence
    
    new_lat = point[0] + total_influence[0]
    new_lon = point[1] + total_influence[1]

    return (new_lon, new_lat)