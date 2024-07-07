import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors

def hilbert_xy(ip_int, order=16):
    """Convert IP integer to (x,y) on a Hilbert curve of given order."""
    x = y = 0
    for i in range(order):
        xi = (ip_int >> (2 * i)) & 1
        yi = (ip_int >> (2 * i + 1)) & 1

        if yi == 0:
            if xi == 1:
                x = (1 << order) - 1 - x
                y = (1 << order) - 1 - y
            x, y = y, x

        x += xi << i
        y += yi << i

    return x, y

def ip_to_int(ip):
    return int(''.join([bin(int(x) + 256)[3:] for x in ip.split('.')]), 2)

def create_hilbert_points(ip_list, order=16):
    points = []
    for ip in ip_list:
        ip_int = ip_to_int(ip)
        x, y = hilbert_xy(ip_int, order)
        points.append((x, y))
    return points

def visualize_hilbert_points(ip_list, order=16, grid_size=32):
    points = create_hilbert_points(ip_list, order)
    x, y = zip(*points)

    fig, ax = plt.subplots(figsize=(12, 12))

    # Create density grid
    H, xedges, yedges = np.histogram2d(x, y, bins=grid_size, range=[[0, 2**order], [0, 2**order]])

    # Plot heatmap
    im = ax.imshow(H.T, cmap='YlOrRd', extent=[0, 2**order, 0, 2**order], origin='lower',
                   norm=colors.LogNorm(vmin=1, vmax=H.max()))

    # Plot points
    ax.scatter(x, y, color='blue', s=2, alpha=0.5)

    ax.set_xlim(0, 2 ** order)
    ax.set_ylim(0, 2 ** order)

    plt.title(f"IP Addresses on Hilbert Curve (order {order}) with Density Heatmap")
    plt.colorbar(im, label='Number of IPs')
    plt.axis('off')
    plt.show()

if __name__ == '__main__':
    ip_list = open(sys.argv[1]).read().splitlines()
    visualize_hilbert_points(ip_list)