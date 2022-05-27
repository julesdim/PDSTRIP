import numpy as np
import matplotlib.pyplot as plt


class Form:
    def __init__(self):
        self.shape = []

    def __append__(self, frame):
        self.shape.append(frame)

    def center_of_gravity_no_mass(self, xb, xe):
        les_y = []
        les_z = []
        for frame in self.shape:
            if xe >= frame.x >= xb:
                xg = (xb + xe) / 2
                for coord in frame.coords:
                    les_y.append(coord[0])
                    les_z.append(coord[1])
        return xg, np.mean(les_y), np.mean(les_z)

    def correction_of_coordinates(self):
        n = len(self.shape)
        for j in range(n):
            z_fr = []  # all the z of the frame
            y_fr = []
            coords = self.shape[j].coords
            n_coord = len(coords)
            for i in range(n_coord):
                z_fr.append(coords[i][1])
                y_fr.append(coords[i][0])
            max_z = min(z_fr)  # we save the max of z in pd strip coordinates, that means z to the ground
            max_y = max(y_fr)
            for coord in coords:
                if coord[1] > max_z and abs(coord[0]) < max_y:
                    self.shape[j].__append__((coord[0], max_z))
        return self

    def conversion_coordinate_to_pdstrip(self, midship):
        for frame in self.shape:
            frame.x = frame.x - midship
        return self

    def x_coordinates(self):
        x_coordinate = []
        for frame in self.shape:
            x_coordinate.append(frame.x)
        return x_coordinate

    def calcul_rx2(self, yg, zg):
        """inputs are a list of coord and yg zg coordinates of the center of gravity
            it returns the square of the inertial radius along x axis, by an average of (y-yg)**2+(z-zg)**2"""
        sum = 0  # initialization of the sum
        nb = 0
        for frame in self.shape:
            for coord in frame.coords:
                nb += 1
                z = coord[1]
                y = coord[0]
                sum += (y - yg) ** 2 + (z - zg) ** 2  # we add the value for the actual point
        return sum / nb

    def calcul_ry2(self, xg, zg):
        sum = 0  # initialization of the sum
        nb = 0
        for frame in self.shape:
            x = frame.x
            for coord in frame.coords:
                nb += 1
                z = coord[1]
                sum += (x - xg) ** 2 + (z - zg) ** 2  # we add the value for the actual point
        # we return an average
        return sum / nb

    def calcul_rz2(self, xg, yg):
        """inputs are a list of coord and yg zg coordinates of the center of gravity
                    it returns the square of the inertial radius along x axis, by an average of (y-yg)**2+(z-zg)**2"""
        sum = 0  # initialization of the sum
        nb = 0
        for frame in self.shape:
            x = frame.x
            for coord in frame.coords:
                nb += 1
                y = coord[0]
                sum += (x - xg) ** 2 + (y - yg) ** 2  # we add the value for the actual point
        return sum / nb

    def calcul_xy(self, xg, yg):
        """inputs are a list of coord and xg yg coordinates of the center of gravity
            it returns the mass weighted average of (x-xg)(y-yg)"""
        sum = 0  # initialization of the sum
        nb = 0
        for frame in self.shape:
            x = frame.x
            for coord in frame.coords:
                nb += 1
                y = coord[0]
                sum += (x - xg) * (y - yg)  # we add the value for the actual point
        return sum / nb

    def calcul_yz(self, yg, zg):
        sum = 0  # initialization of the sum
        nb = 0
        for frame in self.shape:
            for coord in frame.coords:
                nb += 1
                y = coord[0]
                z = coord[1]
                sum += (y - yg) * (z - zg)  # we add the value for the actual point
        return sum / nb

    def calcul_xz(self, xg, zg):
        sum = 0  # initialization of the sum
        nb = 0
        for frame in self.shape:
            x = frame.x
            for coord in frame.coords:
                nb += 1
                z = coord[1]
                sum += (x - xg) * (z - zg)  # we add the value for the actual point
        return sum / nb

    def calcul_all(self, xb, xe, xg, yg, zg):
        list_frame = Form()
        for i in range(len(self.shape)):
            if xb <= self.shape[i].x <= xe:
                list_frame.__append__(self.shape[i])
        rx2 = list_frame.calcul_rx2(xg, yg)
        ry2 = list_frame.calcul_ry2(xg, zg)
        rz2 = list_frame.calcul_rz2(xg, yg)
        xy = list_frame.calcul_xy(xg, yg)
        yz = list_frame.calcul_yz(yg, zg)
        xz = list_frame.calcul_xz(xg, zg)
        return rx2, ry2, rz2, xy, yz, xz

    def plotting(self):
        les_x = []
        les_y = []
        les_z = []
        for frame in self.shape:
            x = frame.x
            for coord in frame.coords:
                y = coord[0]
                z = -coord[1]
                les_x.append(x)
                les_y.append(y)
                les_z.append(z)
        les_z = np.array(les_z)
        les_y = np.array(les_y)
        les_x = np.array(les_x)
        fig = plt.figure()
        ax = fig.gca(projection="3d")
        ax.scatter(les_x, les_y, les_z, label="courbe", marker='d')
        ax.set_title('test')
        plt.tight_layout()
        plt.show()
        return

    def plot_one_frame(self, x):
        les_x = []
        les_y = []
        for frame in self.shape:
            if frame.x == x:
                for coord in frame.coords:
                    les_x.append(coord[0])
                    les_y.append(coord[1])
        plt.plot(les_x, les_y)
        plt.show()

    def checking(self):
        for frame in self.shape:
            for i in range(len(frame.coords)):
                for j in range(len(frame.coords)):
                    if frame.coords[i][0] == frame.coords[j][0] and frame.coords[i][1] == frame.coords[j][1] and i != j:
                        print("pb")
