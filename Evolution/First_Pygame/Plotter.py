import matplotlib.pyplot as pyplot
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.cm as cm
import matplotlib.animation
from typing import List
import pandas

import Constants


class Plotter:
    def __init__(self, file_direction: str, values_to_plot: List[str]):
        self.__file_direction = file_direction
        self.__values_to_plot = values_to_plot
        self.__day = 0
        self.__data = []
        self.__characters = []
        self.__average_data = []
        self.__parse_data_from_file()

    def plot(self):
        average_generation = [x[1] for x in self.__average_data]
        average_hunger = [x[2] for x in self.__average_data]
        average_sensing = [x[3] for x in self.__average_data]
        average_speed = [x[4] for x in self.__average_data]
        average_movement = [x[5] for x in self.__average_data]
        pyplot.plot(range(self.__day),
                    average_generation, 'b',
                    label='average_generation')

        pyplot.plot(range(self.__day),
                    average_hunger, 'g',
                    label='average_hunger')

        pyplot.plot(range(self.__day),
                    average_sensing, 'r',
                    label='average_sensing')

        pyplot.plot(range(self.__day),
                    average_speed, 'k',
                    label='average_speed')

        pyplot.plot(range(self.__day),
                    average_movement, 'y',
                    label='average_movement')
        pyplot.show()

    def __update_graph(self, day: int):
        data = self.__df[self.__df['day'] == day+1]
        self.__graph._offsets3d = (data.sensing, data.speed,
                                   data.movement)
        self.__title.set_text('3D Test, day={}'.format(day+1))
        self.__finished = day+1 == self.__day
        if self.__finished:
            self.__graph.remove()
            colors = cm.rainbow(np.linspace(0, 1, len(self.__characters)))
            for d in range(self.__day):
                data = self.__df[self.__df['day'] == d]
                self.__graph = self.ax.scatter(data.sensing, data.speed,
                                               data.movement,
                                               color=colors[d])

    def plot_3d(self):
        self.fig: pyplot.Figure = pyplot.figure()
        self.ax: pyplot.Axes = self.fig.add_subplot(111, projection='3d')
        data = self.__df[self.__df['day'] == 1]
        self.__graph = self.ax.scatter(data.sensing, data.speed,
                                       data.movement)
        self.__title = self.ax.set_title('3D Test')
        self.ax.set_xlabel('Sensing')
        self.ax.set_ylabel('Speed')
        self.ax.set_zlabel('Movement')
        self.ax.set_xlim([Constants.MIN_SENSING, Constants.MAX_SENSING])
        self.ax.set_ylim([Constants.MIN_SPEED, Constants.MAX_SPEED])
        self.ax.set_zlim([Constants.MIN_MOVEMENTS, Constants.MAX_MOVEMENTS])

        ani = matplotlib.animation.FuncAnimation(self.fig, self.__update_graph,
                                                 len(self.__characters),
                                                 interval=50, blit=False,
                                                 repeat=False)
        pyplot.show()

    def __parse_data_from_file(self):
        file = open(self.__file_direction, 'r')
        lines = file.readlines()
        for line in lines:
            self.__handle_line(line)
        self.__get_averages()
        day = [x[0] for x in self.__data]
        generation = [x[1] for x in self.__data]
        hunger = [x[2] for x in self.__data]
        sensing = [x[3] for x in self.__data]
        speed = [x[4] for x in self.__data]
        movement = [x[5] for x in self.__data]
        self.__df = pandas.DataFrame({"day": day, "generation": generation,
                                      "hunger": hunger, "sensing": sensing,
                                      "speed": speed, "movement": movement})

    def __handle_line(self, line: str):
        line = line.split(' ')
        if line[0] == Constants.CHARACTERS:
            self.__characters.append(int(line[1]))
            self.__day += 1
        elif line[0] == Constants.GENERATION:
            temp = []
            temp.append(self.__day)
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
