import Coordinate
import Dimensions

class StartAndDimension:

	def __init__(self, coordinate, dimension):
		self.coordinate = coordinate
		self.dimension = dimension

	def get_position_dimensions(self):
		return self.coordinate.get_coordinate()  + self.dimension.get_dimension()