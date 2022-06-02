import numpy as np
import matplotlib.pyplot as plt


class Loading:
    """This Class is very simple because it's a list of mass, indeed the loading is nothing more

    :argument
    -----------
    masses: a list
        it's a list of mass object"""

    def __init__(self):
        self.masses = []

    def plot_loading(self, x_start: float, x_end: float):
        """That function permits to the user to print the weightloading, for a list of weight, and with the
        boundaries of the ship

        :argument
        x_start: the start of the ship to print his weight loading

        x_end: the end of the ship

        :returns
        it prints a graph with the loading along the x axis"""
        delt_x = 0.1  # value of the strip to calculate the ship loading
        list_x_coordinates = np.arange(x_start, x_end + delt_x, delt_x)  # coordinates of each strip
        total = len(list_x_coordinates)
        linear_density = [0]  # we initialize the weight loading for x=0, it's equal to 0
        for i in range(total - 1):
            x_inf = list_x_coordinates[i]
            x_up = list_x_coordinates[i + 1]
            # coordinates of the strip i
            mass_element = self.mass_calculation_for_coordinates(x_inf,
                                                                 x_up) / delt_x  # element of weight for the strip
            linear_density.append(mass_element)  # we add to the list
        plt.plot(list_x_coordinates, linear_density)
        plt.title("weight loading")
        plt.show()
        return

    def __append__(self, mass:float):
        """That functions append a new element to the loading

        :argument
        -----------
        mass: a mass object
            the new element of the loading"""
        self.masses.append(mass)

    def mass_calculation_for_coordinates(self, x_start: float, x_end: float):
        """That function computes the value of the mass between two coordinates of a section

        :argument
        -----------
        x_start: x coordinate of the start of the section
        x_end: x_coordinate of the end of the section

        :returns
        -----------
        total_mass: the total mass of the section"""
        number_of_masses = len(self.masses)
        total_mass = 0
        for i in range(number_of_masses):
            x_start_mass = self.masses[i].x_start
            x_end_mass = self.masses[i].x_end
            x_CoG_mass = self.masses[i].x_coordinate_CoG
            linear_density_start = self.masses[i].linear_density_start
            linear_density_end = self.masses[i].linear_density_end
            if x_start_mass < x_end and x_end_mass > x_start:
                real_start = np.max([x_start, x_start_mass])  # real beginning of the weight for the section
                real_end = np.min([x_end, x_end_mass])
                real_linear_density_start = linear_density_start + (real_start - x_start_mass) * \
                                            (linear_density_end - linear_density_start) / (x_end_mass - x_start_mass)
                real_linear_density_end = linear_density_start + (real_end - x_start_mass) * \
                                          (linear_density_end - linear_density_start) / (x_end_mass - x_start_mass)
                if x_CoG_mass != (x_start_mass + x_end_mass) / 2:
                    total_mass += (real_end - real_start) * (real_linear_density_start + real_linear_density_end) / 2
                if x_CoG_mass == (x_start_mass + x_end_mass) / 2:
                    # real end of the weight for the section, if the end of the weight is after the end of the section
                    total_mass += (real_end - real_start) * real_linear_density_start
        return total_mass

    def calcul_center_of_gravity_for_coordinates(self, x_start: float, x_end: float):
        """That function permits to the user to know the center of gravity for a specific section

        :argument
        ----------
        x_start: a float
            x coordinate of the section
        x_end: a float
            x coordinate of the section

        :returns
        -------------
        X_CoG: a float
            x coordinate of the center of gravity of the section
        Y_CoG: a float
            y coordinate of the center of gravity of the section
        Z_CoG: a float
            z coordinate of the center of gravity of the section"""
        total_mass = self.mass_calculation_for_coordinates(x_start, x_end)
        number_of_masses = len(self.masses)
        # initialization of the values
        X_CoG = 0
        Y_CoG = 0
        Z_CoG = 0
        for i in range(number_of_masses):
            x_start_mass = self.masses[i].x_start  # beginning of the weight
            x_end_mass = self.masses[i].x_end  # end of the weight
            if x_start_mass < x_end and x_end_mass > x_start:
                real_start = np.max(
                    [x_start, x_start_mass])  # real beginning of the weight, if the weight begins before the frame
                real_end = np.min([x_end, x_end_mass])
                real_linear_density_start, real_linear_density_end = \
                    self.masses[i].calcul_linear_density_for_coordinates(real_start, real_end)
                real_mass = (real_end - real_start) * (real_linear_density_start + real_linear_density_end) / 2
                # proportion of the weight situated between the section
                if real_linear_density_start != 0 and real_linear_density_end != 0:
                    X_CoG = self.masses[i].calcul_x_coordinate_CoG_for_coordinates(real_start, real_end)
                else:
                    X_CoG = 0
                X_CoG += real_mass * X_CoG
                Y_CoG += real_mass * self.masses[i].y_coordinate_CoG
                Z_CoG += real_mass * self.masses[i].z_coordinate_CoG
        return X_CoG / total_mass, Y_CoG / total_mass, Z_CoG / total_mass

    def pdstrip_coordinates_conversion(self, midship: float):
        """That functions converts every coordinates depending of the PD strip coordinate system

        :argument
        ------------
        midship: a float
            the length of the midship, defined by the length between perpendiculars divide by 2

        :returns
        -------------
        It changes the x coordinates by x-midship (the pd strip system the pd strip system places the origin in
        the middle of the boat) and it changes the z coordinate into -z because the z axis is directed downwards"""
        for mass in self.masses:
            mass.x_start = mass.x_start - midship
            mass.x_end = mass.x_end - midship
            mass.x_coordinate_CoG = mass.x_coordinate_CoG - midship
