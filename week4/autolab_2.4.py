import sys
import numpy as np

def distance_matrix(p1, p2):
    p1 = np.radians(p1)
    p2 = np.radians(p2)

    lat1 = p1[:, 0][:, None]   # shape (n, 1)
    lon1 = p1[:, 1][:, None]   # shape (n, 1)
    lat2 = p2[:, 0][None, :]   # shape (1, m)
    lon2 = p2[:, 1][None, :]   # shape (1, m)

    dlat = lat1 - lat2         # (n, m)
    dlon = lon1 - lon2         # (n, m)

    sin2_dlat = np.sin(0.5 * dlat) ** 2
    sin2_dlon = np.sin(0.5 * dlon) ** 2
    cosprod = np.cos(lat1) * np.cos(lat2)

    a = sin2_dlat + cosprod * sin2_dlon
    D = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))

    return 6371 * D  # km


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