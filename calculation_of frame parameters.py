import csv
from io import StringIO
import numpy as np
import matplotlib.pyplot as plt

Lpp = 100


def conversion_coordinate_to_pdstrip(coord, midship_section):
    """ coord in meter is a tuple (x,y,z)
    The pd strip theory uses the coordinates in the midship sections,
    this function returns the x coordinate with the origine between the perpendiculars"""
    return (coord[0] - midship_section, coord[1], coord[2])


def calculation_coord(filename):
    """The Pias file of coordinates is the input, and it returns a list of the coordinates as tuple
    [(x1,y1,z1),(...),...]"""
    file = open(filename, "r", encoding="utf-8")
    the_lines = csv.reader(file)
    line_counter = 0
    beg_frame = True  # we can know if we are at the beginning of the frame to get the x coordinate of the frame
    x = 0  # initialisation of coordinates
    y = 0
    z = 0
    coord = []  # initialisation of the list of coordinates
    for line in the_lines:
        new = line[0].strip().split()  # formating the line
        # print(new)
        if line_counter == 0:
            nb_f_tot = float(new[0])  # to know the number of frame
        if line_counter != 0 and len(new) == 1 and beg_frame:
            x = (float(new[0]))  # if there is just one coordinate, it is the position along x axis, if beg_frame==True
            beg_frame = False  # As we just passed the beg of the frame, next is false
        if line_counter != 0 and len(new) == 3:
            y = (float(new[0]))
            z = (float(new[1]))
            coord_act = (x, y, z)  # we get the coordinates of the actual point
            coord.append((x, y, z))  # we append to the list
            beg_frame = True  # the next time len(new)==1 it will be the beginning of a new frame
        line_counter += 1
    file.close()
    return coord


def calcul_rx2(coord, yg, zg):
    """inputs are a list of coord and yg zg coordinates of the center of gravity
    it returns the square of the inertial radius along x axis, by an average of (y-yg)**2+(z-zg)**2"""
    sum = 0  # initialization of the sum
    for i in range(len(coord)):
        y = coord[i][1]  # we get the coord
        z = coord[i][2]
        sum += (y - yg) ** 2 + (z - zg) ** 2  # we add the value for the actual point
    for i in range(len(coord)):
        # we do the same thing for the mirror points
        y = -coord[i][1]
        z = coord[i][2]
        sum += (y - yg) ** 2 + (z - zg) ** 2
    # we return an average
    return sum / 2 * len(coord)


def calcul_ry2(coord, xg, zg):
    """inputs are a list of coord and xg zg coordinates of the center of gravity
        it returns the square of the inertial radius along y axis, by an average of (x-xg)**2+(z-zg)**2"""
    sum = 0  # initialisation of the sum
    for i in range(len(coord)):
        # we get the coordinates
        x = coord[i][0]
        z = coord[i][2]
        # we add the value to the sum
        sum += (x - xg) ** 2 + (z - zg) ** 2
    # we calculate the average
    # not necessary to calculate the mirror point because the coordinates are the same, it will not change the final value
    return sum / len(coord)


def calcul_rz2(coord, xg, yg):
    """inputs are a list of coord and xg yg coordinates of the center of gravity
        it returns the square of the inertial radius along z axis, by an average of (x-xg)**2+(y-yg)**2"""
    sum = 0  # initialization of the sum
    for i in range(len(coord)):
        # we get the coordinates
        x = coord[i][0]
        y = coord[i][1]
        # we add the value for the actual point
        sum += (x - xg) ** 2 + (y - yg) ** 2
    # we do the same thing for the mirror points
    for i in range(len(coord)):
        x = coord[i][0]
        y = -coord[i][1]
        sum += (x - xg) ** 2 + (y - yg) ** 27
    # we return the average
    return sum / 2 * len(coord)


