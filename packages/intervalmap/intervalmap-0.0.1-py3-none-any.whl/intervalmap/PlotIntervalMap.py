# PlotIntervalMap.py
# Marcio Gameiro
# 2021-01-05
# MIT LICENSE

import numpy as np
from interval import interval
import matplotlib
import matplotlib.pyplot as plt
# from matplotlib import colors
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection

def PlotMap(f, x_range, num_pts, fig_width=8, fig_height=8):
    """Plots function.
    """
    x = np.linspace(x_range[0], x_range[1], num_pts)
    fig = plt.figure(figsize=(fig_width, fig_height))
    ax = fig.add_subplot(1,1,1)
    ax.tick_params(labelsize=20)
    ax.plot(x, f(x), 'bo', x, f(x), 'k')
    ax.set_xlabel(r"$x$", fontsize=20);
    ax.set_ylabel(r"$y$", fontsize=20);
    plt.show()

def PlotIntervalMap(f, x_range, num_pts, face_color='red', edge_color='black',
                    curve_color='blue', fig_width=10, fig_height=10):
    """Plots function on a grid using interval arithmetic.
    """
    line_width = 2
    alpha = 0.5
    x = np.linspace(x_range[0], x_range[1], num_pts)
    x_intvals = [interval[x[k], x[k+1]] for k in range(len(x) - 1)]
    y_intvals = [f(x) for x in x_intvals]
    patches = [] # Lists of polygons
    for ix, iy in zip(x_intvals, y_intvals):
        # Get vertices of rectangle
        v0 = [ix[0].inf, iy[0].inf]
        v1 = [ix[0].sup, iy[0].inf]
        v2 = [ix[0].sup, iy[0].sup]
        v3 = [ix[0].inf, iy[0].sup]
        verts = [v0, v1, v2, v3]
        polygon = Polygon(verts, closed=True)
        patches.append(polygon)
    # Create patchs collection of Polygons
    p2 = PatchCollection(patches, cmap=matplotlib.cm.jet, fc=face_color, ec=edge_color)
    p2.set_linewidths(line_width)
    p2.set_alpha(alpha)
    # Make a list of colors cycling through the default series
    # clrs = [colors.to_rgba(c) for c in plt.rcParams['axes.prop_cycle'].by_key()['color']]
    # p2.set_color(clrs)
    # fig, ax = plt.subplots(figsize=(fig_width, fig_height))
    fig = plt.figure(figsize=(fig_width, fig_height))
    ax = fig.add_subplot(1,1,1)
    ax.tick_params(labelsize=20)
    ax.plot(x, f(x), c=curve_color) # Plot function
    ax.add_collection(p2) # Add patch collection to the axis
    ax.set_xlabel(r"$x$", fontsize=20);
    ax.set_ylabel(r"$y$", fontsize=20);
    ax.autoscale_view() # Auto scale axis
    # ax.set_aspect(1)
    # plt.axis('equal')
    # plt.axis('off')
    plt.show()
