import unittest
from libpysal.examples import load_example
import geopandas as gpd
import numpy as np
from segregation.aspatial import MultiDivergence


class Multi_Divergence_Tester(unittest.TestCase):
    def test_Multi_Divergence(self):
        s_map = gpd.read_file(load_example("Sacramento1").get_path("sacramentot2.shp"))
        groups_list = ['WHITE', 'BLACK', 'ASIAN','HISP']
        df = s_map[groups_list]
        index = MultiDivergence(df, groups_list)
        np.testing.assert_almost_equal(index.statistic, 0.16645182134289443)


if __name__ == '__main__':
    unittest.main()