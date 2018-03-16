import unittest as ut
from test_util.pointCloudVisualizer import MockModel
import time
from ooscad.sphereEq import get_sphere_coordinates
import math as m

#todo: this is clearly not basic.
class TestBasic(ut.TestCase):
    def testShelly(self):
        moc = MockModel()
        #note: you can use a fourier transform to get at any shape.
        # Just use an array of sin(a*theta)*sin(b*phi)/a*b*pi+...
        coords, ids = get_sphere_coordinates(
            "theta<3.14159?"
            "fmax(theta*phi, 1):"
            "fmax(1.0,3.14159*1.5*pow(sin(2*theta),2)*pow(sin(2*phi),2))",
            phi_inc=m.pi / (2.0 ** 10),
            theta_inc=m.pi / (2.0 ** 5),
            phi_start=0.0,
            phi_end=m.pi,
            theta_start=0,
            theta_end=2 * m.pi,
        )

        moc.batch_points(coords)
        moc.batch_vertices(ids)
        moc.show_cloud()


