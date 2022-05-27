import matplotlib.pyplot as plt


class Frames:
    def __init__(self, x):
        self.x = x
        self.coords = []

    def __append__(self, coord):
        not_in_frame=True
        for i in range (len(self.coords)):
            if coord[0]==self.coords[i][0] and coord[1]==self.coords[i][1]:
                not_in_frame=False
        if not_in_frame:
            self.coords.append(coord)

    def plot(self):
        les_x = []
        les_y = []
        for coord in self.coords:
            les_x.append(coord[0])
            les_y.append(coord[1])
        plt.plot(les_x, les_y)
        plt.show()
