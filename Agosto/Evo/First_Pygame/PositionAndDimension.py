import Coordinate
import Dimensions


class PositionAndDimension:

    def __init__(self, coordinate, dimension):
        self.coordinate = coordinate
        self.dimension = dimension

    def get_position_dimensions(self):
        return self.coordinate.get_coordinate() +\
            self.dimension.get_dimension()

    def get_vertices(self):
        a = Coordinate.Coordinate(self.coordinate.x, self.coordinate.y)
        b = Coordinate.Coordinate(self.coordinate.x + self.dimension.width,
                                  self.coordinate.y)
        c = Coordinate.Coordinate(self.coordinate.x,
                                  self.coordinate.y + self.dimension.heigth)
        d = Coordinate.Coordinate(self.coordinate.x + self.dimension.width,
                                  self.coordinate.y + self.dimension.heigth)
        return (a, b, c, d)

    def get_vertex_limits(self):
        a = Coordinate.Coordinate(self.coordinate.x, self.coordinate.y)
        b = Coordinate.Coordinate(self.coordinate.x + self.dimension.width,
                                  self.coordinate.y + self.dimension.heigth)
        return (a, b)
