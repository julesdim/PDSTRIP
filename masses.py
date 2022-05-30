import numpy as np


class Mass:
    """A simple class to define a weight by the weight, the beginning, the end, the center of gravity along all the axis
    the linear density at the beginning and at the end, it permits to compute different value of the weight if necessary

    :attributes

    weight: the weight of the mass

    x_start: x_coordinate of the mass start

    x_end: x_coordinate of the mass end

    x_coordinate_CoG: x coordinate of the center of gravity

    y_coordinate_CoG: y coordinate of the center of gravity

    z_coordinate_CoG: z coordinate of the center of gravity

    linear_density_start: linear density of the mass at x_start

    linear_density_end: linear density of the mass at x_end
    """

    def __init__(self, weight, x_start, x_end, x_coordinate_CoG, y_coordinate_CoG, z_coordinate_CoG,
                 linear_density_start, linear_density_end):
        self.weight = weight
        self.x_start = x_start
        self.x_end = x_end
        self.x_coordinate_CoG = x_coordinate_CoG
        self.y_coordinate_CoG = y_coordinate_CoG
        self.z_coordinate_CoG = z_coordinate_CoG
        self.linear_density_start = linear_density_start
        self.linear_density_end = linear_density_end

    def calcul_xg_mass(self):
        """That function permits to the user to compute X_CoG in function of linear density when the program calcul the
        new formula.

        :argument
        self: the current mass

        :returns
        X_CoG: the current x_coordinate of the center of gravity"""
        x_end = self.x_end
        x_start = self.x_start
        linear_density_start = self.linear_density_start
        linear_density_end = self.linear_density_end
        list_of_x_coordinates = np.arange(x_start, x_end + 0.01, 0.01)
        list_of_y_coordinates = (linear_density_end - linear_density_start) / \
                                (x_end - x_start) * (list_of_x_coordinates - x_start) + linear_density_start
        sum = 0
        sum_y = 0
        for i in range(len(list_of_x_coordinates)):
            sum += list_of_x_coordinates[i] * list_of_y_coordinates[i]
            sum_y += list_of_y_coordinates[i]
        return sum / sum_y

    def calcul_x_coordinate_CoG_for_coordinates(self, x_start_part, x_end_part):
        """That function permits to know the center of gravity for a section of the mass in function of the
        linear density's formula

        :argument
        x_start_part: x coordinate of the section start

        x_end_part: x coordinate of the section end

        :returns
        X_CoG: the value of the center of gravity for the section"""
        linear_density_start = self.linear_density_start
        linear_density_end = self.linear_density_end
        list_of_x_coordinates = np.arange(x_start_part, x_end_part + 0.01, 0.01)
        list_of_y_coordinates = (linear_density_end - linear_density_start) / (x_end_part - x_start_part) * (
                list_of_x_coordinates - x_start_part) + linear_density_start
        sum = 0
        sum_y = 0
        for i in range(len(list_of_x_coordinates)):
            sum += list_of_x_coordinates[i] * list_of_y_coordinates[i]
            sum_y += list_of_y_coordinates[i]
        if sum_y == 0:
            print(list_of_x_coordinates)
            print(list_of_y_coordinates)
        return sum / sum_y

    def calcul_linear_density_for_coordinates(self, x_start_part, x_end_part):
        """That function permits to know the value of the linear density at the start part and at the end part to
        compute the linear density

        :argument
        x_start_part: x coordinate of the section start

        x_end_part: x coordinate of the section end

        :returns
        linear_density_at_x_start_part: the value for the x coordinate x_start_part

        linear_density_at_x_end_part: the value for the x coordinate x_end_part
        """
        x_end_of_the_mass = self.x_end
        x_start_of_the_mass = self.x_start
        linear_density_start = self.linear_density_start
        linear_density_end = self.linear_density_end
        coefficient_of_the_line = (linear_density_end - linear_density_start) / (x_end_of_the_mass -
                                                                                     x_start_of_the_mass)
        linear_density_at_x_start_part = linear_density_start + coefficient_of_the_line * (x_start_part -
                                                                                                   x_start_of_the_mass)
        linear_density_at_x_end_part= linear_density_start + coefficient_of_the_line * (x_end_part - x_start_of_the_mass)
        return linear_density_at_x_start_part, linear_density_at_x_end_part

    def calcul_xg_not_the_mid(self, eps=0.00001):
        """That functions permits to compute the new value of linear density, indeed at the beginning the linear density
        is defined equal at the beginning and at the end.

        :argument
        eps: for the precision of the computation

        :returns
        Nothing
        """
        weight = self.weight
        x_coordinate_CoG = self.x_coordinate_CoG
        x_end_mass = self.x_end
        x_start_mass = self.x_start
        linear_density_start = weight / (x_end_mass - x_start_mass)
        gap = x_end_mass - x_start_mass
        coefficient = 0
        i = 0
        while gap > eps and i < 500000:
            ratio = abs(self.calcul_xg_mass() - x_coordinate_CoG) / (x_end_mass - x_start_mass)
            if self.calcul_xg_mass() > x_coordinate_CoG:
                coefficient -= ratio
            if self.calcul_xg_mass() < x_coordinate_CoG:
                coefficient += ratio
            self.linear_density_start = (1 - coefficient) * linear_density_start
            self.linear_density_end = (1 + coefficient) * linear_density_start
            gap = abs(self.calcul_xg_mass() - x_coordinate_CoG)
            i += 1
