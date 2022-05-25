import numpy as np
class Form:
    def __init__(self):
        self.shape=[]

    def __append__(self,frame):
        self.shape.append(frame)

    def center_of_gravity_no_mass(self,xb,xe):
        les_y=[]
        les_z=[]
        for frame in self.shape:
            if frame.x<=xe and frame.x>=xb:
                xg=(xb+xe)/2
                for coord in frame.coords:
                    les_y.append(coord[0])
                    les_y.append(-coord[0])
                    les_z.append(coord[1])
        return xg,np.mean(les_y),np.mean(les_z)

    def correction_of_coordinates(self):
        n=len(self.shape)
        for j in range(n):
            x=self.shape[j].x
            z_fr = []  # all the z of the frame
            y_fr = []
            coords=self.shape[j].coords
            n_coord=len(coords)
            for i in range(n_coord):
                z_fr.append(coords[i][1])
                y_fr.append(coords[i][0])
            max_z = max(z_fr)  # we save the max of z
            max_y = max(y_fr)
            for coord in coords:
                if coord[1] < max_z and coord[0] < max_y:
                    self.shape[j].__append__((coord[0],max_z))
        return self

    def conversion_coordinate_to_pdstrip(self,midship):
        for frame in self.shape:
            frame.x=frame.x-midship
        return self

    def x_coordinates (self):
        x_coordinate=[]
        for frame in self.shape:
            x_coordinate.append(frame.x)
        return (x_coordinate)

    def calcul_rx2(self,yg,zg):
        """inputs are a list of coord and yg zg coordinates of the center of gravity
            it returns the square of the inertial radius along x axis, by an average of (y-yg)**2+(z-zg)**2"""
        sum = 0  # initialization of the sum
        nb=0
        for frame in self.shape:
            for coord in frame.coords:
                nb+=1
                z=coord[1]
                y=coord[0]
                sum += (y - yg) ** 2 + (z - zg) ** 2  # we add the value for the actual point
            for coord in frame.coords:
                # we do the same thing for the mirror points
                nb+=1
                y = -coord[0]
                z = coord[1]
                sum += (y - yg) ** 2 + (z - zg) ** 2
        # we return an average
        return sum / nb

    def calcul_ry2(self,xg,zg):
        sum = 0  # initialization of the sum
        nb=0
        for frame in self.shape:
            x=frame.x
            for coord in frame.coords:
                nb += 1
                z = coord[1]
                sum += (x - xg) ** 2 + (z - zg) ** 2  # we add the value for the actual point
        # we return an average
        return sum / nb

    def calcul_rz2(self,xg,yg):
        """inputs are a list of coord and yg zg coordinates of the center of gravity
                    it returns the square of the inertial radius along x axis, by an average of (y-yg)**2+(z-zg)**2"""
        sum = 0  # initialization of the sum
        nb = 0
        for frame in self.shape:
            x=frame.x
            for coord in frame.coords:
                nb += 1
                y = coord[0]
                sum += (x - xg) ** 2 + (y - yg) ** 2  # we add the value for the actual point
            for coord in frame.coords:
                # we do the same thing for the mirror points
                nb += 1
                y = -coord[0]
                sum += (x - xg) ** 2 + (y - yg) ** 2
        # we return an average
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
            for coord in frame.coords:
                # we do the same thing for the mirror points
                nb += 1
                y = -coord[0]
                sum += (x - xg) * (y - yg)
        # we return an average
        return sum / nb

    def calcul_yz(self,yg,zg):
        sum = 0  # initialization of the sum
        nb = 0
        for frame in self.shape:
            for coord in frame.coords:
                nb += 1
                y = coord[0]
                z=coord[1]
                sum += (y - yg)*(z-zg)  # we add the value for the actual point
            for coord in frame.coords:
                # we do the same thing for the mirror points
                nb += 1
                y = -coord[0]
                z=coord[1]
                sum += (y - yg)*(z-zg)
        # we return an average
        return sum / nb

    def calcul_xz(self,xg,zg):
        sum = 0  # initialization of the sum
        nb = 0
        for frame in self.shape:
            x=frame.x
            for coord in frame.coords:
                nb += 1
                z = coord[1]
                sum += (x - xg) * (z - zg)  # we add the value for the actual point
        return sum / nb

    def calcul_all(self,xb,xe,xg,yg,zg):
        list_frame = Form()
        for i in range(len(self.shape)):
            if self.shape[i].x <= xe and self.shape[i].x >= xb:
                list_frame.__append__(self.shape[i])
        rx2=list_frame.calcul_rx2(xg,yg)
        ry2=list_frame.calcul_ry2(xg,zg)
        rz2=list_frame.calcul_rz2(xg,yg)
        xy=list_frame.calcul_xy(xg,yg)
        yz=list_frame.calcul_yz(yg,zg)
        xz=list_frame.calcul_xz(xg,zg)
        return rx2,ry2,rz2,xy,yz,xz