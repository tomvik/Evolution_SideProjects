import matplotlib.pyplot as pyplot
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.cm as cm
from typing import List

import Constants


class Plotter:
    def __init__(self, file_direction: str, values_to_plot: List[str]):
        self.__file_direction = file_direction
        self.__values_to_plot = values_to_plot
        self.__data = []
        self.__characters = []
        self.__average_data = []
        self.__parse_data_from_file()

    def plot(self):
        average_generation = [x[0] for x in self.__average_data]
        average_hunger = [x[1] for x in self.__average_data]
        average_sensing = [x[2] for x in self.__average_data]
        average_speed = [x[3] for x in self.__average_data]
        average_movement = [x[4] for x in self.__average_data]
        pyplot.plot(range(len(average_generation)),
                    average_generation, 'b',
                    label='average_generation')

        pyplot.plot(range(len(average_hunger)),
                    average_hunger, 'g',
                    label='average_hunger')

        pyplot.plot(range(len(average_sensing)),
                    average_sensing, 'r',
                    label='average_sensing')

        pyplot.plot(range(len(average_speed)),
                    average_speed, 'k',
                    label='average_speed')

        pyplot.plot(range(len(average_movement)),
                    average_movement, 'y',
                    label='average_movement')
        pyplot.show()

    def plot_3d(self):
        sensing = [x[2] for x in self.__data]
        speed = [x[3] for x in self.__data]
        movement = [x[4] for x in self.__data]

        fig = pyplot.figure()
        ax = fig.add_subplot(111, projection='3d')
        colors = cm.rainbow(np.linspace(0, 1, len(self.__characters)))
        counter = 0
        i = 0
        for number_of_characters in self.__characters:
            current_sensing = sensing[counter:number_of_characters+counter]
            current_speed = speed[counter:number_of_characters+counter]
            current_movement = movement[counter:number_of_characters+counter]
            ax.scatter(current_sensing, current_speed,
                       current_movement, color=colors[i])
            i += 1
            counter += number_of_characters
        pyplot.show()

    def __parse_data_from_file(self):
        file = open(self.__file_direction, 'r')
        lines = file.readlines()
        for line in lines:
            self.__handle_line(line)
        self.__get_averages()

    def __handle_line(self, line: str):
        line = line.split(' ')
        if line[0] == Constants.CHARACTERS:
            self.__characters.append(int(line[1]))
        elif line[0] == Constants.GENERATION:
            temp = []
            for i in range(1, len(line), 2):
                temp.append(int(line[i]))
            self.__data.append(temp)
        else:
            pass

    def __get_averages(self):
        counter = 0
        for number_of_characters in self.__characters:
            averages = [0] * len(self.__data[counter])
            for i in range(number_of_characters):
                for j in range(len(averages)):
                    averages[j] += self.__data[counter + i][j]
            for i in range(len(averages)):
                averages[i] /= number_of_characters
            self.__average_data.append(averages)
            counter += number_of_characters
