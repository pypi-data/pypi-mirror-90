"""Classes to map a value into a RGB color code.

"""
import pathlib
import re
from matplotlib.colors import Normalize
from matplotlib.cm import ScalarMappable

from svgwrite.container import Defs
from svgwrite.path import Path
from svgwrite.pattern import Pattern
from svgwrite.shapes import Rect


class Stripe(Defs):
    """A stripe pattern used in an SVG image.

    This class is modified from
    https://philiprogers.com/svgpatterns/#thinstripes.

    Note:
        Use as "url(#stripe)" in an SVG image.

    TODO:
        I don't remember how to load this pattern into an SVG file now. This is
        not used in the current version anyway.

    """
    def __init__(self):
        super().__init__()
        rect = Rect(insert=(0, 0), size=(5, 5), fill='#9e9e9e')
        path = Path('M 0 5 L 5 0 Z M 6 4 L 4 6 Z M -1 1 L 1 -1 Z',
                    stroke='#888', stroke_width=1)
        pattern = Pattern(id=self.__class__.__name__.lower(),
                          patternUnits='userSpaceOnUse',
                          size=(5, 5), stroke='none')
        pattern.add(rect)
        pattern.add(path)
        self.add(pattern)


class Colors:
    """Abstract class to convert a value into a RGB color."""
    def get_color(self, value):
        raise NotImplementedError
    def __getitem__(self, value):
        return self.get_color(value)


class ContinousColors(Colors):
    """Returns a RGB color for SVG given a value from a continuous colormap.

    Given a float number between the attributes :attr:`vmin` and :attr:`vmax`,
    the color is found in a colormap between the left-most color (e.g., dark
    blue in the colormap "jet") and the right-most color (e.g., dark red in the
    colormap "jet"). To get a color:

    >>> colors = ContinousColors()
    >>> color = colors[1]

    Args:
        vmin (float): The value of the left-most color.
        vmax (float): The value of the right-most color.
        cmap (str): The name of the colormap. See colormaps in matplotlib
            tutorials for available choices.

    """
    def __init__(self, vmin=-2, vmax=2, cmap='jet'):
        norm = Normalize(vmin=vmin, vmax=vmax)
        self.cmap = ScalarMappable(norm, cmap=cmap)

    def get_color(self, value):
        """Returns the SVG RGB color given ``value``.

        Args:
            value (float): The value of the color between :attr:`vmin` and
                :attr:`vmax`.

        Returns:
            str: The RGB color used in an SVG file (e.g., "rgb(255, 255, 255)").

        """
        color = self.cmap.to_rgba(value, bytes=True)[:3]
        color = 'rgb({})'.format(', '.join([str(c) for c in color]))
        return color


class PatternContinousColors(ContinousColors):
    """Returns a color from a colormap or a stripe pattern given a value.

    If the another input number, ``switch``, is greater than the attribute
    :attr:`threshold`, a stripe pattern pattern is returned; otherwise, the same
    color conversion logic as in :class:`ContinousColors` is used.

    Args:
        threshold (float): Returns a stripe pattern when the value is smaller
            than this number.

    """
    def __init__(self, vmin=-2, vmax=2, cmap='jet', threshold=0.5):
        super().__init__(vmin, vmax, cmap)
        self.threshold = threshold

    def get_color(self, value, switch):
        """Returns the color or a stripe pattern.

        Args:
            value (float): The value of the color between :attr:`vmin` and
                :attr:`vmax'.
            switch (float): If ``switch`` is greater than :attr:`threshold`, a
                stripe pattern is returned.

        Returns:
            str: The RGB color or the stripe pattern.

        """
        if switch <= self.threshold:
            return super().get_color(value)
        else:
            return 'url(#stripe)'

    def __getitem__(self, value):
        raise NotImplementedError


