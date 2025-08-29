import numpy as np

def generate_poisson_points(number, lon_range, lat_range):

    area = (lat_range[1] - lat_range[0]) * (lon_range[1] - lon_range[0])
    lam = number / area
    
    intervals = np.random.poisson(lam, number)
    
    normed = np.cumsum(intervals) / np.sum(intervals)
    lons = lon_range[0] + np.random.rand(number) * (lon_range[1] - lon_range[0])
    lats = lat_range[0] + normed * (lat_range[1] - lat_range[0])
    points = list(zip(lons, lats))
    return points
