import unittest as ut
from test_util.pointCloudVisualizer import MockModel
import time
from ooscad.sphereEq import get_sphere_coordinates

class TestBasic(ut.TestCase):
    def testSphere(self):
        moc = MockModel()
        coords, ids = get_sphere_coordinates("sqrt(cos(theta)*cos(theta)*cos(phi)*cos(phi))")
        moc.batch_points(coords)
        moc.batch_vertices(ids)
        time.sleep(1)
        moc.show_cloud()


