"""
A class dedicated to plotting graphs.
"""
from matplotlib import pyplot as plt

from TripHelper.Graph.Node import Point
import polyline

class Plotter:

    def __init__(self):
        pass

    def plot_points_and_polyline(self, points: list[Point], line: 'str'):
        x = [point.get_data().get_pos()[0] for point in points]
        y = [point.get_data().get_pos()[1] for point in points]

        geometry_decoded = polyline.decode(line)
        x_line = [point[0] for point in geometry_decoded]
        y_line = [point[1] for point in geometry_decoded]

        plt.title("California's Roads and Parks")
        plt.figure(figsize=(15, 9))
        plt.errorbar(y, x, fmt="x")
        plt.plot(y_line, x_line)
        plt.axis('off')
        plt.savefig("california.png")

