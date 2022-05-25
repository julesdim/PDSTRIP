import csv
import matplotlib.pyplot as plt
import essai as xgcalc
import masses as truc
import shape as shape
import numpy as np
import frames as fr
import loading as ld
Lpp = 100
essai=ld.Loading()
mass=truc.Mass(1,2,3,4,5,6,7,8)
essai.__append__(mass)

def correction(x,midship):
    return x-midship

def calculation_coord(filename):
    """The Pias file of coordinates is the input, and it returns a list of the coordinates as tuple
    [(x1,y1,z1),(...),...]"""
    file = open(filename, "r", encoding="utf-8")
    the_lines = csv.reader(file)
    line_counter = 0
    line_deb_frame=0
    line_end=1000
    beg_frame = True  # we can know if we are at the beginning of the frame to get the x coordinate of the frame
    x = 0  # initialisation of coordinates
    y = 0
    z = 0
    les_z = []
    form = shape.Form()  # initialisation of the list of coordinates
    for line in the_lines:
        new = line[0].strip().split()  # formating the line
        # print(new)
        if line_counter == 0:
            nb_f_tot = float(new[0])  # to know the number of frame
        if line_counter != 0 and len(new) == 1 and beg_frame:
            x = (float(new[0]))# if there is just one coordinate, it is the position along x axis, if beg_frame==True
            line_deb_frame=line_counter
            frame_act=fr.Frames(x)
            beg_frame = False  # As we just passed the beg of the frame, next is false
        if line_counter != 0 and len(new) == 3:
            y = (float(new[0]))
            z = (float(new[1]))
            frame_act.__append__((y,z))
            les_z.append(z)
            coord_act = (x, y, z)  # we get the coordinates of the actual point
              # we append to the list
            beg_frame = True  # the next time len(new)==1 it will be the beginning of a new frame
        if len(new)==1 and line_counter==line_deb_frame+1:
            nb_points=int(new[0])
            line_end=line_counter+nb_points
        if line_counter==line_end:
            form.__append__(frame_act)
        line_counter += 1
    file.close()
    return form

def mass_list(masses):
    """the input is a csv file with all the masses with the beginning of the mass along the x axis and the ending of this mass
    there is the center of gravity of this mass, the turning radius and finally the position of the centyer of gravity along
    z axis from the Free surface, it returns the sames informations but with a list of that masses """
    fichier = open(masses, "rt")
    list_of_masses = ld.Loading()  # initialisation of the list of masses
    the_lines = fichier.readlines()
    total_mass = 0  # to check the total mass
    for line in the_lines:
        line = line.strip("\n").split(";")  # we stop the line to the \n and we cut the information where there is a ";"
        m = float(line[0]) / 1000  # the first info is the object mass
        total_mass += m
        xb = float(line[1])  # the second is the beginning
        xe = float(line[2])  # the end
        xg = float(line[3])  # the exact center of gravity
        yr = float(line[4])  # the turning radius
        z = float(line[5])  # the position along z axis of the center of gravity
        if xg != (xb - xe) / 2:
            mb_per_meter, me_per_meter = xgcalc.calcul_xg_not_the_mid(m, xb, xe, xg, 0.00001)
        else:
            me_per_meter = m / (xb - xe)
            mb_per_meter = me_per_meter
        mass = truc.Mass(m, xb, xe, xg, yr, z, mb_per_meter, me_per_meter)
        list_of_masses.__append__(mass)  # we append the current value
    return list_of_masses

def mass_calculation(masses_list, xb, xe):
    """The inputs are the list of the masses in the ship, and the beginning of the frame where we want to calculate the center
    of gravity, along the x-axis, xb and xe.
    It returns the total mass in that section"""
    n = len(masses_list.masses)
    tm = 0
    for i in range(n):
        m = masses_list[i].mass
        xbm = masses_list[i].xb  # beginning of the mass
        xem = masses_list[i].xe  # end of the mass
        xgm = masses_list[i].xg
        mb = masses_list[i].mb_per_meter
        me = masses_list[i].me_per_meter
        if xbm < xe and xem > xb:
            rb = np.max([xb, xbm])  # real beginning of the mass for the section
            re = np.min([xe, xem])
            mbr = mb + (rb - xbm) * (mb - me) / (xbm - xem)
            mer = mb + (re - xbm) * (mb - me) / (xbm - xem)
            if xgm != (xbm - xem) / 2:
                tm += (re - rb) * (mbr + mer) / 2
            if xgm == (xbm - xem) / 2:
                # real end of the mass for the section, if the end of the mass is after the end of the section
                tm += (re - rb) * (mbr + mer) / 2
    return tm

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

def PD_strip_info_from_aft_to_for_mid_frame(masses, coord):
    """The inputs are the masses, the loading of the ship as a csv file, explained in the function calcul_center_of_gravity,
    the second input is a coordinate file, with the Pias format.
    It returns a csv file with all the information needed for a PD strip input file for a bending moment and shear forces
    computation"""
    all_coord = calculation_coord(coord)  # list of the coordinates
    all_coord = all_coord.conversion_coordinate_to_pdstrip(Lpp/2)
    all_coord = all_coord.correction_of_coordinates()
    #print_section(all_coord, 8.5)
    weightloading = mass_list(masses)  # list of the masses
    #graph_loading(weightloading, 0, 100)
    f = open("data_pdstrip.csv", "w")  # writing of the info in the file "data_pdstrip.csv"
    list_x = all_coord.x_coordinates()
    print(list_x)
    list_x.sort()  # we sort the info, maybe not already sorted
    print(list_x)
    n_x = len(list_x)
    # for every section we have the backward and the forward
    for i in range (len(all_coord.shape)-1):
        back = (all_coord.shape[i].x+all_coord.shape[i+1].x)/2
        print(back,"back")
        forw=Lpp
        list_coord=[]
        # for frame in all_coord.shape:
        #     if back<= frame.x<=forw:
        #         list_coord.append(coord)
        # # calculation of every information needed by PD strip code
        m = weightloading.mass_calculation(back,forw)
        print(m)
        xg,yg,zg=weightloading.calcul_center_of_gravity(back,forw)
        xg=correction(xg,Lpp/2)
        print(xg,yg,zg)
        rx2,ry2,rz2,xy,yz,xz = all_coord.calcul_all(back,forw,xg,yg,zg)
        data = [m, xg, yg, zg, rx2, ry2, rz2, xy, yz, xz]
        for inf in data:
            # we write every input for the section
            f.write(str(inf) + " ")
        f.write("\n")
    f.close()
    # total mass is checked
    return

PD_strip_info_from_aft_to_for_mid_frame("masses1.csv", "barge_standaard_pias_text_file.txt")
