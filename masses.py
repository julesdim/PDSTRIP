import numpy as np


class Mass:
    """A simple class to define a weight by the weight, the beginning, the end, the center of gravity along all the axis
    the linear density at the beginning and at the end, it permits to compute different value of the weight if necessary
    """

    def __init__(self, weight, x_beginning, x_end, x_coordinate_CoG, y_coordinate_CoG, z_coordinate_CoG,
                 linear_density_beginning, linear_density_end):
        self.weight = weight
        self.x_beginning = x_beginning
        self.x_end = x_end
        self.x_coordinate_CoG = x_coordinate_CoG
        self.y_coordinate_CoG = y_coordinate_CoG
        self.z_coordinate_CoG = z_coordinate_CoG
        self.linear_density_beginning = linear_density_beginning
        self.linear_density_end = linear_density_end

    def calcul_xg_mass(self):
        x_end = self.x_end
        x_beginning = self.x_beginning
        linear_density_beginning = self.linear_density_beginning
        linear_density_end = self.linear_density_end
        list_of_x_coordinates = np.arange(x_beginning, x_end + 0.01, 0.01)
        list_of_y_coordinates = (linear_density_end - linear_density_beginning) / \
                                (x_end - x_beginning) * (list_of_x_coordinates - x_beginning) + linear_density_beginning
        sum = 0
        sum_y = 0
        for i in range(len(list_of_x_coordinates)):
            sum += list_of_x_coordinates[i] * list_of_y_coordinates[i]
            sum_y += list_of_y_coordinates[i]
        return sum / sum_y

    def calcul_x_coordinate_CoG_for_coordinates(self, x_beginning_part, x_end_part):
        linear_density_beginning = self.linear_density_beginning
        linear_density_end = self.linear_density_end
        list_of_x_coordinates = np.arange(x_beginning_part, x_end_part + 0.01, 0.01)
        list_of_y_coordinates = (linear_density_end - linear_density_beginning) / (x_end_part - x_beginning_part) * (
                list_of_x_coordinates - x_beginning_part) + linear_density_beginning
        sum = 0
        sum_y = 0
        for i in range(len(list_of_x_coordinates)):
            sum += list_of_x_coordinates[i] * list_of_y_coordinates[i]
            sum_y += list_of_y_coordinates[i]
        if sum_y == 0:
            print(list_of_x_coordinates)
            print(list_of_y_coordinates)
        return sum / sum_y

    def calcul_linear_density_for_coordinates(self, x_beginning_part, x_end_part):
        x_end_of_the_mass = self.x_end
        x_beginning_of_the_mass = self.x_beginning
        linear_density_beginning = self.linear_density_beginning
        linear_density_end = self.linear_density_end
        coefficient_of_the_line = (linear_density_end - linear_density_beginning) / (x_end_of_the_mass -
                                                                                     x_beginning_of_the_mass)
        linear_density_at_x_beginning_part = linear_density_beginning + coefficient_of_the_line * (x_beginning_part -
                                                                                              x_beginning_of_the_mass)
        linear_density_at_x_end_part= linear_density_beginning + coefficient_of_the_line * (x_end_part - x_beginning_of_the_mass)
        return linear_density_at_x_beginning_part, linear_density_at_x_end_part

    def calcul_xg_not_the_mid(self, eps=0.00001):
        weight = self.weight
        x_coordinate_CoG = self.x_coordinate_CoG
        x_end_mass = self.x_end
        x_beginning_mass = self.x_beginning
        linear_density_beginning = weight / (x_end_mass - x_beginning_mass)
        gap = x_end_mass - x_beginning_mass
        coefficient = 0
        i = 0
        while gap > eps and i < 500000:
            ratio = abs(self.calcul_xg_mass() - x_coordinate_CoG) / (x_end_mass - x_beginning_mass)
            if self.calcul_xg_mass() > x_coordinate_CoG:
                coefficient -= ratio
            if self.calcul_xg_mass() < x_coordinate_CoG:
                coefficient += ratio
            self.linear_density_beginning = (1 - coefficient) * linear_density_beginning
            self.linear_density_end = (1 + coefficient) * linear_density_beginning
            gap = abs(self.calcul_xg_mass() - x_coordinate_CoG)
            i += 1
        return self.linear_density_beginning, self.linear_density_end
