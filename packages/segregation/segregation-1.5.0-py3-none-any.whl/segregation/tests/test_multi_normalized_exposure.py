import unittest
from libpysal.examples import load_example
import geopandas as gpd
import numpy as np
from segregation.aspatial import MultiNormalizedExposure


class Multi_Normalized_Exposure_Tester(unittest.TestCase):
    def test_Multi_Multi_Normalized_Exposure(self):
        s_map = gpd.read_file(load_example("Sacramento1").get_path("sacramentot2.shp"))
        groups_list = ['WHITE', 'BLACK', 'ASIAN','HISP']
        df = s_map[groups_list]
        index = MultiNormalizedExposure(df, groups_list)
        np.testing.assert_almost_equal(index.statistic, 0.18821879029994157)


if __name__ == '__main__':
    unittest.main()