import matplotlib.pyplot as pyplot


class Plotter:
    def __init__(self, file_direction: str, values_to_plot: List[str]):
        self.__file_direction = file_direction
        self.__values_to_plot = values_to_plot

    def plot(self):
        pass

    def __parse_data(self):
        file = open(self.__file_direction, 'r')
        lines = file.readlines()
        print lines[0]
        # for i in range(len(lines)):
