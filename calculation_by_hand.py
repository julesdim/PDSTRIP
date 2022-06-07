import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import quad
import csv
import shape as shape
import frames as fr

wave_length = 100
wave_number = 2 * np.pi / wave_length
wave_freq = (10 * wave_number) ** 0.5
a = 0.5
g = 10
rho = 1000
B = 10
T = 4.5
wave_per = 2 * np.pi / wave_freq
print(wave_per)
comp = 1j


# we suppose g=10 m/s2
def eta(x, t):
    if wave_length >= 5000:
        return rho * g * B * np.real(a * np.exp((wave_freq * t - wave_number * (x)) * 1j))
    else:
        return (1 - ((wave_freq ** 2) * T) / (g)) * B * rho * g * a * np.real(
            np.exp((wave_freq * t - wave_number * (x)) * 1j))


def func(x):
    return eta(x, 0)


def func2(t):
    return eta(0, t)


def FzFK2(t):
    return np.real(quad(eta, 0, wave_per, args=t)[0])


def FzFK(x):
    return np.real(eta(x, 0))


def convert_N_to_ton(W):
    return W * 10 ** (-4)


Fz = quad(lambda x: FzFK2(x), -50, 50)[0]


def collection_of_coordinates(filename: str):
    """That functions read a Pias file of coordinates, and it reads every coordinate to return a shape object

    :parameter
    -----------
    filename: a text variable corresponding to the pias file of coordinates

    :returns
    ----------
    form: A Form object corresponding to a list of frame, defined by a x coordinate and coordinates of point for that
    frame
    """
    file = open(filename, "r", encoding="utf-8")
    the_lines = csv.reader(file)
    line_counter = 0
    start_line_of_the_frame = 0
    end_line_of_the_frame = 1000
    boolean_for_beginning_of_the_frame = True
    # we can know if we are at the beginning of the frame to get the x coordinate of the frame
    form_of_the_ship = shape.Form()  # initialisation of the list of coordinates
    for line in the_lines:
        line_formatted = line[0].strip().split()  # formatting the line
        if line_counter == 0:
            total_number_of_frame = float(line_formatted[0])  # to know the number of frame
        if line_counter != 0 and len(line_formatted) == 1 and boolean_for_beginning_of_the_frame:
            x_coordinate = (float(line_formatted[0]))
            # if there is just one coordinate, it is the position along x-axis, if beg_frame==True
            start_line_of_the_frame = line_counter
            current_frame = fr.Frames(x_coordinate)
            boolean_for_beginning_of_the_frame = False  # As we just passed the start of the frame, next is false
        if line_counter != 0 and len(line_formatted) == 3:
            y_coordinate = (float(line_formatted[0]))
            z_coordinate = (float(line_formatted[1]))
            current_frame.__append__((y_coordinate, z_coordinate))  # we append to the list
            if y_coordinate != 0:
                current_frame.__append__((-y_coordinate, z_coordinate))
            boolean_for_beginning_of_the_frame = True
            # the next time len(new)==1 it will be the beginning of a new frame
        if len(line_formatted) == 1 and line_counter == start_line_of_the_frame + 1:
            number_points_of_the_current_frame = int(line_formatted[0])
            end_line_of_the_frame = line_counter + number_points_of_the_current_frame
        if line_counter == end_line_of_the_frame:
            form_of_the_ship.__append__(current_frame)
        line_counter += 1
    file.close()
    return form_of_the_ship


def calcul_simple_vol(lamb):
    return 5  * T * (lamb + 50)


def Buoyancy(lamb):
    return calcul_simple_vol(lamb) * 10000


def Fk(lamb):
    return quad(lambda x: FzFK2(x), -50, lamb)[0]


def Fk2(lamb):
    return -quad(FzFK, -50, lamb)[0]


def P(x):
    if x < -25:
        return 0
    if -25 <= x <= 25:
        return (x + 25) * convert_ton_to_N(2250) / 50
    if x > 25:
        return convert_ton_to_N(2250)

def P_non_linear(x):
    if x < -25:
        return 0
    if -25 <= x <= 25:
        print(((66.591312175022-(66.591312175022-23.408687824978006)*(x+25))+66.591312175022)*(x+25)/2)
        return ((66.591312175022-(66.591312175022-23.408687824978006)*(x+25))+66.591312175022)*(x+25)/2
    if x > 25:
        return 2250


def convert_ton_to_N(W):
    return W * 10000


def strength(lamb):
    return P(lamb) - Buoyancy(lamb) - Fk2(lamb)

def strength_non_linear(lamb):
    return P_non_linear(lamb)#-Buoyancy(lamb)#-Fk2(lamb)


def plot(lamb):
    the_x = np.linspace(-50, lamb, 100)
    the_y = []
    for x in the_x:
        the_y.append(strength_non_linear(x))
    plt.plot(the_x, the_y)
    print(the_y[25])
    plt.show()
    return


plot(50)

list_wave_length = [6161.7, 1901.76, 911.49, 533.02, 349.3, 246.47, 183.17, 141.45, 112.52,100]
for length in list_wave_length:
    wave_length = length
    wave_number = 2 * np.pi / wave_length
    wave_freq = (10 * wave_number) ** 0.5
    wave_per = 2 * np.pi / wave_freq
    the_x = np.linspace(-50, 50, 100)
    the_y = []
    the_y2 = []
    the_x2 = np.linspace(-50, 50)
    for x in the_x:
        the_y.append(convert_N_to_ton(strength(x)))
    plt.plot(the_x, the_y, label=str(wave_length))
    plt.legend()
    for x2 in the_x2:
        the_y2.append(convert_N_to_ton(Fk2(x2)))
    fig = plt.figure()
    plt.plot(the_x2, the_y2)
    fig.show()

plt.show()
# plot(50)
