"""Classes to hold a shape.

"""
import numpy as np
from svgwrite.container import Group
from svgwrite.path import Path

from .path_code import PathCode
from .text import Value, Annotation
from .colors import DiscreteColors, CerebellumLabelColors


class Shape:
    """Abstract class to hold a shape.

    """
    @property
    def points(self):
        """Returns points (vertices) of this shape.

        Returns:
            numpy.ndarray[float]:
            The shape is num_colors x 2. Each row is a vertex of this shape.

        """
        raise NotImplementedError

    @property
    def left(self):
        """Returns the left-most horizontal coordinate."""
        return np.min(self.points[:, 0])

    @property
    def right(self):
        """Returns the right-most horizontal coordinate."""
        return np.max(self.points[:, 0])

    @property
    def bottom(self):
        """Returns the bottom-most vertical coordinate."""
        return np.max(self.points[:, 1])

    @property
    def top(self):
        """Returns the top-most vertical coordinate."""
        return np.min(self.points[:, 1])

    @property
    def h_center(self):
        """Returns the averge of :meth:`left` and :meth:`right`."""
        return (self.left + self.right) / 2

    @property
    def v_center(self):
        """Returns the averge of :meth:`bottom` and :meth:`top`."""
        return (self.top + self.bottom) / 2

    def get_svg(self, **kwargs):
        """Returns the svg code of this shape.

        Args:
            kwargs: The svg options such as ``fill``.

        """
        raise NotImplementedError

    def translate(self, x, y):
        """Translate the shape by an offset (x, y).

        Args:
            x (float): The horizontal translation.
            y (float): The vertical translation.

        Returns:
            Shape: The translated shape.

        """
        raise NotImplementedError

    def scale(self, f):
        """Scales the shape.

        Args:
            f (float): The scale factor.

        Returns:
            Shape: The scaled shape.

        """
        raise NotImplementedError


class PathShape(Shape):
    """A shape specified with path codes.

    Note:
        To convert the shape into SVG code:

        >>> str(PathShape())

    Args:
        codes (list[PathCode]): The path codes to form the shape.
        enclose (bool): If True, add a path code "Z" to enclose the shape.

    """
    def __init__(self, *codes, enclose=True):
        self.codes = list(codes)
        self.enclose = True

    def __repr__(self):
        return ',\n'.join([repr(code) for code in self.codes])

    def __str__(self):
        path_codes = [str(c) for c in self.codes]
        if self.enclose:
            path_codes.append('Z')
        return ' '.join(path_codes)

    @property
    def points(self):
        points = np.array([code.points[-1] for code in self.codes])
        return points

    def get_svg(self, **kwargs):
        path = Path([str(self)], **kwargs)
        return path

    def flip(self, axis):
        """Flips the shape around a vertical axis.

        Args:
            axis (float): The horizontal location of this vertical axis.

        Returns:
            PathShape: The flipped shape.

        """
        flipped_codes = list()
        for code in self.codes:
            flipped_codes.append(code.flip(axis))
        return self.__class__(*flipped_codes, enclose=self.enclose)

    def translate(self, x, y):
        codes = [code.translate(x, y) for code in self.codes]
        return self.__class__(*codes, enclose=self.enclose)

    def scale(self, f):
        codes = [code.scale(f) for code in self.codes]
        return self.__class__(*codes, enclose=self.enclose)


class AnnotatedShape(Shape):
    """Wraps a shape with annotation using SVG Group.

    Args:
        shape (Shape): The shape to annotate.
        value (float): The coloring value.
        colors (cerebellum_value_map.colors.Colors): Converts the value into a
            color.
        annot_txt (str): The annotation text, such as the name of this shape.
        annot_pos (str, cerebellum_value_map.text.AnnotationPosition): The
            annotation position. See
            :class:`cerebellum_value_map.text.AnnotationPosition` for available
            choices.
        show_annot (bool): Show annotation with the shape.
        show_value_txt (bool): If True, show a text of the coloring value.

    """
    def __init__(self, shape, value, colors=DiscreteColors(),
                 annot_txt='', annot_pos='right',
                 show_annot=False, show_value_txt=False):
        super().__init__()
        self.shape = shape
        self.value = value
        self.colors = colors
        self.color = colors[value]
        self.annot_txt = annot_txt
        self.annot_pos = annot_pos
        self.show_annot = show_annot
        self.show_value_txt = show_value_txt

    def get_svg(self, **kwargs):
        """Returns the svg code of this shape with annotation.

        Args:
            kwargs: The options for the group.

        Returns:
            svgwrite.container.Group: The group of the shape and annotations.

        """
        group = Group(**kwargs)
        group.add(self.shape.get_svg(fill=self.color))
        if len(self.annot_txt) > 0 and self.show_annot:
            group.add(Annotation(self.annot_txt, self.annot_pos, self.shape))
        if self.show_value_txt:
            group.add(Value(self.value, self.shape))
        return group

    @property
    def points(self):
        return self.shape.points

    def translate(self, x, y):
        shape = self.shape.translate(x, y)
        return self.__class__(shape, self.value, colors=self.colors,
                              annot_txt=self.annot_txt,
                              annot_pos=self.annot_pos,
                              show_annot=self.show_annot,
                              show_value_txt=self.show_value_txt)

    def scale(self, f):
        shape = self.shape.scale(f)
        return self.__class__(shape, self.value, colors=self.colors,
                              annot_txt=self.annot_txt,
                              annot_pos=self.annot_pos,
                              show_annot=self.show_annot,
                              show_value_txt=self.show_value_txt)
