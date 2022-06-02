import matplotlib.pyplot as plt


class Frames:
    """That class is defined by a x coordinate and a list of point for that x coordinate

    :argument
    ----------
    x_coordinate: a float
        the x_coordinate of the frame
    coordinates: a list of tuples
        represents the list of frame situated in that frame"""

    def __init__(self, x):
        self.x_coordinate = x
        self.coordinates = []

    def __append__(self, new_coordinate: tuple):
        """That function appends a new point for a frame with the same x

        :parameter
        -----------
        new_coordinate: a tuple
            (y,z) it represents the coordinates of the point for a frame"""
        not_in_frame = True
        for i in range(len(self.coordinates)):
            if new_coordinate[0] == self.coordinates[i][0] and new_coordinate[1] == self.coordinates[i][1]:
                not_in_frame = False
        if not_in_frame:
            self.coordinates.append(new_coordinate)

    def plot(self):
        """That functions permits to plot the frame

        :argument
        ----------
        self: a frame object

        :returns
        ------------
        print the frame in a graph"""
        list_x_coordinates = []
        list_y_coordinates = []
        for coord in self.coordinates:
            list_x_coordinates.append(coord[0])
            list_y_coordinates.append(coord[1])
        plt.plot(list_x_coordinates, list_y_coordinates)
        plt.show()
