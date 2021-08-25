import unittest
from read_Kp import *
from read_cdf import *
from model import *

class Tests(unittest.TestCase):

    def test_read_Kp(self):
        Kp_data = read_Kp("testdata/Kp_data.lst")
        self.assertEqual(Kp_data, {1512: 8.1, 1513: 6.4, 1514: 4.9, 1515: 3.6})

    def test_find_orbit(self):
        OrbTimes = [2, 3, 5, 7, 11]
        self.assertEqual(find_orbit(OrbTimes, 4), 2)

    def test_points_from_cdf(self):
        path = "testdata/test.cdf"
        cdf = pycdf.CDF(path)
        mu_ = 4.5
        I_ = 1.3333
        tolerance = 0.1
        points = [(datetime.datetime(2017, 12, 26, 0, 0, 30),
                   4.20448,
                   1.34193,
                   4.421030044555664,
                   2.2004580387147143e-05),
                  (datetime.datetime(2017, 12, 26, 0, 1, 30),
                   4.2184740000000005,
                   1.3385500000000001,
                   4.474546909332275,
                   2.381381818850059e-05),
                  (datetime.datetime(2017, 12, 26, 0, 2, 30),
                   4.232468,
                   1.33517,
                   4.529375076293945,
                   2.996713010361418e-05),
                  (datetime.datetime(2017, 12, 26, 0, 3, 30),
                   4.246462,
                   1.33179,
                   4.5855631828308105,
                   3.1091349228518084e-05),
                  (datetime.datetime(2017, 12, 26, 0, 4, 30),
                   4.260456,
                   1.3284099999999999,
                   4.643163204193115,
                   3.383381772437133e-05)]
        self.assertEqual(points_from_cdf(cdf, mu_, I_, tolerance), points)

    def test_points_into_orbits(self):
        orbTimes = [
            datetime.datetime(2000, 1, 1, 2, 0, 0, 0),
            datetime.datetime(2000, 1, 1, 3, 0, 0, 0),
            datetime.datetime(2000, 1, 1, 5, 0, 0, 0),
            datetime.datetime(2000, 1, 1, 7, 0, 0, 0),
            datetime.datetime(2000, 1, 1, 11, 0, 0, 0)]
        points = [
            (datetime.datetime(2000, 1, 1, 8, 0, 0, 0), 5, 3, 4, 2),
            (datetime.datetime(2000, 1, 1, 10, 0, 0, 0), 4, 7, 2, 7.8),
            (datetime.datetime(2000, 1, 1, 11, 30, 0, 0), 4, 8, 4, 8),
            (datetime.datetime(2000, 1, 1, 2, 15, 0, 0), 2, 2, 2, 2),
            (datetime.datetime(2000, 1, 1, 1, 0, 0, 0), 9, 8, 7, 6)]
        orbPoints = [[(datetime.datetime(2000, 1, 1, 1, 0), 9, 8, 7, 6)],
                     [(datetime.datetime(2000, 1, 1, 2, 15), 2, 2, 2, 2)],
                     [],
                     [],
                     [(datetime.datetime(2000, 1, 1, 8, 0), 5, 3, 4, 2),
                      (datetime.datetime(2000, 1, 1, 10, 0), 4, 7, 2, 7.8)],
                     [(datetime.datetime(2000, 1, 1, 11, 30), 4, 8, 4, 8)]]
        self.assertEqual(points_into_orbits(orbTimes, points), orbPoints)

    def test_data_from_orbit_points(self):
        ops = [[(datetime.datetime(2000, 1, 1, 1, 0), 9, 8, 7, 6)],
                     [(datetime.datetime(2000, 1, 1, 2, 15), 2, 2, 2, 2)],
                     [],
                     [],
                     [(datetime.datetime(2000, 1, 1, 8, 0), 4.12, 3, 4, 2),
                      (datetime.datetime(2000, 1, 1, 10, 0), 4, 7, 2, 7.8)],
                     [(datetime.datetime(2000, 1, 1, 11, 30), 3.95, 8, 4, 8)]]
        L_range = (4, 4.1)
        nL = 4
        data_from_orbit_points(ops, L_range, nL)

    def test_find_min_max_times(self):
        ts = np.array([[datetime.datetime(2000, 1, 1, 8, 0),
                        np.nan,
                        datetime.datetime(2000, 1, 1, 9, 30)],
                       [datetime.datetime(2000, 1, 1, 11, 0),
                        datetime.datetime(2000, 1, 1, 10, 30),
                        datetime.datetime(2000, 1, 1, 9, 30)],
                       [np.nan,
                        datetime.datetime(2000, 1, 1, 8, 0),
                        datetime.datetime(2000, 1, 1, 13, 30)],
                       [datetime.datetime(2000, 1, 1, 15, 0),
                        np.nan,
                        datetime.datetime(2000, 1, 1, 14, 30)]])
        minmax = (datetime.datetime(2000, 1, 1, 9, 30),
                  datetime.datetime(2000, 1, 1, 10, 30))
        self.assertEqual(find_min_max_times(ts), minmax)

    def test_time_linspace(self):
        times = [datetime.datetime(2000, 1, 1, 8, 0),
                 datetime.datetime(2000, 1, 1, 9, 0),
                 datetime.datetime(2000, 1, 1, 10, 0),
                 datetime.datetime(2000, 1, 1, 11, 0),
                 datetime.datetime(2000, 1, 1, 12, 0)]
        self.assertEqual(time_linspace(datetime.datetime(2000, 1, 1, 8, 0),
                                       datetime.datetime(2000, 1, 1, 12, 0),
                                       5), times)

    def test_interpolated_PSD(self):
        L, t = 3.5, datetime.datetime(2000, 1, 1, 8, 0) #m=0
        Li = [3, 4, 5]
        ts = np.array([[datetime.datetime(2000, 1, 1, 7, 0),
                        datetime.datetime(2000, 1, 1, 7, 30),
                        datetime.datetime(2000, 1, 1, 9, 0)],
                       [datetime.datetime(2000, 1, 1, 8, 30),
                        datetime.datetime(2000, 1, 1, 9, 0),
                        datetime.datetime(2000, 1, 1, 10, 0)],
                       [datetime.datetime(2000, 1, 1, 13, 0),
                        datetime.datetime(2000, 1, 1, 14, 0),
                        datetime.datetime(2000, 1, 1, 15, 0)]])
        # ts[:, 0], Li[:, 1]
        F_bars = np.array([[5, 9, 3],
                           [8, 6, 0],
                           [1, 6, 11]])
        interpolated = interpolated_PSD(L, t, Li, ts, F_bars)

        self.assertAlmostEqual(interpolated, 7.333270549944682)

    def test_complete_PSD(self):
        Li = [3, 4, 5]
        ts = np.array([[datetime.datetime(2000, 1, 1, 7, 0),
                        datetime.datetime(2000, 1, 1, 7, 30),
                        datetime.datetime(2000, 1, 1, 8, 0)],
                       [datetime.datetime(2000, 1, 1, 8, 30),
                        datetime.datetime(2000, 1, 1, 9, 0),
                        datetime.datetime(2000, 1, 1, 10, 0)],
                       [datetime.datetime(2000, 1, 1, 13, 0),
                        datetime.datetime(2000, 1, 1, 14, 0),
                        datetime.datetime(2000, 1, 1, 15, 0)]])
        # ts[:, 0], Li[:, 1]
        F_bars = np.array([[5, 9, 3],
                           [8, 6, 0],
                           [1, 6, 11]])
        t_range = (datetime.datetime(2000, 1, 1, 8, 0),
                   datetime.datetime(2000, 1, 1, 13, 0))
        nTimes = 2
        times, complete = complete_PSD(Li, ts, F_bars, t_range, nTimes)
        correct = np.array([[6.839904, 7.862224, 3], [1, 6, 0]])
        self.assertEqual(times, [datetime.datetime(2000, 1, 1, 8, 0),
                                 datetime.datetime(2000, 1, 1, 13, 0)])
        np.testing.assert_allclose(complete, correct)

    def test_interpolate_1D(self):
        xi = [2, 4, 7]
        fi = [6, 8, 2]
        self.assertAlmostEqual(interpolate1D(xi, fi, 2), 6)
        self.assertAlmostEqual(interpolate1D(xi, fi, 3), 7)
        self.assertAlmostEqual(interpolate1D(xi, fi, 5), 6)
        self.assertAlmostEqual(interpolate1D(xi, fi, 7), 2)


    def test_interpolate_2D(self):
        xi = [2, 5, 8]
        yi = [4, 8, 12, 16]
        fi = np.array([[1, 16, 8, 3], [12, 4, 0, 8], [7, 3, 19, 7]])
        self.assertAlmostEqual(interpolate2D(xi, yi, fi, 2, 4), 1)
        self.assertAlmostEqual(interpolate2D(xi, yi, fi, 3, 11), 7)
        self.assertAlmostEqual(interpolate2D(xi, yi, fi, 6, 6), 7)
        self.assertAlmostEqual(interpolate2D(xi, yi, fi, 8, 16), 7)

    def test_diffusion(self):
        LRange = (3.5, 4.5)
        tRange = (0, 2)
        nL = 3
        nT = 2
        f0 = lambda L: 1e-7 * (100**L)
        def D_LL(L, Kpt):
            return L*Kpt + 1
        def tau(L, Kpt):
            return Kpt
        uL = lambda t: 2**(t/2)
        uR = lambda t: 100*(2**(-t/2))
        Kp = lambda t: t/2
        u_correct = np.array([[1., 2.], [10., 23.45021064], [100., 50.]])
        Li, u = solve_diffusion(LRange, tRange, nL, nT, f0, D_LL, tau, uL, uR,
                                Kp)
        np.testing.assert_almost_equal(Li, np.array([3.5, 4.0, 4.5]))
        np.testing.assert_almost_equal(u, u_correct)







if __name__ == '__main__':
    unittest.main()