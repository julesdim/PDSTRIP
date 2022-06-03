import matplotlib.pyplot as plt
import csv
import numpy as np


def graph_file_for_one_wave(filename: str, wave_length: float, wave_angle: float,
                            wave_speed: float, text: str, boolean_print, bool_initialisation, text_fonction):
    """That function plots 6 different graphs. The 3 firsts are the forces along each axis, the value printed depends on
     the text, it can be the real part the imaginary or the absolute value

    :argument
    ---------
    filename: a text object
        that's the name of the pdstrip results file
    wave_frequency: a float
        that's the value of the frequency of the wave that we want to print the results
    wave_length: a float
        that's the value of the length of the wave that we want to print the results
    wave_angle: a float
        that's the value of the angle of the wave that we want to print the results
    wave_speed: a float
        that's the value of the speed of the wave that we want to print the results
    text: a text object
        3 possibilities, "real" to plot the real part
        "imaginary" to plot the imaginary part
        "absolute" to plot the absolute value"

    :returns
    --------
    It plots 6 graphs for the wave selected and for the part selected (real, imaginary or absolute)
    """
    if text == "real":
        constant = 0
    elif text == "imaginary":
        constant = 1
    elif text == "absolute":
        constant = 2
    file = open(filename, "r", encoding="utf-8")
    file_writed = open("data_results.csv", "w")
    the_lines = csv.reader(file)
    line_counter = 0
    list_x_coordinates = []
    forces_along_x = []
    forces_along_y = []
    forces_along_z = []
    moment_along_x = []
    moment_along_y = []
    moment_along_z = []
    number_of_section = 0
    example_wave_frequency = 0
    example_wave_length = 0
    example_wave_angle = 0
    example_wave_speed = 0
    for line in the_lines:
        try:
            line_formatted = line[0].strip().split()
        except IndexError:
            pass
        if len(line_formatted) == 0:
            line_formatted = ["error", "error", "error"]
        if line_formatted[0] == "wave" and line_formatted[2] == "frequency":
            example_wave_frequency = float(line_formatted[3])
            print(example_wave_frequency)
        if line_formatted[0] == "wave" and line_formatted[1] == "length":
            try:
                example_wave_length = float(line_formatted[2])
                #if example_wave_length == wave_length:
                    #print(example_wave_frequency)
            except:
                example_wave_length = 100000
        if line_formatted[0] == "wave" and line_formatted[1] == "angle":
            example_wave_angle = float(line_formatted[2])
        if line_formatted[0] == "speed":
            example_wave_speed = float(line_formatted[1])
        if line_formatted[0] == "Number":
            number_of_section = float(line_formatted[3])
        if example_wave_length == wave_length and example_wave_angle == wave_angle and example_wave_speed == wave_speed:
            if line_formatted[0] == "Force":
                x_coordinate = float(line_formatted[1]) + 100 / 2
                element_force_x = float(line_formatted[2 + constant])
                element_force_y = float(line_formatted[5 + constant])
                element_force_z = float(line_formatted[8 + constant])
                forces_along_x.append(element_force_x)
                forces_along_y.append(element_force_y)
                forces_along_z.append(element_force_z)
                if x_coordinate not in list_x_coordinates:
                    list_x_coordinates.append(x_coordinate)
            if line_counter == (number_of_section - 1):
                break
            if line_formatted[0] == "Moment":
                line_counter += 1
                element_moment_x = float(line_formatted[1 + constant])
                element_moment_y = float(line_formatted[4 + constant])
                element_moment_z = float(line_formatted[7 + constant])
                moment_along_x.append(element_moment_x)
                moment_along_y.append(element_moment_y)
                moment_along_z.append(element_moment_z)
    # list_x_coordinates=np.array(list_x_coordinates)
    # forces_along_z=np.array(forces_along_z)
    # moment_along_y=np.array(moment_along_y)
    # forces_along_z=(140-list_x_coordinates)*forces_along_z
    # print(100-list_x_coordinates,"les x")
    # moment_along_y=(115-list_x_coordinates)*moment_along_y
    # print(forces_along_x)
    # print(forces_along_y)
    # print(forces_along_z)
    # print(moment_along_x)
    # print(moment_along_y)
    # print(moment_along_z)
    all_graph = [forces_along_z, moment_along_y]
    list_title = ["x", "y", "z"]
    n_all_graph = len(all_graph)
    for i in range(len(list_x_coordinates)):
        file_writed.write(str(list_x_coordinates[i]) + " ")
        for graph in all_graph:
            file_writed.write(str(graph[i]) + " ")
        file_writed.write("\n")
    if bool_initialisation:
        fig = plt.figure()
        subplot1 = fig.add_subplot(1, 2, 1)
        subplot2 = fig.add_subplot(1, 2, 2)
        global list_subplot
        list_subplot = [subplot1, subplot2]
    if text_fonction=="speed":
        legend=str(wave_speed)
    if text_fonction=="wave length":
        legend=str(wave_length)
    for i in range(n_all_graph):
        list_subplot[i].plot(list_x_coordinates, all_graph[i], label=legend)
        plt.grid()
        if i == 0:
            list_subplot[i].set_title("Forces along z axis")
            list_subplot[i].legend()
        if i == 1:
            list_subplot[i].set_title("Bending moment")
            list_subplot[i].legend()
    if boolean_print:
        plt.show()
    return


