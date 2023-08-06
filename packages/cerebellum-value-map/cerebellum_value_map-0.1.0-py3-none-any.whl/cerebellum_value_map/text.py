"""Wrapper classes to create text in an SVG image.

"""
from enum import Enum
from svgwrite.text import Text


class AnnotationPosition(str, Enum):
    """Enum of the annotation positions.

    To show available choices:

    >>> print(list(AnnotationPosition))

    """
    RIGHT = 'right'
    LEFT = 'left'
    TOP = 'top'
    BOTTOM = 'bottom'


class Annotation(Text):
    """Creates an annotation for the shape.

    Args:
        text (str): The annotation text to show.
        position (str): The position of the annotation, such as "left",
            "right", and "bottom".
        shape (cerebellum_value_map.shape.PathShape): The shape to annotate.

    """
    def __init__(self, text, position, shape):
        self.shape = shape
        super().__init__(text, **self._create_prop(position), stroke='none')

    def _create_prop(self, position):
        """Returns the property of the annotation."""
        position = AnnotationPosition(position)
        if position == AnnotationPosition.RIGHT:
            prop = self._put_right()
        elif position == AnnotationPosition.LEFT:
            prop = self._put_left()
        elif position == AnnotationPosition.TOP:
            prop = self._put_top()
        elif position == AnnotationPosition.BOTTOM:
            prop = self._put_bottom()
        return prop

    def _put_right(self):
        return dict(x=[self.shape.right],
                    y=[self.shape.v_center],
                    text_anchor='start',
                    alignment_baseline='middle')

    def _put_left(self):
        return dict(x=[self.shape.right],
                    y=[self.shape.v_center],
                    text_anchor='end',
                    alignment_baseline='middle')

    def _put_top(self):
        return dict(x=[self.shape.h_center],
                    y=[self.shape.top],
                    text_anchor='middle',
                    alignment_baseline='baseline')

    def _put_bottom(self):
        return dict(x=[self.shape.h_center],
                    y=[self.shape.bottom],
                    text_anchor='middle',
                    alignment_baseline='hanging')


class Value(Text):
    """Creates the text of the color value.

    Args:
        value (float): The value of the color to show on top of the shape.
        shape (cerebellum_value_map.shape.PathShape): The shape to annotate.

    """
    def __init__(self, value, shape):
        super().__init__(str(value), stroke='none',
                         x=[shape.h_center], y=[shape.v_center],
                         alignment_baseline='middle', text_anchor='middle')
