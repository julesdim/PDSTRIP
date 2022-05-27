import csv
import masses as truc
import shape as shape
import frames as fr
import loading as ld


def correction(x, midship):
    return x - midship


def calculation_coord(filename):
    """The Pias file of coordinates is the input, and it returns a list of the coordinates as tuple
    [(x1,y1,z1),(...),...]"""
    file = open(filename, "r", encoding="utf-8")
    the_lines = csv.reader(file)
    line_counter = 0
    line_deb_frame = 0
    line_end = 1000
    beg_frame = True  # we can know if we are at the beginning of the frame to get the x coordinate of the frame
    form = shape.Form()  # initialisation of the list of coordinates
    for line in the_lines:
        new = line[0].strip().split()  # formating the line
        if line_counter == 0:
            nb_f_tot = float(new[0])  # to know the number of frame
        if line_counter != 0 and len(new) == 1 and beg_frame:
            x = (float(new[0]))  # if there is just one coordinate, it is the position along x axis, if beg_frame==True
            line_deb_frame = line_counter
            frame_act = fr.Frames(x)
            beg_frame = False  # As we just passed the beg of the frame, next is false
        if line_counter != 0 and len(new) == 3:
            y = (float(new[0]))
            z = (-float(new[1]))
            frame_act.__append__((y, z))  # we append to the list
            beg_frame = True  # the next time len(new)==1 it will be the beginning of a new frame
        if len(new) == 1 and line_counter == line_deb_frame + 1:
            nb_points = int(new[0])
            line_end = line_counter + nb_points
        if line_counter == line_end:
            form.__append__(frame_act)
        line_counter += 1
    file.close()
    return form


def mass_list(masses):
    """the input is a csv file with all the masses with the beginning of the mass along the x axis and the ending of
    this mass there is the center of gravity of this mass, the turning radius and finally the position of the centyer
    of gravity along z axis from the Free surface, it returns the sames informations but with a list of that masses """
    fichier = open(masses, "rt")
    list_of_masses = ld.Loading()  # initialisation of the list of masses
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
        mb_per_meter, me_per_meter = m / (xe - xb), m / (xe - xb)
        if m != 0:
            mass = truc.Mass(m, xb, xe, xg, yr, z, mb_per_meter, me_per_meter)
            if xg != (xb + xe) / 2:
                mass.calcul_xg_not_the_mid()
            list_of_masses.__append__(mass)
    return list_of_masses


def PD_strip_info_from_aft_to_for_mid_frame(masses, coord, Lpp):
    """The inputs are the masses, the loading of the ship as a csv file, explained in the function
    calcul_center_of_gravity, the second input is a coordinate file, with the Pias format. It returns a csv file with
    all the information needed for a PD strip input file for a bending moment and shear forces computation """
    all_coord = calculation_coord(coord)  # list of the coordinates
    all_coord = all_coord.conversion_coordinate_to_pdstrip(Lpp / 2)
    all_coord = all_coord.correction_of_coordinates()
    all_coord.plotting()
    weightloading = mass_list(masses)  # list of the masses
    weightloading.pdstrip_coordinates(Lpp / 2)
    weightloading.plot_loading(-Lpp / 2, Lpp / 2)
    f = open("data_pdstrip.csv", "w")  # writing of the info in the file "data_pdstrip.csv"
    # for every section we have the backward and the forward
    for i in range(len(all_coord.shape) - 1):
        back = (all_coord.shape[i].x + all_coord.shape[i + 1].x) / 2
        forw = correction(Lpp, Lpp / 2)
        m = weightloading.mass_calculation(back, forw)
        try:
            xg, yg, zg = weightloading.calcul_center_of_gravity(back, forw)
        except ZeroDivisionError:
            xg, yg, zg = all_coord.center_of_gravity_no_mass(back, forw)
        rx2, ry2, rz2, xy, yz, xz = all_coord.calcul_all(back, forw, xg, yg, zg)
        data = [m, xg, yg, zg, rx2, ry2, rz2, xy, yz, xz]
        for inf in data:
            # we write every input for the section
            f.write(str(inf) + " ")
        f.write("\n")
    f.close()
    # total mass is checked
    return


masses1 = "masses1.csv"
shape1 = "barge_standaard_pias_text_file.txt"
masses2 = "masses.csv"
shape2 = "correct_frames_of_oural.asc"
PD_strip_info_from_aft_to_for_mid_frame(masses2, shape2, 135)
