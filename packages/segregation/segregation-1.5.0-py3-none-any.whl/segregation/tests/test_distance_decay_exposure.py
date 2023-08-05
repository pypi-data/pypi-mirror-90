import unittest
from libpysal.examples import load_example
import geopandas as gpd
import numpy as np
from segregation.spatial import DistanceDecayExposure


class Distance_Decay_Exposure_Tester(unittest.TestCase):
    def test_Distance_Decay_Exposure(self):
        s_map = gpd.read_file(load_example("Sacramento1").get_path("sacramentot2.shp"))
        df = s_map[['geometry', 'HISP', 'TOT_POP']]
        index = DistanceDecayExposure(df, 'HISP', 'TOT_POP')
        np.testing.assert_almost_equal(index.statistic, 0.8396583368412371)


if __name__ == '__main__':
    unittest.main()