def graph_many_wave_length(filename, first_wave_length, last_wave_length, speed, angle, text):
    list_wave_length = []
    bool_initialisation = True
    file = open(filename, "r", encoding="utf-8")
    the_lines = csv.reader(file)
    boolean_print = False
    example_wave_length = 0
    text_fonction="wave length"
    for line in the_lines:
        try:
            line_formatted = line[0].strip().split()
        except IndexError:
            pass
        if len(line_formatted) == 0:
            line_formatted = ["error", "error", "error"]
        if line_formatted[0] == "wave" and line_formatted[1] == "length":
            example_wave_length = float(line_formatted[2])
        if first_wave_length < example_wave_length < last_wave_length and example_wave_length not in list_wave_length:
            list_wave_length.append(example_wave_length)
    if len(list_wave_length) == 0:
        return
    for i in range(len(list_wave_length)):
        wave_length = list_wave_length[i]
        if i == 1:
            bool_initialisation = False
        if i == len(list_wave_length) - 1:
            boolean_print = True
        graph_file_for_one_wave(filename, wave_length, angle, speed, text, boolean_print, bool_initialisation, text_fonction)
    return

def graph_many_speed(filename, first_speed, last_speed, wave_length, angle, text):
    list_speed = []
    bool_initialisation = True
    file = open(filename, "r", encoding="utf-8")
    the_lines = csv.reader(file)
    boolean_print = False
    example_wave_length = 0
    text_fonction="speed"
    for line in the_lines:
        try:
            line_formatted = line[0].strip().split()
        except IndexError:
            pass
        if len(line_formatted) == 0:
            line_formatted = ["error", "error", "error"]
        if line_formatted[0] == "speed":
            example_wave_speed = float(line_formatted[1])
            if first_speed <= example_wave_speed <= last_speed and example_wave_speed not in list_speed:
                list_speed.append(example_wave_speed)
    if len(list_speed) == 0:
        return
    for i in range(len(list_speed)):
        speed = list_speed[i]
        if i == len(list_speed) - 1:
            boolean_print = True
        graph_file_for_one_wave(filename, wave_length, angle, speed, text, boolean_print, bool_initialisation, text_fonction)
        bool_initialisation = False
    return

#graph_file_for_one_wave("pdstrip.out.ok", 183.17, 0, 0, "real", True, True, "speed")
graph_many_wave_length("pdstrip.out.ok", 100, 800, 0, 0, "real")
graph_many_speed("pdstrip.out.ok",0,10,1540.43,0,"real")