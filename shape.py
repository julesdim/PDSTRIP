import numpy as np
import matplotlib.pyplot as plt

import frames
import loading as ld
import shape


class Form:
    """That a class to define the form of the ship, it's a list of frame

    :argument
    ---------
    shape: a list
        it's a list of frame for each axes"""

    def __init__(self):
        self.shape = []

    def __append__(self, new_frame):
        """That function appends a new element to the existing list

        :argument
        -----------
        new_frame: a frame object
            it's a new frame defined by a x coordinates and different points for that x

        :returns
        -----------
        A new element is added to the existing shape"""
        self.shape.append(new_frame)

    def center_of_gravity_no_mass_for_coordinates(self, x_start, x_end):
        """That function allows the user to know the center of gravity if there's no mass between the x_start and the
        x_end of the section

        :argument
        ---------
        x_start: a float
            the x coordinate at the start of the section
        x_end: a float
            the x coordinate at the end of the section

        :returns
        -----------
        x_CoG: a float
            it corresponds to the center of the volume of the x axis
        y_CoG: a float
            it corresponds to the center of the volume of the y axis
        z_CoG: a float
            it corresponds to the center of the volume of the z axis"""
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
        """That function corrects the coordinates if it misses a point at the maximum z to get the good Z_CoG

        :argument
        ----------
        self: a form object

        :returns
        -----------
        self: a form object
            the point needed are added to the current form """
        n = len(self.shape)
        for j in range(n):
            list_z_coordinates_of_frame = []  # all the z of the frame
            list_y_coordinates_of_frame = []
            coordinates = self.shape[j].coordinates
            number_coordinates = len(coordinates)
            for i in range(number_coordinates):
                list_z_coordinates_of_frame.append(coordinates[i][1])
                list_y_coordinates_of_frame.append(coordinates[i][0])
            maximum_z = max(list_z_coordinates_of_frame)  # we save the max of z in pd strip coordinates, that means
            # z to the ground
            maximum_y = max(list_y_coordinates_of_frame)
            for coordinate in coordinates:
                if coordinate[1] < maximum_z and abs(coordinate[0]) < maximum_y:
                    self.shape[j].__append__((coordinate[0], maximum_z))
        return self

    def conversion_coordinate_to_pdstrip(self, midship):
        """That function changes the x coordinate into the PD strip system of coordinate

        :argument
        ---------
        midship: a float
            that's the middle of the ship, defined by the length between perpendicular divided by 2

        :returns
        ---------
        self: a form object
            that's the same frames but with different x_coordinates, x-midship for every frame"""
        for frame in self.shape:
            frame.x_coordinate = frame.x_coordinate - midship
        return self

    def x_coordinates(self):
        """That functions permits to get each x coordinate of the frame to check if there's no missing frame

        :argument
        ---------
        self: a form object
            the current form

        :returns
        ---------
        x_coordinate: a list
            the list of x coordinate of the frames
        """
        x_coordinates = []
        for frame in self.shape:
            x_coordinates.append(frame.x)
        return x_coordinates

    def calcul_square_inertial_radius_x(self, y_CoG, Z_CoG):
        """That function calcul the square of the inertial radius relating to the axis through the center of gravity
        parallel to the x-axis.

        :argument
        ----------
        Y_CoG: a float
            the y coordinate of self, the current form
        Z_CoG: a float
            the z coordinate of self, the current form

        :returns
        -----------
        rx2: a float
            this is the average of (y - y_CoG) ** 2 + (z - Z_CoG) ** 2
        """
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
        """That function calcul the square of the inertial radius relating to the axis through the center of gravity
                parallel to the y-axis.

                :argument
                ----------
                X_CoG: a float
                    the x coordinate of self, the current form
                Z_CoG: a float
                    the z coordinate of self, the current form

                :returns
                -----------
                ry2: a float
                    this is the average of (x - x_CoG) ** 2 + (z - Z_CoG) ** 2
                """
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
        """That function calcul the square of the inertial radius relating to the axis through the center of gravity
        parallel to the z-axis.

        :argument
        ----------
        X_CoG: a float
            the y coordinate of self, the current form
        Y_CoG: a float
            the z coordinate of self, the current form

        :returns
        -----------
        rz2: a float
            this is the average of (x - X_CoG) ** 2 + (y - Y_CoG) ** 2
        """
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
        """That function computes the mass weighted average of (x-X_CoG)*(y-Y_CoG) for self, the current form object

        :argument
        ----------
        X_CoG: a float
            the center of gravity of the current form along x-axis
        Y_CoG: a float
            the center of gravity of the current form along y-axis

        :returns
        ----------
        xy: a float
            the average of the (x-X_CoG)*(y-Y_CoG) for the current form"""
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
        """That function computes the mass weighted average of (y-Y_CoG)*(z-Z_CoG) for self, the current form object

                :argument
                ----------
                Y_CoG: a float
                    the center of gravity of the current form along y-axis
                Z_CoG: a float
                    the center of gravity of the current form along z-axis

                :returns
                ----------
                yz: a float
                    the average of the (y-Y_CoG)*(z-Z_CoG) for the current form"""
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
        """That function computes the mass weighted average of (x-X_CoG)*(z-Z_CoG) for self, the current form object

                :argument
                ----------
                X_CoG: a float
                    the center of gravity of the current form along x-axis
                Z_CoG: a float
                    the center of gravity of the current form along z-axis

                :returns
                ----------
                xz: a float
                    the average of the (x-X_CoG)*(z-Z_CoG) for the current form"""
        sum = 0  # initialization of the sum
        counter = 0
        for frame in self.shape:
            x = frame.x_coordinate
            for coordinate in frame.coordinates:
                counter += 1
                z = coordinate[1]
                sum += (x - X_CoG) * (z - Z_CoG)  # we add the value for the actual point
        return sum / counter

    def calcul_every_parameters(self, x_start, x_end, X_CoG, Y_CoG, Z_CoG, weightloading):
        """That function creates a new form, it keeps just the frame between a section, from the x_start to the x_end.
        For that form it computes all the information, the square of the inertial radius for every axis and the
        average for xy, yz and xz.

        :argument
        ---------
        x_start: a float
            the x coordinate of the start section
        x_end: a float
            the x coordinate of the end section
        X_CoG: a float
            the x coordinate of the center of gravity for the section
        Y_CoG: a float
            the y coordinate of the center of gravity for the section
        Z_CoG: a float
            the z coordinate of the center of gravity for the section

        :returns
        ---------
        radius_of_inertia_x2: a float
            the square of the inertial radius relating to the axis through the center of gravity
        parallel to the x-axis for the section
        radius_of_inertia_y2: a float
            the square of the inertial radius relating to the axis through the center of gravity
        parallel to the y-axis for the section
        radius_of_inertia_z2: a float
            the square of the inertial radius relating to the axis through the center of gravity
        parallel to the z-axis for the section
        average_xy: a float
            the mass weighted average of (x-X_CoG)*(y-Y_CoG) for the section
        average_yz: a float
            the mass weighted average of (y-Y_CoG)*(z-Z_CoG) for the section
        average_xz: a float
            the mass weighted average of (x-X_CoG)*(z-Z_CoG) for the section"""
        list_frame = Form()
        for i in range(len(self.shape)):
            if x_start <= self.shape[i].x_coordinate <= x_end:
                list_frame.__append__(self.shape[i])
        radius_of_inertia_x2 = self.calcul_square_inertial_radius_x_mass_average(weightloading, Y_CoG, Z_CoG, x_start,
                                                                                 x_end)
        radius_of_inertia_y2 = list_frame.calcul_square_inertial_radius_y(X_CoG, Z_CoG)
        radius_of_inertia_z2 = list_frame.calcul_square_inertial_radius_z(X_CoG, Y_CoG)
        average_xy = list_frame.calcul_average_xy(X_CoG, Y_CoG)
        average_yz = list_frame.calcul_average_yz(Y_CoG, Z_CoG)
        average_xz = list_frame.calcul_average_xz(X_CoG, Z_CoG)
        return radius_of_inertia_x2, radius_of_inertia_y2, radius_of_inertia_z2, average_xy, average_yz, average_xz

    def plotting(self):
        """That function plots the current form in 3D

        :argument
        ----------
        self: a form object
            the current form

        :returns
        ------------
            It prints the current form in 3D"""
        list_x_coordinates = []
        list_y_coordinates = []
        list_z_coordinates = []
        for frame in self.shape:
            x = frame.x_coordinate
            for coordinate in frame.coordinates:
                y = coordinate[0]
                z = coordinate[1]
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
        """That function plots one frame of the form for an x written by the user

        :argument
        ------------
        x: a float
            corresponds to an x coordinate that is part of the frames

        :returns
        ----------
        It plots a graph in 2D for one frame
        """
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
        """That functions checks if there are not 2 same points, with the same coordinates

        :argument
        ---------
        self: a form object
            the current form

        :returns
        -----------
        It prints an error message if there are two same coordinates
        """
        for frame in self.shape:
            for i in range(len(frame.coordinates)):
                for j in range(len(frame.coordinates)):
                    if frame.coordinates[i][0] == frame.coordinates[j][0] and \
                            frame.coordinates[i][1] == frame.coordinates[j][1] and i != j:
                        if frame.coordinates[i][0] == frame.coordinates[j][0]:
                            print("pb y")
                        if frame.coordinates[i][1] == frame.coordinates[j][0]:
                            print("pb x")

    def calcul_square_inertial_radius_x_mass_average(self, weightloading, Y_Cog, Z_Cog, x_start, x_end):
        n = len(self.shape)
        sum = 0
        counter = 0
        real_start = 0
        real_end = 0
        total_mass = weightloading.mass_calculation_for_coordinates(x_start, x_end)
        for i in range(1, n):
            if x_start <= self.shape[i].x_coordinate <= x_end:
                if i == n - 1 and self.shape[i].x_coordinate == x_end:
                    real_end = x_end
                    real_start = (self.shape[i - 1].x_coordinate + self.shape[i].x_coordinate) / 2
                if i == 1 and self.shape[i - 1].x_coordinate == x_start:
                    real_start = x_start
                    real_end = (self.shape[i].x_coordinate + self.shape[i + 1].x_coordinate) / 2
                elif 1 < i < n - 1:
                    x_start_part = (self.shape[i - 1].x_coordinate + self.shape[i].x_coordinate) / 2
                    x_end_part = (self.shape[i].x_coordinate + self.shape[i + 1].x_coordinate) / 2
                    real_start = max([x_start, x_start_part])
                    real_end = min([x_end_part, x_end])
                real_mass = weightloading.mass_calculation_for_coordinates(real_start, real_end)
                if total_mass != 0:
                    number_of_point=len(self.shape[i].coordinates)
                    for coord in self.shape[i].coordinates:
                        y = coord[0]
                        z = coord[1]
                        sum += ((y - Y_Cog) ** 2 + (z - Z_Cog) ** 2) * (real_mass/number_of_point) / total_mass
                if total_mass == 0:
                    for coord in self.shape[i].coordinates:
                        y = coord[0]
                        z = coord[1]
                        counter += 1
                        sum += (y - Y_Cog) ** 2 + (z - Z_Cog) ** 2
                    sum /= counter
        return sum

    def calcul_square_inertial_radius_y_mass_average(self, weightloading, X_Cog, Z_Cog, x_start, x_end):
        n = len(self.shape)
        sum = 0
        counter = 0
        real_start = 0
        real_end = 0
        total_mass = weightloading.mass_calculation_for_coordinates(x_start, x_end)
        for i in range(1, n):
            x = self.shape[i].x_coordinate
            if x_start <= self.shape[i].x_coordinate <= x_end:
                if i == n - 1 and self.shape[i].x_coordinate == x_end:
                    real_end = x_end
                    x = x_end
                    real_start = (self.shape[i - 1].x_coordinate + self.shape[i].x_coordinate) / 2
                if i == 1 and self.shape[i - 1].x_coordinate == x_start:
                    real_start = x_start
                    x = x_start
                    real_end = (self.shape[i].x_coordinate + self.shape[i + 1].x_coordinate) / 2
                elif 1 < i < n - 1:
                    x_start_part = (self.shape[i - 1].x_coordinate + self.shape[i].x_coordinate) / 2
                    x_end_part = (self.shape[i].x_coordinate + self.shape[i + 1].x_coordinate) / 2
                    real_start = max([x_start, x_start_part])
                    real_end = min([x_end_part, x_end])
                real_mass = weightloading.mass_calculation_for_coordinates(real_start, real_end)
                if total_mass != 0:
                    number_of_point = len(self.shape[i].coordinates)
                    for coord in self.shape[i].coordinates:
                        z = coord[1]
                        sum += ((x - X_Cog) ** 2 + (z - Z_Cog) ** 2) * (real_mass/number_of_point) / total_mass
                if total_mass == 0:
                    for coord in self.shape[i].coordinates:
                        z = coord[1]
                        counter += 1
                        sum += (x - X_Cog) ** 2 + (z - Z_Cog) ** 2
                    sum /= counter
        return sum

    def calcul_square_inertial_radius_z_mass_average(self, weightloading, X_Cog, Y_Cog, x_start, x_end):
        n = len(self.shape)
        sum = 0
        counter = 0
        real_start = 0
        real_end = 0
        total_mass = weightloading.mass_calculation_for_coordinates(x_start, x_end)
        for i in range(1, n):
            x = self.shape[i].x_coordinate
            if x_start <= self.shape[i].x_coordinate <= x_end:
                if i == n - 1 and self.shape[i].x_coordinate == x_end:
                    real_end = x_end
                    x = x_end
                    real_start = (self.shape[i - 1].x_coordinate + self.shape[i].x_coordinate) / 2
                if i == 1 and self.shape[i - 1].x_coordinate == x_start:
                    real_start = x_start
                    x = x_start
                    real_end = (self.shape[i].x_coordinate + self.shape[i + 1].x_coordinate) / 2
                elif 1 < i < n - 1:
                    x_start_part = (self.shape[i - 1].x_coordinate + self.shape[i].x_coordinate) / 2
                    x_end_part = (self.shape[i].x_coordinate + self.shape[i + 1].x_coordinate) / 2
                    real_start = max([x_start, x_start_part])
                    real_end = min([x_end_part, x_end])
                real_mass = weightloading.mass_calculation_for_coordinates(real_start, real_end)
                if total_mass != 0:
                    number_of_point = len(self.shape[i].coordinates)
                    for coord in self.shape[i].coordinates:
                        y = coord[0]
                        sum += ((x - X_Cog) ** 2 + (y - Y_Cog) ** 2) * (real_mass/number_of_point) / total_mass
                if total_mass == 0:
                    for coord in self.shape[i].coordinates:
                        y = coord[0]
                        counter += 1
                        sum += (x - X_Cog) ** 2 + (y - Y_Cog) ** 2
                    sum /= counter
        return sum

    def calcul_xy_mass_average(self, weightloading, X_Cog, Y_Cog, x_start, x_end):
        n = len(self.shape)
        sum = 0
        counter = 0
        real_start = 0
        real_end = 0
        total_mass = weightloading.mass_calculation_for_coordinates(x_start, x_end)
        for i in range(1, n):
            x = self.shape[i].x_coordinate
            if x_start <= self.shape[i].x_coordinate <= x_end:
                if i == n - 1 and self.shape[i].x_coordinate == x_end:
                    real_end = x_end
                    x = x_end
                    real_start = (self.shape[i - 1].x_coordinate + self.shape[i].x_coordinate) / 2
                if i == 1 and self.shape[i - 1].x_coordinate == x_start:
                    real_start = x_start
                    x = x_start
                    real_end = (self.shape[i].x_coordinate + self.shape[i + 1].x_coordinate) / 2
                elif 1 < i < n - 1:
                    x_start_part = (self.shape[i - 1].x_coordinate + self.shape[i].x_coordinate) / 2
                    x_end_part = (self.shape[i].x_coordinate + self.shape[i + 1].x_coordinate) / 2
                    real_start = max([x_start, x_start_part])
                    real_end = min([x_end_part, x_end])
                real_mass = weightloading.mass_calculation_for_coordinates(real_start, real_end)
                if total_mass != 0:
                    number_of_point = len(self.shape[i].coordinates)
                    for coord in self.shape[i].coordinates:
                        y = coord[0]
                        sum += ((x - X_Cog) * (y - Y_Cog)) * (real_mass/number_of_point) / total_mass
                if total_mass == 0:
                    for coord in self.shape[i].coordinates:
                        y = coord[0]
                        counter += 1
                        sum += (x - X_Cog) * (y - Y_Cog)
                    sum /= counter
        return sum

    def calcul_yz_mass_average(self, weightloading, Y_Cog, Z_Cog, x_start, x_end):
        n = len(self.shape)
        sum = 0
        counter = 0
        real_start = 0
        real_end = 0
        total_mass = weightloading.mass_calculation_for_coordinates(x_start, x_end)
        for i in range(1, n):
            if x_start <= self.shape[i].x_coordinate <= x_end:
                if i == n - 1 and self.shape[i].x_coordinate == x_end:
                    real_end = x_end
                    real_start = (self.shape[i - 1].x_coordinate + self.shape[i].x_coordinate) / 2
                if i == 1 and self.shape[i - 1].x_coordinate == x_start:
                    real_start = x_start
                    real_end = (self.shape[i].x_coordinate + self.shape[i + 1].x_coordinate) / 2
                elif 1 < i < n - 1:
                    x_start_part = (self.shape[i - 1].x_coordinate + self.shape[i].x_coordinate) / 2
                    x_end_part = (self.shape[i].x_coordinate + self.shape[i + 1].x_coordinate) / 2
                    real_start = max([x_start, x_start_part])
                    real_end = min([x_end_part, x_end])
                real_mass = weightloading.mass_calculation_for_coordinates(real_start, real_end)
                if total_mass != 0:
                    number_of_point = len(self.shape[i].coordinates)
                    for coord in self.shape[i].coordinates:
                        y = coord[0]
                        z = coord[1]
                        sum += ((y - Y_Cog) * (z - Z_Cog)) * (real_mass/number_of_point) / total_mass
                if total_mass == 0:
                    for coord in self.shape[i].coordinates:
                        y = coord[0]
                        z = coord[1]
                        counter += 1
                        sum += (y - Y_Cog) * (z - Z_Cog)
                    sum /= counter
        return sum

    def calcul_xz_mass_average(self, weightloading, X_Cog, Z_Cog, x_start, x_end):
        n = len(self.shape)
        sum = 0
        counter = 0
        real_start = 0
        real_end = 0
        total_mass = weightloading.mass_calculation_for_coordinates(x_start, x_end)
        for i in range(1, n):
            x = self.shape[i].x_coordinate
            if x_start <= self.shape[i].x_coordinate <= x_end:
                if i == n - 1 and self.shape[i].x_coordinate == x_end:
                    real_end = x_end
                    x = x_end
                    real_start = (self.shape[i - 1].x_coordinate + self.shape[i].x_coordinate) / 2
                if i == 1 and self.shape[i - 1].x_coordinate == x_start:
                    real_start = x_start
                    x = x_start
                    real_end = (self.shape[i].x_coordinate + self.shape[i + 1].x_coordinate) / 2
                elif 1 < i < n - 1:
                    x_start_part = (self.shape[i - 1].x_coordinate + self.shape[i].x_coordinate) / 2
                    x_end_part = (self.shape[i].x_coordinate + self.shape[i + 1].x_coordinate) / 2
                    real_start = max([x_start, x_start_part])
                    real_end = min([x_end_part, x_end])
                real_mass = weightloading.mass_calculation_for_coordinates(real_start, real_end)
                if total_mass != 0:
                    number_of_point=len(self.shape[i].coordinates)
                    for coord in self.shape[i].coordinates:
                        z = coord[1]
                        counter+=1
                        sum += ((x - X_Cog) * (z - Z_Cog)) * (real_mass/number_of_point) / total_mass
                if total_mass == 0:
                    for coord in self.shape[i].coordinates:
                        z = coord[1]
                        counter += 1
                        sum += (x - X_Cog) * (z - Z_Cog)
                    sum /= counter
        return sum

    def calcul_every_parameters_mass_average(self, x_start, x_end, X_CoG, Y_CoG, Z_CoG, weightloading):
        """That function creates a new form, it keeps just the frame between a section, from the x_start to the x_end.
        For that form it computes all the information, the square of the inertial radius for every axis and the
        average for xy, yz and xz.

        :argument
        ---------
        x_start: a float
            the x coordinate of the start section
        x_end: a float
            the x coordinate of the end section
        X_CoG: a float
            the x coordinate of the center of gravity for the section
        Y_CoG: a float
            the y coordinate of the center of gravity for the section
        Z_CoG: a float
            the z coordinate of the center of gravity for the section

        :returns
        ---------
        radius_of_inertia_x2: a float
            the square of the inertial radius relating to the axis through the center of gravity
        parallel to the x-axis for the section
        radius_of_inertia_y2: a float
            the square of the inertial radius relating to the axis through the center of gravity
        parallel to the y-axis for the section
        radius_of_inertia_z2: a float
            the square of the inertial radius relating to the axis through the center of gravity
        parallel to the z-axis for the section
        average_xy: a float
            the mass weighted average of (x-X_CoG)*(y-Y_CoG) for the section
        average_yz: a float
            the mass weighted average of (y-Y_CoG)*(z-Z_CoG) for the section
        average_xz: a float
            the mass weighted average of (x-X_CoG)*(z-Z_CoG) for the section"""
        radius_of_inertia_x2 = self.calcul_square_inertial_radius_x_mass_average(weightloading, Y_CoG, Z_CoG, x_start,
                                                                                 x_end)
        radius_of_inertia_y2 = self.calcul_square_inertial_radius_y_mass_average(weightloading, X_CoG, Z_CoG, x_start,
                                                                                 x_end)
        radius_of_inertia_z2 = self.calcul_square_inertial_radius_z_mass_average(weightloading, X_CoG, Y_CoG, x_start,
                                                                                 x_end)
        average_xy = self.calcul_xy_mass_average(weightloading, X_CoG, Y_CoG, x_start, x_end)
        average_yz = self.calcul_yz_mass_average(weightloading, Y_CoG, Z_CoG, x_start, x_end)
        average_xz = self.calcul_xz_mass_average(weightloading, X_CoG, Z_CoG, x_start, x_end)
        return radius_of_inertia_x2, radius_of_inertia_y2, radius_of_inertia_z2, average_xy, average_yz, average_xz
