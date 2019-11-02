from Rectangle import Rectangle
from Common_Types import Color, PointSize


class Food(Rectangle):
    def __init__(self, id: int, rectangle: PointSize,
                 color: Color, background_color: Color,
                 nutritional_value: int):
        super().__init__(rectangle, color, background_color)
        self._id = id
        self._nutritional_value = nutritional_value

    # Returns the id.
    def get_id(self) -> int:
        return self._id

    # Returns the nutritional value.
    def get_nutritional_value(self) -> int:
        return self._nutritional_value
