import unittest
from libpysal.examples import load_example
import geopandas as gpd
import numpy as np
from segregation.aspatial import MultiInformationTheory


class Multi_Information_Theory_Tester(unittest.TestCase):
    def test_Multi_Information_Theory(self):
        s_map = gpd.read_file(load_example("Sacramento1").get_path("sacramentot2.shp"))
        groups_list = ['WHITE', 'BLACK', 'ASIAN','HISP']
        df = s_map[groups_list]
        index = MultiInformationTheory(df, groups_list)
        np.testing.assert_almost_equal(index.statistic, 0.1710160297858887)


if __name__ == '__main__':
    unittest.main()