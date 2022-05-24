import csv
from io import StringIO
import numpy as np
import matplotlib.pyplot as plt

Lpp = 135


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
    les_z = []
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
            les_z.append(z)
            coord_act = (x, y, z)  # we get the coordinates of the actual point
            coord.append((x, y, z))  # we append to the list
            beg_frame = True  # the next time len(new)==1 it will be the beginning of a new frame
        line_counter += 1
    file.close()
    print(les_z)
    return coord


def correction_of_coordinates(list_coord):
    """Because the PIAS file does not create the coordinates of the top of the frame,
    with that function for each point not at the max y or max z, it creates a point with the same y, same x but at the top,
    like this it corrects the zG I think"""
    x_coord = []  # list of frames coordinates
    list_coord_fr = []  # for one frame we save the coord of the point
    z_fr = []  # all the z of the frame
    y_fr = []  # all the y of the frame
    for coord2 in list_coord:
        if coord2[0] not in x_coord:
            x_coord.append(coord2[0])  # we create the list of frame
    for x_fr in x_coord:
        for coord2 in list_coord:
            if coord2[0] == x_fr:
                # for one frame, at x_fr
                list_coord_fr.append(coord2)  # list of the coordinates for that frame
                z_fr.append(coord2[2])  # same for the z
                y_fr.append(coord2[1])  # same for the y
        max_z = max(z_fr)  # we save the max of z
        max_y = max(y_fr)  # we save the max of y
        for coord2 in list_coord_fr:
            if coord2[2] < max_z and coord2[1] < max_y:
                list_coord.append(
                    (coord2[0], coord2[1], max_z))  # we append a point at the same coordinates but at max_z
    return list_coord


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
        sum += (x - xg) ** 2 + (y - yg) ** 2
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


def graph_loading(list_mass, x_min, x_max):
    """That function allow the user to print the weightloading, for a list of mass, and with the
    boundaries of the ship"""
    delt_x = 0.1  # value of the strip to calculate the ship loading
    les_x = np.arange(x_min, x_max + delt_x, delt_x)  # coordinates of each strip
    n = len(les_x)
    mass_per_m = [0]  # we initialize the weight loading for x=0, it's equal to 0
    for i in range(n - 1):
        x_inf = les_x[i]
        x_up = les_x[i + 1]
        # coordinates of the strip i
        el_mass = mass_calculation(list_mass, x_inf, x_up) / delt_x  # element of mass for the strip
        mass_per_m.append(el_mass)  # we add to the list
    plt.plot(les_x, mass_per_m)
    plt.title("weight loading")
    plt.show()
    return


def mass_calculation(masses_list, xb, xe):
    """The inputs are the list of the masses in the ship, and the beginning of the frame where we want to calculate the center
    of gravity, along the x-axis, xb and xe.
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
            if xb == 55 and xe == 55.1:
                # print(m,"m")
                # print(rb,"rb")
                # print(re,"re")
                # print(xbm,"xb")
                # print(xem,"xe")
                print(m)
                print(m * (re - rb) / (xem - xbm), "mass act")
                print(re - rb)
                print(tm)
            # print(m,"m")
            # print(rb,"rb")
            # print(re,"re")
            # print(xbm,"xb")
            # print(xem,"xe")
            # print(tm)
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
    yg = 0
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
            yg += rm * list_masses[i][4]
            zg += rm * list_masses[i][5]
            # print(masses[i][5])
    try:
        xg = xg / tm
        yg = yg / tm
        zg = zg / tm
    except ZeroDivisionError:
        the_coord = calculation_coord("barge_standaard_pias_text_file.txt")
        the_coord = correction_of_coordinates(the_coord)
        sum = 0
        sum_z = 0
        y = 0
        z = 0
        the_x = []
        for coord in the_coord:
            if coord[0] <= xe and coord[0] >= xb:
                if coord[0] not in the_x:
                    the_x.append(coord[0])
                y += coord[1]
                z += coord[2]
                sum += 1
                sum_z += 1
        sum_z += len(the_x)  # pour prendre en compte le bas du bateau
        xg = (xb + xe) / 2
        yg = y / sum
        zg = z / sum_z
    return (xg, yg, zg)


def print_section(list_coord, x):
    z_coord = []
    y_coord = []
    print("actif")
    for coord in list_coord:
        if coord[0] == x:
            z_coord.append(coord[2])
            y_coord.append(coord[1])
    plt.plot(y_coord, z_coord, "ob")
    plt.show()
    return


def PD_strip_info_from_aft_to_for_mid_frame(masses, coord):
    """The inputs are the masses, the loading of the ship as a csv file, explained in the function calcul_center_of_gravity,
    the second input is a coordinate file, with the Pias format.
    It returns a csv file with all the information needed for a PD strip input file for a bending moment and shear forces
    computation"""
    all_coord = calculation_coord(coord)  # list of the coordinates
    all_coord = correction_of_coordinates(all_coord)
    print_section(all_coord, 8.5)
    mass = mass_list(masses)  # list of the masses
    graph_loading(mass, 0, 135)
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
        # if i == 0:
        #    back = list_x[0]
        #    #forward middle of the section
        #    forw = (list_x[0] + list_x[1]) / 2
        # #elif i == n_x - 2:
        # #     forw = list_x[-1]
        #      # backward the middle of the section
        # #     back = (list_x[-1] + list_x[-2]) / 2
        # else:
        #     # forward and backward are the middle of the offset frames
        #     forw = (list_x[i + 1]+list_x[i])/2
        #     back = (list_x[i]+list_x[i-1])/2
        back = (list_x[i] + list_x[i + 1]) / 2
        forw = Lpp
        # print(i)
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
        data = [m, xg, yg, zg, rx2, ry2, rz2, xy, yz, xz]
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
PD_strip_info_from_aft_to_for_mid_frame("masses_North_4layers_98.csv", "correct_frames_of_oural.asc")
