"""
A class dedicated to plotting graphs.
"""
import matplotlib_inline
from matplotlib import pyplot as plt

from TripHelper.Graph.Node import Point
from TripHelper.Graph.Edge import Edge
import polyline

from TripHelper.Loader.TypeManager import TypeManager


class Plotter:

    def __init__(self):
        self.type_manager = TypeManager()
        pass

    def set_lims(self, pos1, pos2):
        x_lim = [0.99 * min([pos1[0], pos2[0]]), 1.01 * max([pos1[0], pos2[0]])]
        y_lim = [0.99 * max([pos1[1], pos2[1]]), 1.01 * min([pos1[1], pos2[1]])]
        print("limits", x_lim, y_lim)
        plt.ylim(x_lim)
        plt.xlim(y_lim)
        return

    def plot_points(self, points: list[Point]):
        #x = [point.get_data().get_pos()[0] for point in points]
        #y = [point.get_data().get_pos()[1] for point in points]
        #plt.errorbar(y, x, fmt="x")
        for point in points:
            x = point.get_data().get_pos()[0]
            y = point.get_data().get_pos()[1]
            plt.errorbar(y, x, fmt="x")
            if not self.type_manager.obj_is_of_type(point.get_data(), "Road"):

                plt.text(y, x, f"{point.get_data().get_name()}")
        return

    def plot_points_and_polyline(self, points: list[Point], lines: list[str]):
        self.plot_points(points)

        plt.title("California's Roads and Parks")
        plt.figure(figsize=(15, 9))

        for line in lines:
            geometry_decoded = polyline.decode(line)
            x_line = [point[0] for point in geometry_decoded]
            y_line = [point[1] for point in geometry_decoded]
            plt.plot(y_line, x_line)

        for point in points:
            for edge in point.get_neighbours():
                poly_encoded = edge.get_extra()
                poly_decoded = polyline.decode(poly_encoded)
                x_line = [point[0] for point in poly_decoded]
                y_line = [point[1] for point in poly_decoded]
                plt.plot(y_line, x_line)

    def plot_point_and_edges(self, point: Point):
        points = [point]
        for edge in point.get_neighbours():
            self.plot_extra_of_edge(edge)
            points.append(edge.get_end_point())
        self.plot_points(points)
        plt.title(f"{point.get_data().get_name()}")
        return

    def plot_extra_of_edge(self, edge: 'Edge'):
        poly_decoded = polyline.decode(edge.get_extra())
        x_line = [point[0] for point in poly_decoded]
        y_line = [point[1] for point in poly_decoded]
        plt.plot(y_line, x_line)

    def plot_route(self, points: list[Point]):
        for index, point in enumerate(points[:-1]):
            for edge in point.get_neighbours():
                if points[index + 1] == edge.get_end_point():
                    self.plot_extra_of_edge(edge)
        pass

    def finalise_plot(self, name: 'str', save: 'bool'):
        #plt.axis('off')
        if save: plt.savefig(f"{name}.png")
        plt.show()

