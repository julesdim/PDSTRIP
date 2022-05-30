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
        "im" to plot the imaginary part
        "abs" to plot the absolute value"

    :returns
    --------
    It plots 6 graphs for the wave selected and for the part selected (real, imaginary or absolute)
    """
    if text== "real":
        const=0
    elif text== "im":
        const=1
    elif text== "abs":
        const=2
    file = open(filename, "r", encoding="utf-8")
    the_lines = csv.reader(file)
    line_counter = 0
    les_x = []
    forces_along_x = []
    forces_along_y = []
    forces_along_z = []
    moment_along_x = []
    moment_along_y = []
    moment_along_z = []
    number_of_section = 0
    ex_wave_frequency = 0
    ex_wave_length = 0
    ex_wave_angle = 0
    ex_speed = 0
    for line in the_lines:
        try:
            new = line[0].strip().split()
        except IndexError:
            pass
        print(new)
        if len(new) == 0:
            new = ["error", "error", "error"]
        if new[0] == "wave" and new[2] == "frequency":
            ex_wave_frequency = float(new[3])
        if new[0] == "wave" and new[1] == "length":
            try:
                ex_wave_length = float(new[2])
            except:
                ex_wave_length = 100000
        if new[0] == "wave" and new[1] == "angle":
            ex_wave_angle = float(new[2])
        if new[0] == "speed":
            ex_speed = float(new[1])
        if new[0] == "Number":
            number_of_section = float(new[3])
        if ex_wave_length == wave_length and ex_wave_angle == wave_angle and ex_wave_frequency == wave_frequency and ex_speed == wave_speed:
            if new[0] == "Force":
                x = float(new[1])
                el_force_x = float(new[2+const])
                el_force_y = float(new[5+const])
                el_force_z = float(new[8+const])
                forces_along_x.append(el_force_x)
                forces_along_y.append(el_force_y)
                forces_along_z.append(el_force_z)
                if x not in les_x:
                    les_x.append(x)
            if line_counter == (number_of_section - 1):
                break
            if new[0] == "Moment":
                line_counter += 1
                el_moment_x = float(new[1+const])
                el_moment_y = float(new[4+const])
                el_moment_z = float(new[7+const])
                moment_along_x.append(el_moment_x)
                moment_along_y.append(el_moment_y)
                moment_along_z.append(el_moment_z)
    print(forces_along_x)
    print(forces_along_y)
    print(forces_along_z)
    print(moment_along_x)
    print(moment_along_y)
    print(moment_along_z)
    all_el = [forces_along_x, forces_along_y, forces_along_z, moment_along_x, moment_along_y, moment_along_z]
    list_title = ["x", "y", "z"]
    n_all_el = len(all_el)
    for i in range(n_all_el):
        plt.plot(les_x, all_el[i])
        if i <= 2:
            plt.title("Forces along " + list_title[i] + " axis" + " " + text)
        if i > 2:
            plt.title("Moment along " + list_title[i - 3] + " axis" + " " + text)
        plt.show()
    return


graph_file_for_one_wave("pdstrip.out.ok", 0.2, 1540.43, 0, 0,"abs")
