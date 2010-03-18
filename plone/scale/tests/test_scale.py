from cStringIO import StringIO
import os.path
from unittest import TestCase
from plone.scale.scale import scaleImage
from plone.scale.tests import TEST_DATA_LOCATION
import PIL.Image

PNG = open(os.path.join(TEST_DATA_LOCATION, "logo.png")).read()
GIF = open(os.path.join(TEST_DATA_LOCATION, "logo.gif")).read()


class ScalingTests(TestCase):
    def testNewSizeReturned(self):
        (imagedata, format, size)=scaleImage(PNG, 42, 51, "down")
        input=StringIO(imagedata)
        image=PIL.Image.open(input)
        self.assertEqual(image.size, size)

    def testScaledImageIsJpeg(self):
        self.assertEqual(scaleImage(GIF, 84, 103, "down")[1] , "JPEG")

    def XtestScaledPngImageIsPng(self):
        # This test failes because the sample input file has a format of
        # None according to PIL..
        self.assertEqual(scaleImage(PNG, 84, 103, "down")[1] , "PNG")


    def testSameSizeDownScale(self):
        self.assertEqual(scaleImage(PNG,  84, 103, "down")[2], (84, 103))

    def testHalfSizeDownScale(self):
        self.assertEqual(scaleImage(PNG,  42, 51, "down")[2], (42, 51))

    def testScaleWithCropDownScale(self):
        self.assertEqual(scaleImage(PNG,  20, 51, "down")[2], (20, 51))

    def testNoStretchingDownScale(self):
        self.assertEqual(scaleImage(PNG,  200, 103, "down")[2], (200, 103))

    def testRestrictWidthOnlyDownScale(self):
        self.assertEqual(scaleImage(PNG,  42, None, "down")[2], (42, 52))

    def testRestrictHeightOnlyDownScale(self):
        self.assertEqual(scaleImage(PNG,  None, 51, "down")[2], (42, 51))


    def testSameSizeUpScale(self):
        self.assertEqual(scaleImage(PNG,  84, 103, "up")[2], (84, 103))

    def testHalfSizeUpScale(self):
        self.assertEqual(scaleImage(PNG,  42, 51, "up")[2], (42, 51))

    def testNoStretchingUpScale(self):
        self.assertEqual(scaleImage(PNG,  200, 103, "up")[2], (84, 103))

    def testRestrictWidthOnlyUpScale(self):
        self.assertEqual(scaleImage(PNG,  42, None, "up")[2], (42, 52))

    def testRestrictHeightOnlyUpScale(self):
        self.assertEqual(scaleImage(PNG,  None, 51, "up")[2], (42, 51))

    def testNoRestrictions(self):
        self.assertRaises(ValueError, scaleImage, PNG, None, None)

    def testQuality(self):
        img1 = scaleImage(PNG, 84, 103)[0]
        img2 = scaleImage(PNG, 84, 103, quality=50)[0]
        img3 = scaleImage(PNG, 84, 103, quality=20)[0]
        self.assertNotEqual(img1, img2)
        self.assertNotEqual(img1, img3)
        self.failUnless(len(img1) > len(img2) > len(img3))

    def testResultBuffer(self):
        img1 = scaleImage(PNG, 84, 103)[0]
        result = StringIO()
        img2 = scaleImage(PNG, 84, 103, result=result)[0]
        self.assertEqual(result, img2)      # the return value _is_ the buffer
        self.assertEqual(result.getvalue(), img1)   # but with the same value


def test_suite():
    from unittest import defaultTestLoader
    return defaultTestLoader.loadTestsFromName(__name__)
