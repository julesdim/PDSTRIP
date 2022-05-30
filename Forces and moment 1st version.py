import matplotlib.pyplot as plt
import csv


def graph_file_for_one_wave(filename, wave_frequency, wave_length, wave_angle, wave_speed, text):
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
        if line_formatted[0] == "wave" and line_formatted[1] == "length":
            try:
                example_wave_length = float(line_formatted[2])
            except:
                example_wave_length = 100000
        if line_formatted[0] == "wave" and line_formatted[1] == "angle":
            example_wave_angle = float(line_formatted[2])
        if line_formatted[0] == "speed":
            example_wave_speed = float(line_formatted[1])
        if line_formatted[0] == "Number":
            number_of_section = float(line_formatted[3])
        if example_wave_length == wave_length and example_wave_angle == wave_angle and \
                example_wave_frequency == wave_frequency and example_wave_speed == wave_speed:
            if line_formatted[0] == "Force":
                x_coordinate = float(line_formatted[1])
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
    print(forces_along_x)
    print(forces_along_y)
    print(forces_along_z)
    print(moment_along_x)
    print(moment_along_y)
    print(moment_along_z)
    all_graph = [forces_along_x, forces_along_y, forces_along_z, moment_along_x, moment_along_y, moment_along_z]
    list_title = ["x", "y", "z"]
    n_all_graph = len(all_graph)
    for i in range(n_all_graph):
        plt.plot(list_x_coordinates, all_graph[i])
        if i <= 2:
            plt.title("Forces along " + list_title[i] + " axis" + " " + text)
        if i > 2:
            plt.title("Moment along " + list_title[i - 3] + " axis" + " " + text)
        plt.show()
    return


graph_file_for_one_wave("pdstrip.out.ok", 0.1, 6161.7, 0, 0, "real")
