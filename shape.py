import numpy as np
import matplotlib.pyplot as plt


class Form:
    def __init__(self):
        self.shape = []

    def __append__(self, new_frame):
        self.shape.append(new_frame)

    def center_of_gravity_no_mass_for_coordinates(self, x_start, x_end):
        list_y_coordinates = []
        list_z_coordinates = []
        for frame in self.shape:
            if x_end >= frame.x_coordinate >= x_start:
                x_CoG = (x_start + x_end) / 2
                for coordinate in frame.coordinates:
                    list_y_coordinates.append(coordinate[0])
                    list_z_coordinates.append(coordinate[1])
        return x_CoG, np.mean(list_y_coordinates), np.mean(list_z_coordinates)

    def correction_of_coordinates_for_up(self):
        n = len(self.shape)
        for j in range(n):
            list_z_coordinates_of_frame = []  # all the z of the frame
            list_y_coordinates_of_frame = []
            coordinates = self.shape[j].coordinates
            number_coordinates = len(coordinates)
            for i in range(number_coordinates):
                list_z_coordinates_of_frame.append(coordinates[i][1])
                list_y_coordinates_of_frame.append(coordinates[i][0])
            maximum_z = min(list_z_coordinates_of_frame)  # we save the max of z in pd strip coordinates, that means z to the ground
            maximum_y = max(list_y_coordinates_of_frame)
            for coordinate in coordinates:
                if coordinate[1] > maximum_z and abs(coordinate[0]) < maximum_y:
                    self.shape[j].__append__((coordinate[0], maximum_z))
        return self

    def conversion_coordinate_to_pdstrip(self, midship):
        for frame in self.shape:
            frame.x_coordinate = frame.x_coordinate - midship
        return self

    def x_coordinates(self):
        x_coordinates = []
        for frame in self.shape:
            x_coordinates.append(frame.x)
        return x_coordinates

    def calcul_square_inertial_radius_x(self, y_CoG, Z_CoG):
        """inputs are a list of coord and yg zg coordinates of the center of gravity
            it returns the square of the inertial radius along x axis, by an average of (y-yg)**2+(z-zg)**2"""
        sum = 0  # initialization of the sum
        counter = 0
        for frame in self.shape:
            for coordinate in frame.coordinates:
                counter += 1
                z = coordinate[1]
                y = coordinate[0]
                sum += (y - y_CoG) ** 2 + (z - Z_CoG) ** 2  # we add the value for the actual point
        return sum / counter

    def calcul_square_inertial_radius_y(self, X_CoG, z_CoG):
        sum = 0  # initialization of the sum
        counter = 0
        for frame in self.shape:
            x = frame.x_coordinate
            for coordinate in frame.coordinates:
                counter += 1
                z = coordinate[1]
                sum += (x - X_CoG) ** 2 + (z - z_CoG) ** 2  # we add the value for the actual point
        # we return an average
        return sum / counter

    def calcul_square_inertial_radius_z(self, X_CoG, Y_CoG):
        """inputs are a list of coord and yg zg coordinates of the center of gravity
                    it returns the square of the inertial radius along x axis, by an average of (y-yg)**2+(z-zg)**2"""
        sum = 0  # initialization of the sum
        counter = 0
        for frame in self.shape:
            x = frame.x_coordinate
            for coordinate in frame.coordinates:
                counter += 1
                y = coordinate[0]
                sum += (x - X_CoG) ** 2 + (y - Y_CoG) ** 2  # we add the value for the actual point
        return sum / counter

    def calcul_average_xy(self, X_CoG, Y_CoG):
        """inputs are a list of coord and xg yg coordinates of the center of gravity
            it returns the weight weighted average of (x-xg)(y-yg)"""
        sum = 0  # initialization of the sum
        counter = 0
        for frame in self.shape:
            x = frame.x_coordinate
            for coordinate in frame.coordinates:
                counter += 1
                y = coordinate[0]
                sum += (x - X_CoG) * (y - Y_CoG)  # we add the value for the actual point
        return sum / counter

    def calcul_average_yz(self, Y_CoG, Z_CoG):
        sum = 0  # initialization of the sum
        counter = 0
        for frame in self.shape:
            for coordinate in frame.coordinates:
                counter += 1
                y = coordinate[0]
                z = coordinate[1]
                sum += (y - Y_CoG) * (z - Z_CoG)  # we add the value for the actual point
        return sum / counter

    def calcul_average_xz(self, X_CoG, Z_CoG):
        sum = 0  # initialization of the sum
        counter = 0
        for frame in self.shape:
            x = frame.x_coordinate
            for coordinate in frame.coordinates:
                counter += 1
                z = coordinate[1]
                sum += (x - X_CoG) * (z - Z_CoG)  # we add the value for the actual point
        return sum / counter

    def calcul_every_parameters(self, x_start, x_end, X_CoG, Y_CoG, Z_CoG):
        list_frame = Form()
        for i in range(len(self.shape)):
            if x_start <= self.shape[i].x_coordinate <= x_end:
                list_frame.__append__(self.shape[i])
        radius_of_inertia_x2 = list_frame.calcul_square_inertial_radius_x(X_CoG, Y_CoG)
        radius_of_inertia_y2 = list_frame.calcul_square_inertial_radius_y(X_CoG, Z_CoG)
        radius_of_inertia_z2 = list_frame.calcul_square_inertial_radius_z(X_CoG, Y_CoG)
        average_xy = list_frame.calcul_average_xy(X_CoG, Y_CoG)
        average_yz = list_frame.calcul_average_yz(Y_CoG, Z_CoG)
        average_xz = list_frame.calcul_average_xz(X_CoG, Z_CoG)
        return radius_of_inertia_x2, radius_of_inertia_y2, radius_of_inertia_z2, average_xy, average_yz, average_xz

    def plotting(self):
        list_x_coordinates = []
        list_y_coordinates = []
        list_z_coordinates = []
        for frame in self.shape:
            x = frame.x_coordinate
            for coordinate in frame.coordinates:
                y = coordinate[0]
                z = -coordinate[1]
                list_x_coordinates.append(x)
                list_y_coordinates.append(y)
                list_z_coordinates.append(z)
        list_z_coordinates = np.array(list_z_coordinates)
        list_y_coordinates = np.array(list_y_coordinates)
        list_x_coordinates = np.array(list_x_coordinates)
        fig = plt.figure()
        ax = fig.gca(projection="3d")
        ax.scatter(list_x_coordinates, list_y_coordinates, list_z_coordinates, label="courbe", marker='d')
        ax.set_title('test')
        plt.tight_layout()
        plt.show()

    def plot_one_frame(self, x):
        list_x_coordinates = []
        list_y_coordinates = []
        for frame in self.shape:
            if frame.x_coordinate == x:
                for coordinate in frame.coordinates:
                    list_x_coordinates.append(coordinate[0])
                    list_y_coordinates.append(coordinate[1])
        plt.plot(list_x_coordinates, list_y_coordinates)
        plt.show()

    def checking(self):
        for frame in self.shape:
            for i in range(len(frame.coordinates)):
                for j in range(len(frame.coordinates)):
                    if frame.coordinates[i][0] == frame.coordinates[j][0] and frame.coordinates[i][1] == frame.coordinates[j][1] and i != j:
                        if frame.coordinates[i][0]==frame.coordinates[j][0]:
                            print("pb y")
                        if frame.coordinates[i][1]==frame.coordinates[j][0]:
                            print("pb x")