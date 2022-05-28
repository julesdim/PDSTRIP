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
    start_line_of_the_frame = 0
    end_line_of_the_frame = 1000
    boolean_for_beginning_of_the_frame = True  # we can know if we are at the beginning of the frame to get the x coordinate of the frame
    form_of_the_ship = shape.Form()  # initialisation of the list of coordinates
    for line in the_lines:
        line_formatted = line[0].strip().split()  # formating the line
        if line_counter == 0:
            total_number_of_frame = float(line_formatted[0])  # to know the number of frame
        if line_counter != 0 and len(line_formatted) == 1 and boolean_for_beginning_of_the_frame:
            x_coordinate = (float(line_formatted[
                                      0]))  # if there is just one coordinate, it is the position along x axis, if beg_frame==True
            start_line_of_the_frame = line_counter
            current_frame = fr.Frames(x_coordinate)
            boolean_for_beginning_of_the_frame = False  # As we just passed the beg of the frame, next is false
        if line_counter != 0 and len(line_formatted) == 3:
            y_coordinate = (float(line_formatted[0]))
            z_coordinate = (-float(line_formatted[1]))
            current_frame.__append__((y_coordinate, z_coordinate))  # we append to the list
            if y_coordinate != 0:
                current_frame.__append__((-y_coordinate, z_coordinate))
            boolean_for_beginning_of_the_frame = True  # the next time len(new)==1 it will be the beginning of a new frame
        if len(line_formatted) == 1 and line_counter == start_line_of_the_frame + 1:
            number_points_of_the_current_frame = int(line_formatted[0])
            end_line_of_the_frame = line_counter + number_points_of_the_current_frame
        if line_counter == end_line_of_the_frame:
            form_of_the_ship.__append__(current_frame)
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
    file = open(filename, "rt")
    weight_loading = ld.Loading()  # initialisation of the list of masses
    the_lines = file.readlines()
    total_mass = 0  # to check the total mass
    for line in the_lines:
        line_formatted = line.strip("\n").split(
            ";")  # we stop the line to the \n and we cut the information where there is a ";"
        current_weight = float(line_formatted[0])  # the first info is the object mass
        total_mass += current_weight
        x_beginning = float(line_formatted[1])  # the second is the beginning
        x_end = float(line_formatted[2])  # the end
        x_coordinate_CoG = float(line_formatted[3])  # the exact center of gravity
        y_coordinate_CoG = float(line_formatted[4])  # the turning radius
        z_coordinate_CoG = float(line_formatted[5])  # the position along z axis of the center of gravity
        linear_density_x_beginning, linear_density_x_end = current_weight / (x_end - x_beginning), current_weight / (
                x_end - x_beginning)
        if current_weight != 0:
            current_mass = mass.Mass(current_weight, x_beginning, x_end, x_coordinate_CoG, y_coordinate_CoG,
                                     z_coordinate_CoG, linear_density_x_beginning, linear_density_x_end)
            if x_coordinate_CoG != (x_beginning + x_end) / 2:
                current_mass.calcul_xg_not_the_mid()
            weight_loading.__append__(current_mass)
    return weight_loading


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
    hull_form = collection_of_coordinates(coordinates_filename)  # list of the coordinates
    hull_form = hull_form.conversion_coordinate_to_pdstrip(Lpp / 2)
    hull_form = hull_form.correction_of_coordinates()
    hull_form.checking()
    hull_form.plot_one_frame(0)
    hull_form.plotting()
    weight_loading = collection_of_mass(masses_filename)  # list of the masses
    weight_loading.pdstrip_coordinates(Lpp / 2)
    weight_loading.plot_loading(-Lpp / 2, Lpp / 2)
    file = open("data_pdstrip.csv", "w")  # writing of the info in the file "data_pdstrip.csv"
    # for every section we have the backward and the forward
    for i in range(len(hull_form.shape) - 1):
        back_section = (hull_form.shape[i].x + hull_form.shape[i + 1].x) / 2
        front_section = conversion_for_pdstrip_xaxis(Lpp, Lpp / 2)
        weight_o_the_current_part = weight_loading.mass_calculation(back_section, front_section)
        try:
            x_coordinate_CoG, y_coordinate_CoG, z_coordinate_CoG = \
                weight_loading.calcul_center_of_gravity(back_section, front_section)
        except ZeroDivisionError:
            x_coordinate_CoG, y_coordinate_CoG, z_coordinate_CoG = \
                hull_form.center_of_gravity_no_mass(back_section, front_section)
        radius_of_inertia_x_square, radius_of_inertia_y_square, radius_of_inertia_z_square, xy, yz, xz = \
            hull_form.calcul_all(back_section, front_section, x_coordinate_CoG, y_coordinate_CoG, z_coordinate_CoG)
        data = [weight_o_the_current_part, x_coordinate_CoG, y_coordinate_CoG, \
                z_coordinate_CoG, radius_of_inertia_x_square, radius_of_inertia_y_square, radius_of_inertia_z_square,\
                xy, yz, xz]
        for input_value in data:
            # we write every input for the section
            file.write(str(input_value) + " ")
        file.write("\n")
    file.close()  # total mass is checked
    return


masses1 = "masses1.csv"
shape1 = "barge_standaard_pias_text_file.txt"
masses2 = "masses.csv"
shape2 = "correct_frames_of_oural.asc"
Writing_of_the_PDstrip_input_file(masses2, shape2, 135)
