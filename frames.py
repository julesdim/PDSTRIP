import matplotlib.pyplot as plt

class Frames:
    def __init__(self,x):
        self.x=x
        self.coords=[]

    def __append__(self,coord):
        self.coords.append(coord)

    def plot(self):
        les_x=[]
        les_y=[]
        for coord in self.coords:
            les_x.append(coord[0])
            les_y.append(coord[1])
        plt.plot(les_x,les_y)
        plt.show()
