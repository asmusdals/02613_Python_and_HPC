import sys
import numpy as np

def distance_matrix(p1, p2):
    # Convert degrees -> radians
    p1 = np.radians(p1)
    p2 = np.radians(p2)

    lat2 = p2[:, 0]   # (m,)
    lon2 = p2[:, 1]   # (m,)

    D = np.empty((len(p1), len(p2)))

    for i in range(len(p1)):  # only ONE loop
        lat1 = p1[i, 0]       # scalar
        lon1 = p1[i, 1]       # scalar

        dlat = lat1 - lat2    # (m,)
        dlon = lon1 - lon2    # (m,)

        sin2_dlat = np.sin(0.5 * dlat) ** 2
        sin2_dlon = np.sin(0.5 * dlon) ** 2
        cosprod = np.cos(lat1) * np.cos(lat2)

        a = sin2_dlat + cosprod * sin2_dlon
        D[i, :] = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))

    D *= 6371  # Earth radius in km
    return D


def load_points(fname):
    data = np.loadtxt(fname, delimiter=',', skiprows=1, usecols=(1, 2))
    return data


def distance_stats(D):
    assert D.shape[0] == D.shape[1], 'D must be square'
    idx = np.triu_indices(D.shape[0], k=1)
    distances = D[idx]
    return {
        'mean': float(distances.mean()),
        'std': float(distances.std()),
        'max': float(distances.max()),
        'min': float(distances.min()),
    }


fname = sys.argv[1]
points = load_points(fname)
D = distance_matrix(points, points)
stats = distance_stats(D)
print(stats)