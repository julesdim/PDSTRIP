import matplotlib.pyplot as plt
import csv


def graph_file_for_one_wave(filename, wave_freq, wave_length, wave_angle, speed):
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
            except ValueError:
                ex_wave_length = 24646.8
        if new[0] == "wave" and new[1] == "angle":
            ex_wave_angle = float(new[2])
        if new[0] == "speed":
            ex_speed = float(new[1])
        if new[0] == "Number":
            number_of_section = float(new[3])
        if ex_wave_length == wave_length and ex_wave_angle == wave_angle and ex_wave_frequency == wave_freq and ex_speed == speed:
            if new[0] == "Force":
                x = float(new[1])
                # el_force_x = float(new[2])
                # el_force_y = float(new[5])
                el_force_z = float(new[-1])
                # forces_along_x.append(el_force_x)
                # forces_along_y.append(el_force_y)
                forces_along_z.append(el_force_z)
                if x not in les_x:
                    les_x.append(x)
            if line_counter == (number_of_section - 1):
                break
            if new[0] == "Moment":
                line_counter += 1
                # el_moment_x = float(new[1])
                try:
                    el_moment_y = float(new[-4])
                except:
                    el_moment_y = float(new[-2])
                # el_moment_z = float(new[7])
                # moment_along_x.append(el_moment_x)
                moment_along_y.append(el_moment_y)
                # moment_along_z.append(el_moment_z)
    # print(forces_along_x)
    # print(forces_along_y)
    print(forces_along_z)
    # print(moment_along_x)
    print(moment_along_y)
    # print(moment_along_z)
    plt.plot(les_x, forces_along_z)
    plt.title("Forces along Z axis")
    plt.show()
    plt.plot(les_x, moment_along_y)
    plt.title("Moment along y axis")
    plt.show()
    return


graph_file_for_one_wave("pdstrip.out.ok", 0.05, 24646.8, 135, 0)
