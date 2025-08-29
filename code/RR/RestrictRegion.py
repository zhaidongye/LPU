import numpy as np
from RR.PossionGenerate import generate_poisson_points
from RR.PoissonTest import poisson_distribution_test
def restric_region(trajctory,G,decay=0.7):
    
    
    centroid_lon = trajctory['lon'].mean()
    centroid_lat = trajctory['lat'].mean()
    centroid = np.array([centroid_lon, centroid_lat])
    
    coords = trajctory[['lon', 'lat']].values
    distances = np.linalg.norm(coords - centroid, axis=1)
    R_max = np.max(distances)
    R = R_max
    

    chi2, p_value = poisson_distribution_test(R_max, G, centroid)

    while p_value < 0.05 and R >= 0.01:
        R = max(0, decay * R)
        chi2, p_value = poisson_distribution_test(R, G, centroid)
    if p_value > 0.05:
        nodes, data = zip(*G.nodes(data=True))
        node_coords = np.array([[d['x'], d['y']] for d in data])
        node_distances = np.linalg.norm(node_coords - centroid, axis=1)
        nodes_within_radius = [nodes[i] for i in range(len(nodes)) if node_distances[i] <= R]
    else:
        R = R_max
        nodes_within_radius = [nodes[i] for i in range(len(nodes)) if node_distances[i] <= R]
        number = len(nodes_within_radius)
        
        north, south = 40.05, 39.8
        east, west = 116.55, 116.2
        
        min_lon, max_lon = centroid_lon - R, centroid_lon + R
        min_lat, max_lat = centroid_lat - R, centroid_lat + R
        
        min_lon = max(min_lon, west)
        max_lon = min(max_lon, east)
        min_lat = max(min_lat, south)
        max_lat = min(max_lat, north)
        lon_range = (min_lon, max_lon)
        lat_range = (min_lat, max_lat)
        
        nodes_within_radius = generate_poisson_points(number, lon_range, lat_range)
    
    return R_max,nodes_within_radius