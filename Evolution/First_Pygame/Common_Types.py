from collections import namedtuple

Point = namedtuple('Point', ['x', 'y'])
Color = namedtuple('Color', ['red', 'green', 'blue'])
Size = namedtuple('Size', ['width', 'height'])
PointSize = namedtuple('PointSize', ['x', 'y', 'width', 'height'])
Corners = namedtuple('Corners', ['top_left', 'top_right',
                                 'bottom_right', 'bottom_left'])
Limits = namedtuple('Limits', ['x_min', 'y_min', 'x_max', 'y_max'])
Direction = namedtuple('Direction', ['dx', 'dy'])
Font = namedtuple('Font', ['letter', 'size'])
KeyValue = namedtuple('KeyValue', ['key', 'value'])
