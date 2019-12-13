import matplotlib.pyplot as pyplot
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.cm as cm
import matplotlib.animation
import matplotlib.gridspec as gridspec
from typing import List, Tuple
import pandas

import Constants


class Plotter:
    def __init__(self, file_direction: str, values_to_plot: List[str]):
        self.__file_direction = file_direction
        self.__tags = values_to_plot
        self.__max_day, self.__characters, self.__data, self.__data_av = \
            self.__parse_data_from_file(self.__file_direction, self.__tags)
        self.__3d_fig, self.__3d_ax, self.__3d_title = \
            self.__prepare_3d_graph(values_to_plot[3:],
                                    Constants.PARAMS_LIMITS)

    # Plots all the 2d graphs each on its own scale.
    def plot_2d(self):
        days = self.__data_av[self.__tags[0]]

        fig = pyplot.figure()
        fig.suptitle('Average values per day')
        gs = gridspec.GridSpec(2, 3)

        column = 0
        row = 0
        colors = cm.rainbow(np.linspace(0, 1, len(self.__tags)))
        for tag in self.__tags:
            if tag == Constants.DAYS:
                continue
            ax = fig.add_subplot(gs[row % 2, column % 3])
            self.__plot_2d((days, self.__data_av[tag]),
                           (self.__tags[0], tag), colors[row+column], ax)
            column += 1
            row = row + 1 if column == 3 else row
        ax = fig.add_subplot(gs[row % 2, column % 3])
        self.__plot_2d((days, self.__characters),
                       (self.__tags[0], 'Characters'), colors[-1], ax)

        mng = pyplot.get_current_fig_manager()
        mng.window.state('zoomed')
        pyplot.show()

    # Scatters the data on a 3d grid.
    # It first plots them per day, showing the progression of evolution, and
    # afterwards it plots all of them with a color code per day.
    def plot_3d(self):
        data = self.__data[self.__data[self.__tags[0]] == 1]
        self.__graph = self.__3d_ax.scatter(data.Sensing, data.Speed,
                                            data.Aggression)

        ani = matplotlib.animation.FuncAnimation(self.__3d_fig,
                                                 self.__update_graph,
                                                 self.__max_day,
                                                 interval=50, blit=False,
                                                 repeat=False)
        pyplot.show()

    def __plot_2d(self,
                  data: Tuple[List[int], List[float]],
                  tags: Tuple[str, str],
                  color: cm.ScalarMappable,
                  ax: pyplot.Axes):
        ax.set_xlabel(tags[0])
        ax.set_ylabel(tags[1])
        ax.plot(data[0], data[1], color=color)
        pass

    # Function that updates the graph throughout the animation.

    def __update_graph(self, day: int):
        data = self.__data[self.__data[self.__tags[0]] == day+1]
        self.__graph._offsets3d = (data.Sensing, data.Speed,
                                   data.Aggression)
        self.__3d_title.set_text('Narutal Selection Sim, day={}'.format(day+1))
        if day+1 == self.__max_day:
            self.__graph.remove()
            self.__scatter_all_3d()

    # Scatters all the 3d points with the color code per day.
    def __scatter_all_3d(self):
        colors = cm.rainbow(np.linspace(0, 1, self.__max_day))
        for d in range(self.__max_day):
            data = self.__data[self.__data[self.__tags[0]] == d]
            self.__graph = self.__3d_ax.scatter(data.Sensing, data.Speed,
                                                data.Aggression,
                                                color=colors[d])

    # Prepares the 3d graph with the labels and limits introduced.
    # It returns the Figure, its Axes and the Title of the graph.
    def __prepare_3d_graph(self,
                           labels: Tuple[str, str, str],
                           limits: Tuple[Tuple[int, int],
                                         Tuple[int, int],
                                         Tuple[int, int]]) -> \
        Tuple[pyplot.Figure,
              pyplot.Axes,
              matplotlib.text.Text]:
        fig = pyplot.figure()
        ax = fig.add_subplot(111, projection='3d')
        title = ax.set_title('3D Test')
        ax.set_xlabel(labels[0])
        ax.set_ylabel(labels[1])
        ax.set_zlabel(labels[2])
        ax.set_xlim(limits[0])
        ax.set_ylim(limits[1])
        ax.set_zlim(limits[2])
        ax.view_init(elev=46, azim=-57)
        return fig, ax, title
        pass

    # Parses the data from the file and returns:
    # Max number of days of simulation.
    # A List of amount of characters per day.
    # A pandas.DataFrame of the data per character.
    # A pandas.DataGrame of the average data per day.
    def __parse_data_from_file(self,
                               file_dir: str,
                               tags: str) -> Tuple[int,
                                                   List[int],
                                                   pandas.DataFrame,
                                                   pandas.DataFrame]:
        max_day, characters, raw_data = self.__handle_file(file_dir)
        raw_average_data = self.__get_averages(characters, raw_data)
        data = self.__parse_to_panda(raw_data, tags)
        data_av = self.__parse_to_panda(raw_average_data, tags)
        return max_day, characters, data, data_av

    # Transforms the data List into a pandas.DataFrame object with the
    # corresponding tags.
    def __parse_to_panda(self, data: List[List[float]],
                         tags: List[str]) -> pandas.DataFrame:
        temp = {}
        for i in range(len(tags)):
            t = [x[i] for x in data]
            temp[tags[i]] = t

        return pandas.DataFrame(temp)

    # Opens the file_dir given as argument and returns a Tuple containing the
    # total amount of days, a List of the size of the days transcurred
    # with the number of characters and a List with the raw data of
    # each character
    def __handle_file(self,
                      file_dir: str) -> Tuple[int, List[int], List[List[int]]]:
        file = open(file_dir, 'r')
        lines = file.readlines()
        days = 0
        characters = []
        data = []
        for line in lines:
            days = self.__handle_line(line, days, characters, data)
        return days, characters, data

    # Parses the input Line, and appends the data to the arguments lists and
    #   returns the number of days transcurred.
    # So far the implementation does the following:
    #   - If the line begins with the Characters string,
    #   it adds a new day and appends the number of characters.
    #   - If the line begins with the Generation string,
    #   it adds the new raw data row.
    def __handle_line(self, line: str, days: int,
                      characters: List[int], data: List[List[int]]) -> int:
        line = line.split(' ')
        if line[0] == Constants.CHARACTERS:
            characters.append(int(line[1]))
            days += 1
        elif line[0] == Constants.GENERATION:
            temp = []
            temp.append(days)
            for i in range(1, len(line), 2):
                temp.append(int(line[i]))
            data.append(temp)
        else:
            pass
        return days

    # Returns a matrix of average values of the raw_data divided by
    # the amount of characters per day.
    def __get_averages(self, characters: List[int],
                       raw_data: List[List[int]]) -> List[List[float]]:
        counter = 0
        average_data = []
        for number_of_characters in characters:
            averages = [0] * len(raw_data[counter])
            for i in range(number_of_characters):
                for j in range(len(averages)):
                    averages[j] += raw_data[counter + i][j]
            for i in range(len(averages)):
                averages[i] /= number_of_characters
            average_data.append(averages)
            counter += number_of_characters
        return average_data
