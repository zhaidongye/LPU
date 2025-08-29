import numpy as np
from scipy.stats import poisson, chisquare


def poisson_distribution_test(R_max, G, centroid, grid_size=0.005):
    
    nodes, data = zip(*G.nodes(data=True))
    node_coords = np.array([[d['x'], d['y']] for d in data])
    node_distances = np.linalg.norm(node_coords - centroid, axis=1)
    
    nodes_within_radius = [nodes[i] for i in range(len(nodes)) if node_distances[i] <= R_max]
    
    
    centroid_lon, centroid_lat = centroid
    
    
    north, south = 40.05, 39.8
    east, west = 116.55, 116.2
    
    
    min_lon, max_lon = centroid_lon - R_max, centroid_lon + R_max
    min_lat, max_lat = centroid_lat - R_max, centroid_lat + R_max
    
    min_lon = max(min_lon, west)
    max_lon = min(max_lon, east)
    min_lat = max(min_lat, south)
    max_lat = min(max_lat, north)
    
    
    grid_counts = {}
    for node in nodes_within_radius:
        x, y = G.nodes[node]['x'], G.nodes[node]['y']
        grid_x = int((x - min_lon) // grid_size)
        grid_y = int((y - min_lat) // grid_size)
        key = (grid_x, grid_y)
        grid_counts[key] = grid_counts.get(key, 0) + 1

    counts = list(grid_counts.values())
    num_grids = len(grid_counts)
    mean_count = np.mean(counts)

    
    max_count = max(counts)
    observed_freq = np.bincount(counts, minlength=max_count+1)
    expected_freq = poisson.pmf(np.arange(max_count+1), mean_count) * num_grids

    
    mask = expected_freq > 1
    observed_freq = observed_freq[mask]
    expected_freq = expected_freq[mask]

    
    expected_freq = expected_freq * (observed_freq.sum() / expected_freq.sum())

    chi2, p_value = chisquare(observed_freq, expected_freq)
    
    return p_value, chi2