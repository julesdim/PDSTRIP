import csv
import masses as mass
import shape as shape
import frames as fr
import loading as ld


def conversion_for_pdstrip_xaxis(x, midship):
    """That functions converts a x coordinate with an origin at the PPAR into a coordinate with an origin at
     middle ship
     :parameter
     ----------
     x: a float
        the coordinate to convert
     midship: a float
        the localisation of midship from the PPAR, corresponds to Lpp/2
    :returns
    x: the coordinates from the middle ship
     """
    return x - midship


def collection_of_coordinates(filename):
    """That functions read a Pias file of coordinates, and it reads every coordinate to return a shape object
    :parameter
    filename: a text variable corresponding to the pias file of coordinates
    :returns
    form: A Form object corresponding to a list of frame, defined by a x coordinate and coordinates of point for that
    frame
    """
    file = open(filename, "r", encoding="utf-8")
    the_lines = csv.reader(file)
    line_counter = 0
    line_of_the_frame_beginning = 0
    line_of_the_frame_ending = 1000
    boolean_for_beginning_of_the_frame = True  # we can know if we are at the beginning of the frame to get the x coordinate of the frame
    form_of_the_ship = shape.Form()  # initialisation of the list of coordinates
    for line in the_lines:
        new = line[0].strip().split()  # formating the line
        if line_counter == 0:
            nb_f_tot = float(new[0])  # to know the number of frame
        if line_counter != 0 and len(new) == 1 and boolean_for_beginning_of_the_frame:
            x = (float(new[0]))  # if there is just one coordinate, it is the position along x axis, if beg_frame==True
            line_of_the_frame_beginning = line_counter
            frame_act = fr.Frames(x)
            boolean_for_beginning_of_the_frame = False  # As we just passed the beg of the frame, next is false
        if line_counter != 0 and len(new) == 3:
            y = (float(new[0]))
            z = (-float(new[1]))
            frame_act.__append__((y, z))  # we append to the list
            if y != 0:
                frame_act.__append__((-y, z))
            boolean_for_beginning_of_the_frame = True  # the next time len(new)==1 it will be the beginning of a new frame
        if len(new) == 1 and line_counter == line_of_the_frame_beginning + 1:
            nb_points = int(new[0])
            line_of_the_frame_ending = line_counter + nb_points
        if line_counter == line_of_the_frame_ending:
            form_of_the_ship.__append__(frame_act)
        line_counter += 1
    file.close()
    return form_of_the_ship


def collection_of_mass(filename):
    """That functions reads a csv file and collects all the information, the mass in ton, the beginning of the mass,
    the end of the mass, the center of gravity with x coordinate, y and z, then it defines the mass per meter at the
    beginning of the mass repartition and the mass per meter at the end of the mass repartition (along the x axis), the
    code uses the localisation of the center of gravity to compute that values.
    :parameter
    filename: a csv file
        every line are : x coordinate of the beginning, x coordinate of the end, x coordinate of the center of gravity
        y coordinate of CoG, z coordinate of the CoG
    :returns
    list_of_masses: a loading file
        it is a list of mass, defined by the information mentioned above but with mass per
        meter computed at the beginning and at the end
     """
    fichier = open(filename, "rt")
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
            masse = mass.Mass(m, xb, xe, xg, yr, z, mb_per_meter, me_per_meter)
            if xg != (xb + xe) / 2:
                masse.calcul_xg_not_the_mid()
            list_of_masses.__append__(masse)
    return list_of_masses


def Writing_of_the_PDstrip_input_file(masses_filename, coordinates_filename, Lpp):
    """That function writes a file titled data_pdstrip.csv with all the input data from the frames that needs the
    PDstrip program, that function needs the loading informations, the shape of the ship, and the length between
    perpendiculars.
    :parameter
    masses_filename: a text variable
        it corresponds to a csv file
        every line are : x coordinate of the beginning, x coordinate of the end, x coordinate of the center of gravity
        y coordinate of CoG, z coordinate of the CoG
    coordinates_filename:a text variable
        it corresponds to the pias file of coordinates
    Lpp: a number
        it is the length between perpendiculars
    :returns
    nothing, it writes a file with the data needed """
    all_coord = collection_of_coordinates(coordinates_filename)  # list of the coordinates
    all_coord = all_coord.conversion_coordinate_to_pdstrip(Lpp / 2)
    all_coord = all_coord.correction_of_coordinates()
    all_coord.checking()
    all_coord.plot_one_frame(0)
    all_coord.plotting()
    weightloading = collection_of_mass(masses_filename)  # list of the masses
    weightloading.pdstrip_coordinates(Lpp / 2)
    weightloading.plot_loading(-Lpp / 2, Lpp / 2)
    f = open("data_pdstrip.csv", "w")  # writing of the info in the file "data_pdstrip.csv"
    # for every section we have the backward and the forward
    for i in range(len(all_coord.shape) - 1):
        back = (all_coord.shape[i].x + all_coord.shape[i + 1].x) / 2
        forw = conversion_for_pdstrip_xaxis(Lpp, Lpp / 2)
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
    f.close()  # total mass is checked
    return


masses1 = "masses1.csv"
shape1 = "barge_standaard_pias_text_file.txt"
masses2 = "masses.csv"
shape2 = "correct_frames_of_oural.asc"
Writing_of_the_PDstrip_input_file(masses2, shape2, 135)
