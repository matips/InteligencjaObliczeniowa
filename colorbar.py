"""
Demonstrates similarities between pcolor, pcolormesh, imshow and pcolorfast
for drawing quadrilateral grids.

"""
import matplotlib.pyplot as plt
import numpy as np


# make these smaller to increase the resolution


def visual(function, populations, xmin=None, xmax=None, ymin=None, ymax=None, dx=None, dy=None, border=0.5):
    if xmin is None:
        xmin = min([individual.genomeList[0] for population in populations for individual in population['individuals']]) - border
    if xmax is None:
        xmax = max([individual.genomeList[0] for population in populations for individual in population['individuals']]) + border
    if ymin is None:
        ymin = min([individual.genomeList[1] for population in populations for individual in population['individuals']]) - border
    if ymax is None:
        ymax = max([individual.genomeList[1] for population in populations for individual in population['individuals']]) + border
    if dx is None:
        dx = (xmax - xmin) / 200
    if dy is None:
        dy = (xmax - xmin) / 200
    # generate 2 2d grids for the x & y bounds
    y, x = np.mgrid[slice(ymin, ymax + dy, dy),
                    slice(xmin, xmax + dx, dx)]
    z = function([x, y])
    # x and y are bounds, so z should be the value *inside* those bounds.
    # Therefore, remove the last value from the z array.
    z = z[:-1, :-1]
    z_min, z_max = np.min(z), np.max(z)

    plt.subplot(1, 1, 1)
    plt.pcolor(x, y, z, vmin=z_min, vmax=z_max)
    plots = []
    for population in populations:
        created_plot, = plt.plot([individual.genomeList[0] for individual in population['individuals']], [individual[1] for individual in population['individuals']], population['style'], label=population['name'])
        plots.append(created_plot)
    plt.legend(handles=plots)
    plt.title('schafferF6')
    # set the limits of the plot to the limits of the data
    plt.axis([x.min(), x.max(), y.min(), y.max()])
    plt.colorbar()

    plt.show()
