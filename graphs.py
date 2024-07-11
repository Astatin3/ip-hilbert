import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from utils import *

order=16
grid_size=128
def line_chart(x,y ):
    plt.plot(x, y)
    plt.show()


def graph_density(ip_list: str):
    xarr = []
    yarr = []
    for ip in ip_list:
        try:
            if ":" in ip:
                ip = ip_to_int(ip.split(":")[0])
            else:
                ip = ip_to_int(ip)
        except ValueError as e:
            print(e)
            continue
        x, y = d2xy(2**order, ip)
        xarr.append(x)
        yarr.append(y)


    fig, ax = plt.subplots(figsize=(64, 64))

    # Create density grid
    H, xedges, yedges = np.histogram2d(xarr, yarr, bins=grid_size, range=[[0, 2**order], [0, 2**order]])

    # Plot heatmap
    im = ax.imshow(H.T, cmap='YlOrRd', extent=[0, 2**order, 0, 2**order], origin='lower',
                   norm=colors.LogNorm(vmin=1, vmax=H.max()))
    # Plot points
    ax.scatter(xarr, yarr, color='blue', s=1, alpha=0.5)

    ax.set_xlim(0, 2 ** order)
    ax.set_ylim(0, 2 ** order)

    # plt.colorbar(im, label='Number of IPs')
    plt.axis('on')
    plt.show()

def graph_ports(ip_list: str):
    count = np.zeros(65536)

    for ip in ip_list:
        if not ":" in ip:
            continue
        port = int(ip.split(":")[1])
        count[port] += 1

    line_chart(np.arange(0, 65536), count)


def graph_nonstandard_ports(ip_list: str):
    xarr = []
    yarr = []
    colorarr = []
    for ip in ip_list:
        try:
            if ":" in ip:
                split = ip.split(":")
                ip = ip_to_int(split[0])
                if split[1] == "25565":
                    colorarr.append('red')
                else:
                    colorarr.append('blue')

            else:
                ip = ip_to_int(ip)
                colorarr.append('green')
        except ValueError as e:
            print(e)
            continue
        x, y = d2xy(2**order, ip)
        xarr.append(x)
        yarr.append(y)


    fig, ax = plt.subplots(figsize=(12, 12))

    # Create density grid
    H, xedges, yedges = np.histogram2d(xarr, yarr, bins=grid_size, range=[[0, 2**order], [0, 2**order]])

    # Plot heatmap
    im = ax.imshow(H.T, cmap='YlOrRd', extent=[0, 2**order, 0, 2**order], origin='lower',
                   norm=colors.LogNorm(vmin=1, vmax=H.max()))
    # Plot points
    ax.scatter(xarr, yarr, color=colorarr, s=1, alpha=0.5)

    ax.set_xlim(0, 2 ** order)
    ax.set_ylim(0, 2 ** order)

    # plt.colorbar(im, label='Number of IPs')
    plt.axis('on')
    plt.show()

def random_choord(H):
    weights = H.flatten()

    weights = weights / np.sum(weights)
    index = np.random.choice(grid_size*grid_size, p=weights)
    x, y = divmod(index, grid_size)

    x += np.random.random()
    y += np.random.random()

    x /= grid_size
    y /= grid_size

    x *= 2 ** order
    y *= 2 ** order

    return x, y


def generate_random_ips(ip_list: str, count: int):
    xarr = []
    yarr = []
    for ip in ip_list:
        try:
            if ":" in ip:
                split = ip.split(":")
                ip = ip_to_int(split[0])
            else:
                ip = ip_to_int(ip)
        except ValueError as e:
            print(e)
            continue
        x, y = d2xy(2**order, ip)
        xarr.append(x)
        yarr.append(y)

    fig, ax = plt.subplots(figsize=(12, 12))

    H, xedges, yedges = np.histogram2d(xarr, yarr, bins=grid_size, range=[[0, 2**order], [0, 2**order]])


    # x /= grid_size
    # y /= grid_size

    # ips = []

    print(count)

    for i in range(count):
        x, y = random_choord(H)
        d = xy2d(2**order, x, y)
        ip = ip_int_to_ip(d)
        print(ip)
