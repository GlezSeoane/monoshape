# -*- coding: utf-8 -*-


"""monoshape unit test suite"""

import unittest
from unittest import TestCase

from PIL import Image
from PIL import ImageChops

from monoshape.__main__ import extract_shape

__author__ = 'Borja González Seoane'
__copyright__ = 'Copyright 2019, Borja González Seoane'
__credits__ = 'Borja González Seoane'
__license__ = 'LICENSE'
__version__ = '1.2'
__maintainer__ = 'Borja González Seoane'
__email__ = 'garaje@glezseoane.es'
__status__ = 'Production'


class UnitTestSuite(TestCase):
    """Unit test container class for monoshape library."""

    @staticmethod
    def are_equals(img1, img2):
        """Determine if two images are equals in contents."""
        return ImageChops.difference(img1, img2).getbbox() is None

    def test_simple_draw(self):
        source = 'test_src/original_pear.png'

        drawn = extract_shape(path=source,
                              black_background=False,
                              white_shape=False,
                              rgb_shape=False,
                              red=None,
                              green=None,
                              blue=None)

        expected = Image.open(source.replace('original', 'expected'))

        self.assertTrue(self.are_equals(drawn, expected))

    def test_draw_with_white_output(self):
        source = 'test_src/original_plane.png'

        drawn = extract_shape(path=source,
                              black_background=False,
                              white_shape=True,
                              rgb_shape=False,
                              red=None,
                              green=None,
                              blue=None)

        expected = Image.open(source.replace('original', 'expected'))

        self.assertTrue(self.are_equals(drawn, expected))

    def test_draw_with_rgb_output(self):
        source = 'test_src/original_udc.png'

        drawn = extract_shape(path=source,
                              black_background=False,
                              white_shape=False,
                              rgb_shape=True,
                              red=159,
                              green=36,
                              blue=110)

        expected = Image.open(source.replace('original', 'expected'))

        self.assertTrue(self.are_equals(drawn, expected))

    def test_draw_with_black_background(self):
        source = 'test_src/original_spaceship.png'

        drawn = extract_shape(path=source,
                              black_background=True,
                              white_shape=False,
                              rgb_shape=False,
                              red=None,
                              green=None,
                              blue=None)

        expected = Image.open(source.replace('original', 'expected'))

        self.assertTrue(self.are_equals(drawn, expected))


if __name__ == '__main__':
    unittest.main()
