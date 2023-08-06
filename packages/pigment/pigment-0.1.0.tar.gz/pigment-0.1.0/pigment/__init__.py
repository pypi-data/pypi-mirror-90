"""Python utilities for colors"""

__version__ = "0.1.0"

from colorsys import hls_to_rgb, hsv_to_rgb, rgb_to_hls, rgb_to_hsv
from math import sqrt

from .exceptions import InvalidRGBValue, WrongLengthError


def normalize_hex(hex_code: str) -> str:
    """Normalizes a hex color code

    Removes the leading ``#`` if there is one, expands 3-character hex codes,
    and lowercases the hex code

    Args:
        hex_code (:class:`str`): A hex code to normalize

    Returns:
        :class:`str`: The normalized hex code

    Raises:
        :exception:`~pigment.exceptions.WrongLengthError`: The provided hex
            code had the wrong length
    """

    hex_code = hex_code.lstrip("#").lower()

    if len(hex_code) == 3:
        hex_code = "".join(c * 2 for c in hex_code)

    if len(hex_code) != 6:
        raise WrongLengthError("hex_code")

    return hex_code


class Color:
    """Represents a color

    Args:
        red (:class:`int`): The color's red RGB component (0-255)
        green (:class:`int`): The color's green RGB component (0-255)
        blue (:class:`int`): The color's blue RGB component (0-255)

    Note:
        The :attr:`~cmyk`, :attr:`~hex_code`, :attr:`~hls`, :attr:`~hsv`, and
        :attr:`~rgb` properties can be set to update the color object.
    """

    def __init__(self, red: int, green: int, blue: int):
        self.rgb = (red, green, blue)

    @property
    def rgb(self):
        """The color as an RGB tuple

        * Red (0-255)
        * Green (0-255)
        * Blue (0-255)
        """

        return self._rgb

    @rgb.setter
    def rgb(self, value):
        if len(value) != 3:
            raise WrongLengthError()

        for c in value:
            if c not in range(256):
                raise InvalidRGBValue()

        self._rgb = value

    @property
    def hex_code(self):
        """The color's hex code"""

        return "%02x%02x%02x" % (self.rgb[0], self.rgb[1], self.rgb[2])

    @hex_code.setter
    def hex_code(self, value):
        self.rgb = (int(normalize_hex(value)[i : i + 2], 16) for i in (0, 2, 4))

    @property
    def hsv(self):
        """The color as an HSV tuple

        * Hue: color (0-360)
        * Saturation: amount of gray vs. color (0-100)
        * Value: amount of black vs. color (0-100)
        """

        res = rgb_to_hsv(
            self.rgb[0] / 255, self.rgb[1] / 255, self.rgb[2] / 255
        )

        return (
            round(res[0] * 360),
            round(res[1] * 100),
            round(res[2] * 100),
        )

    @hsv.setter
    def hsv(self, value):
        self.rgb = hsv_to_rgb(*value)

    @property
    def hls(self):
        """The color as an HLS tuple

        * Hue: color (0-360)
        * Lightness: amount of white vs. color (0-100)
        * Saturation: amount of gray vs. color (0-100)
        """

        res = rgb_to_hls(
            self.rgb[0] / 255, self.rgb[1] / 255, self.rgb[2] / 255
        )

        return (
            round(res[0] * 360),
            round(res[1] * 100),
            round(res[2] * 100),
        )

    @hls.setter
    def hls(self, value):
        self.rgb = hls_to_rgb(*value)

    @property
    def cmyk(self):
        """The color as a CMYK tuple

        * Cyan (0-100)
        * Magenta (0-100)
        * Yellow (0-100)
        * Key/Black (0-100)
        """

        if self.rgb == (0, 0, 0):
            return (0, 0, 0, 100)

        c = 1 - self.rgb[0] / 255
        m = 1 - self.rgb[1] / 255
        y = 1 - self.rgb[2] / 255

        min_cmy = min(c, m, y)
        c = (c - min_cmy) / (1 - min_cmy)
        m = (m - min_cmy) / (1 - min_cmy)
        y = (y - min_cmy) / (1 - min_cmy)
        k = min_cmy

        return (round(c * 100), round(m * 100), round(y * 100), round(k * 100))

    @cmyk.setter
    def cmyk(self, value):
        cyan, magenta, yellow, key = value

        self.rgb = (
            round(255 * (1 - cyan / 100) * (1 - key / 100)),
            round(255 * (1 - magenta / 100) * (1 - key / 100)),
            round(255 * (1 - yellow / 100) * (1 - key / 100)),
        )


def blend(color1: Color, color2: Color) -> Color:
    """Blends two colors together

    Args:
        color1 (:class:`~pigment.Color`): The first color
        color2 (:class:`~pigment.Color`): The second color

    Returns:
        :class:`~pigment.Color`
    """

    return Color(
        round(sqrt((color1[0] ** 2 + color2[0] ** 2) / 2)),
        round(sqrt((color1[1] ** 2 + color2[1] ** 2) / 2)),
        round(sqrt((color1[2] ** 2 + color2[2] ** 2) / 2)),
    )