class DiscreteColors(Colors):
    """Returns discrete colors loaded from a .txt file given a value.

    The .txt file should use the ITK-SNAP format. An example:

    .. code-block:: text

        ################################################
        # ITK-SnAP Label Description File
        # File format:
        # IDX   -R-  -G-  -B-  -A--  VIS MSH  LABEL
        # Fields:
        #    IDX:   Zero-based index
        #    -R-:   Red color component (0..255)
        #    -G-:   Green color component (0..255)
        #    -B-:   Blue color component (0..255)
        #    -A-:   Label transparency (0.00 .. 1.00)
        #    VIS:   Label visibility (0 or 1)
        #    IDX:   Label mesh visibility (0 or 1)
        #  LABEL:   Label description
        ################################################
            0     0    0    0        0  0  0    "Clear Label"
           12   255  255  150        1  1  1    "Corpus medullare"
           33    88   95  255        1  1  1    "Left I-III"
           36    53   55  143        1  1  1    "Right I-III"

    The # lines are ignored during the loading. Only the lines with colors are
    needed. Only the IDX, R, G, and B columns are used.

    Or simply:
    
    .. code-block:: text
        
         0     0    0    0
         1   255  255  150
        -1    88   95  255

    Any number of spaces can be used to separate these numbers. The IDX column
    should be integers (0, positive, or negative).

    To get a color:

    >>> colors = DiscreteColors()
    >>> color = colors[1]

    Args:
        filename (str): The filename of the colors. If it is ``None`` or  does
            not exist, default colors are used.

    Attributes:
        colors (dict): The loaded colors. The dict key is the color value, and
            the dict value is the corresponding RGB color.

    """
    def __init__(self, filename=None):
        if filename is None or not pathlib.Path(filename).exists():
            self.colors = { 0: (255, 255, 255),
                            1: (255, 225, 25),
                            2: (245, 130, 49),
                            3: (230, 25, 75),
                           -1: (66, 212, 244),
                           -2: (67, 99, 216),
                           -3: (70, 153, 144)} 
        else:
            with open(filename) as colors_file:
                lines = colors_file.readlines()
            self.colors = dict()
            for line in lines:
                if not line.strip().startswith('#'):
                    line = tuple(int(l) for l in line.strip().split()[:4])
                    self.colors[line[0]] = line[1:]
                else:
                    continue

    def get_color(self, value):
        """Returns the SVG RGB color given ``value``.

        Args:
            value (int): The value of the color as in :attr:`colors`.

        Returns:
            str: The RGB color used in an SVG file (e.g., "rgb(255, 255, 255)").

        """
        color = self.colors[value]
        return 'rgb({})'.format(', '.join([str(c) for c in color]))


class CerebellumLabelColors(DiscreteColors):
    """A wrapper for cerebellum label colors.

    To get a color:

    >>> colors = CerebellumLabelColors()
    >>> color = colors['Vermis']

    """
    def __init__(self, filename=None):
        if filename is None:
            filename = pathlib.Path(__file__).parent.joinpath('colormap.txt')
        super().__init__(filename)
        self._mapping = NameValueMapping(filename)

    def get_color_from_name(self, name):
        """Use the region name instead of value to get the color.

        Args:
            name (str): The name of the region.

        Returns:
            str: The RGB color used in an SVG file (e.g., "rgb(255, 255, 255)").

        """
        value = self._mapping[name]
        return self.get_color(value)

    def __getitem__(self, name):
        return self.get_color_from_name(name)


class NameValueMapping:
    """Maps the name to the label value.

    Args:
        filename (str): The filename of the colormap. See
            :class:`DiscreteColors` for more details for the file format.

    """
    def __init__(self, filename):
        with open(filename) as colors_file:
            lines = colors_file.readlines()
        self._mapping = dict()
        for line in lines:
            if not line.strip().startswith('#'):
                value = int(line.strip().split()[0])
                name = re.sub(r'^.*"(.*)".*$', r'\1', line.strip())
                self._mapping[name] = value
            else:
                continue

    def __getitem__(self, name):
        """Returns the value given the name.

        Args:
            name (str): The name of the region.

        Returns:
            value (int): The value of the color for
                :class:`CerebellumLabelColors`.

        """
        return self._mapping[name]
