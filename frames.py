import matplotlib.pyplot as plt


class Frames:
    def __init__(self, x):
        self.x_coordinate = x
        self.coordinates = []

    def __append__(self, new_coordinate):
        not_in_frame=True
        for i in range (len(self.coordinates)):
            if new_coordinate[0]==self.coordinates[i][0] and new_coordinate[1]==self.coordinates[i][1]:
                not_in_frame=False
        if not_in_frame:
            self.coordinates.append(new_coordinate)

    def plot(self):
        list_x_coordinates = []
        list_y_coordinates = []
        for coord in self.coordinates:
            list_x_coordinates.append(coord[0])
            list_y_coordinates.append(coord[1])
        plt.plot(list_x_coordinates, list_y_coordinates)
        plt.show()
