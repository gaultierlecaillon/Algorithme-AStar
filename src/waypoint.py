from path_validator import PathValidator


class Waypoint(object):
    """Class to represent the position and orientation of Mary Anne.

    Note about orientation. Orientation is an integer between 0 and 3 inclusive.
        0 maps to the unit vector (0, 1)
        1 maps to the unit vector (1, 0)
        2 maps to the unit vector (0, -1)
        3 maps to the unit vector (-1, 0)
    An easy way to think about the orientation is that 0 is North, 1 is East, 2 is South, and 3 is West.
    """

    def __init__(self, x, y, orientation, parent=None):
        self._x = x
        self._y = y
        self._orientation = orientation

        self.parent = parent
        self.H = 0  # The heuristic, estimated distance from the current waypoint to the end waypoint.
        self.G = 0  # The distance between the current waypoint and the start waypoint.
        self.cost = 0  # total cost of the waypoint.

    def generate_children(self, grid):
        """ Return all childrens from a waypoint

        The time complexity of this function is O(n) with n=8

        @param grid: A 2D narray of True/False values to represent the field and obstacles
        @return: children: List of all childrens
        """
        children = []
        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]:
            wp_position = (self.x + new_position[0], self.y + new_position[1])

            # Create new waypoint
            new_wp = Waypoint(
                wp_position[0],
                wp_position[1],
                PathValidator.new_orientation(self, new_position),
                self
            )

            # Make sure within range and no obstacle
            if not PathValidator.is_valid_waypoint(new_wp, grid):
                continue

            # Make sure valid path
            if not PathValidator.is_valid_transition(self, new_wp):
                continue

            # Append
            children.append(new_wp)

        return children

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def orientation(self):
        return self._orientation

    @property
    def tuple(self):
        return tuple((self._x, self._y, self._orientation))

    def __eq__(self, other):
        return self._x == other.x and self._y == other.y and self._orientation == other.orientation

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        return 'Waypoint(%s, %s, %s)' % (self._x, self._y, self._orientation)

    def __repr__(self):
        return str(self)

    def __hash__(self):
        return hash((self._x, self._y, self._orientation))