def calcul_xy(coord, xg, yg):
    """inputs are a list of coord and xg yg coordinates of the center of gravity
        it returns the mass weighted average of (x-xg)(y-yg)"""
    sum = 0  # initialization of the sum
    for i in range(len(coord)):
        # we get the x coordinate
        x = coord[i][0]
        y = coord[i][1]
        # we add the value to the sum
        sum += (x - xg) * (y - yg)
    # same thing for the mirror points along y axis
    for i in range(len(coord)):
        x = coord[i][0]
        y = -coord[i][1]
        sum += (x - xg) * (y - yg)
    # we return the average
    return sum / 2 * len(coord)


def calcul_yz(coord, yg, zg):
    """inputs are a list of coord and xg yg coordinates of the center of gravity
            it returns the mass weighted average of (y-yg)(z-zg)"""
    sum = 0  # initialization of the sum
    for i in range(len(coord)):
        # we get the coordinates
        z = coord[i][2]
        y = coord[i][1]
        # we add the value into the sum
        sum += (z - zg) * (y - yg)
    # same thing for the mirror points
    for i in range(len(coord)):
        z = coord[i][2]
        y = -coord[i][1]
        sum += (z - zg) * (y - yg)
    # we return the average
    return sum / 2 * len(coord)


def calcul_xz(coord, xg, zg):
    """inputs are a list of coord and xg yg coordinates of the center of gravity
            it returns the mass weighted average of (x-xg)(z-zg)"""
    sum = 0  # initialization of the sum
    for i in range(len(coord)):
        # we get the coordinates
        z = coord[i][2]
        x = coord[i][0]
        # we add the value to the sum
        sum += (z - zg) * (x - xg)
    # we return the average
    return sum / len(coord)


def mass_list(masses):
    """the input is a csv file with all the masses with the beginning of the mass along the x axis and the ending of this mass
    there is the center of gravity of this mass, the turning radius and finally the position of the centyer of gravity along
    z axis from the Free surface, it returns the sames informations but with a list of that masses """
    fichier = open(masses, "rt")
    list_of_masses = []  # initialisation of the list of masses
    the_lines = fichier.readlines()
    total_mass = 0  # to check the total mass
    for line in the_lines:
        line = line.strip("\n").split(";")  # we stop the line to the \n and we cut the information where there is a ";"
        m = float(line[0])  # the first info is the object mass
        total_mass += m
        xb = float(line[1])  # the second is the beginning
        xe = float(line[2])  # the end
        xg = float(line[3])  # the exact center of gravity
        yr = float(line[4])  # the turning radius
        z = float(line[5])  # the position along z axis of the center of gravity
        list_of_masses.append((m, xb, xe, xg, yr, z))  # we append the current value
    print(total_mass, "tm")
    return list_of_masses


def mass_calculation(masses_list, xb, xe):
    """The inputs are the list of the masses in the ship, and the beginning of the frame where we want to calculate the center
    of gravity, along the x axis, xb and xe.
    It returns the total mass in that section"""
    n = len(masses_list)
    tm = 0
    for i in range(n):
        m = masses_list[i][0]
        xbm = masses_list[i][1]  # beginning of the mass
        xem = masses_list[i][2]  # end of the mass
        if xbm < xe and xem > xb:
            rb = np.max([xb, xbm])  # real beginning of the mass for the section
            re = np.min([xe,
                         xem])  # real end of the mass for the section, if the end of the mass is after the end of the section
            tm += m * (re - rb) / (xem - xbm)
            # print(m*(re-rb)/(xem-xbm))
    return tm


