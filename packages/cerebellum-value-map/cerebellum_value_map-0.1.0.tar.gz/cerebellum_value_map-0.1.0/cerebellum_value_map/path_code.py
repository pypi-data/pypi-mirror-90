"""Wrapper class of path codes.

"""
class PathCode:
    """Wrapper class of an SVG path code.

    Args:
        points (tuple[tuple]): 2D points of the path code.

    """
    command = ''
    """str: The SVG command."""

    def __init__(self, *points):
        self.points = points

    def __repr__(self):
        pattern = '%s(' + ', '.join(['(%.3f, %.3f)'] * len(self.points)) + ')'
        return pattern % (self.command, *[c for p in self.points for c in p])

    def __str__(self):
        """Returns the SVG path code."""
        pattern = '%s ' + ' '.join(['%.3f, %.3f'] * len(self.points))
        return pattern % (self.command, *[c for p in self.points for c in p])

    def flip(self, axis):
        """Flips the the path code around a vertial axis.

        Args:
            axis (float): The location of the axis.

        Returns:
            PathCode: The flipped path code.

        """
        points = [(2 * axis - p[0], p[1]) for p in self.points]
        return self.__class__(*points)

    def translate(self, x, y):
        """Translate the path code by an offset of (x, y).

        Args:
            x (float): The horizontal translation.
            y (float): The vertical translation.

        Returns:
            PathCode: The translated path code.

        """
        points = [(p[0] + x, p[1] + y)  for p in self.points]
        return self.__class__(*points)

    def scale(self, f):
        """Scales the path code relative to the origin.

        Args:
            f (float): The scale factor.

        Returns:
            PathCode: The scaled path code.

        """
        points = [(p[0] * f, p[1] * f) for p in self.points]
        return self.__class__(*points)


class Move(PathCode):
    """Moves to a point.

    Example:

    >>> str(Move((10, 20)))
    M 10.000 20.000

    Args:
        points (tuple[tuple]): The target point. It should have only one 2D
            point (x, y).

    """
    command = 'M'


class Line(PathCode):
    """Draws a line.

    Example:

    >>> str(Line((10, 20)))
    L 10.000 20.000

    Args:
        points (tuple[tuple]): The stop point. It should have one 2D point
            (x_stop, y_stop).

    """
    command = 'L'


class QuadraticCurve(PathCode):
    """Draws a quadratic curve.

    Example:

    >>> str(QuadraticCurve((10, 20), (20, 30)))
    Q 10.000 20.000 20.000 30.000

    Args:
        points (tuple[tuple]): The control, and stop points. It should
            have two 2D points (x_control, y_control) and (x_stop, y_stop).

    """
    command = 'Q'


class BezierCurve(PathCode):
    """Draws a Bezier curve.

    Example:

    >>> str(BezierCurve((10, 20), (20, 30)))
    C 10.000 20.000 20.000 30.000

    Args:
        points (tuple[tuple]): The control 1, control2, and stop points.
            It should have three 2D points (x_control_1, y_control_1),
            (x_control_2, y_control_2), and (x_stop, y_stop).

    """
    command = 'C'