def calcul_center_of_gravity(list_masses, xb, xe):
    """"calculation of the center of gravity for a section, with a list of masses as input
     warning the origine is the Pias origin of the report, a conversion is needed
     if we want to use the coordinates relative to the midship, for the PD Strip Theory.
     It returns the coordinates of the center of gravity as a tuple (xg,yg,zg)
     It supposes the mass is distributed linearly"""
    tm = mass_calculation(list_masses, xb, xe)
    n = len(list_masses)
    # initialization of the values
    xg = 0
    zg = 0
    for i in range(n):
        m = list_masses[i][0]
        xbm = list_masses[i][1]  # beginning of the mass
        xem = list_masses[i][2]  # end of the mass
        if xbm < xe and xem > xb:
            rb = np.max([xb, xbm])  # real beginning of the mass, if the mass begins before the frame
            re = np.min([xe, xem])  # same for the end
            rm = m * (re - rb) / (xem - xbm)  # proportion of the mass situated between the section
            xg += rm * (re + rb) / 2
            zg += rm * list_masses[i][5]
            # print(masses[i][5])
    xg = xg / tm
    zg = zg / tm
    return (xg, 0, zg)


def PD_strip_info_from_aft_to_for_mid_frame(masses, coord):
    """The inputs are the masses, the loading of the ship as a csv file, explained in the function calcul_center_of_gravity,
    the second input is a coordinate file, with the Pias format.
    It returns a csv file with all the information needed for a PD strip input file for a bending moment and shear forces
    computation"""
    all_coord = calculation_coord(coord)  # list of the coordinates
    mass = mass_list(masses)  # list of the masses
    list_x = []  # initialization of the x coordinates of the sections
    f = open("data_pdstrip.csv", "w")  # writing of the info in the file "data_pdstrip.csv"
    for coord in all_coord:
        if coord[0] not in list_x:
            list_x.append(coord[0])  # we append just one time every x coordinates of the frames
    list_x.sort()  # we sort the info
    print(list_x)
    n_x = len(list_x)
    # for every section we have the backward and the forward
    for i in range(n_x - 1):
        if i == 0:
             back = list_x[0]
             # forward middle of the section
             forw = (list_x[0] + list_x[1]) / 2
        #elif i == n_x - 2:
        #     forw = list_x[-1]
             # backward the middle of the section
        #     back = (list_x[-1] + list_x[-2]) / 2
        else:
             # forward and backward are the middle of the offset frames
            forw = (list_x[i + 1]+list_x[i])/2
            back = (list_x[i]+list_x[i-1])/2
        list_coord = []  # initialization of the list of coordinates
        for coord in all_coord:
            # we append the coordinates situated in the section
            if back <= coord[0] <= forw:
                list_coord.append(coord)
        # calculation of every information needed by PD strip code
        m = mass_calculation(mass, back, forw)
        xg, yg, zg = calcul_center_of_gravity(mass, back, forw)
        xg, yg, zg = conversion_coordinate_to_pdstrip((xg, yg, zg), Lpp / 2)
        rx2 = calcul_rx2(list_coord, yg, zg)
        ry2 = calcul_ry2(list_coord, xg, zg)
        rz2 = calcul_rz2(list_coord, xg, yg)
        xy = calcul_xy(list_coord, xg, yg)
        yz = calcul_yz(list_coord, yg, zg)
        xz = calcul_xz(list_coord, xg, zg)
        # mass is divided by 1000 because PD strip unity is the ton instead of kg
        data = [m / 1000, xg, yg, zg, rx2, ry2, rz2, xy, yz, xz]
        for inf in data:
            # we write every input for the section
            f.write(str(inf) + " ")
        f.write("\n")
    f.close()
    # total mass is checked
    return


coord = calculation_coord("frame_try.asc")
zg = 3.372587
yg = 0
xg = 90.01621
rx2 = calcul_rx2(coord, yg, zg)
ry2 = calcul_ry2(coord, xg, zg)
rz2 = calcul_rz2(coord, xg, yg)
xy = calcul_xy(coord, xg, yg)
yz = calcul_yz(coord, yg, zg)
xz = calcul_xz(coord, xg, zg)
PD_strip_info_from_aft_to_for_mid_frame("masses1.csv", "barge_standaard_pias_text_file.txt")
