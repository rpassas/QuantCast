import unittest
from most_active_cookie import most_active_cookie_finder as finder


class TestSum(unittest.TestCase):
    subset = finder("cookie_log.csv", "2011-04-30")
    subset_2 = finder("cookie_log.csv", "2011-05-30")

    def test_load(self):
        """
        Test that all the data has been loaded.
        """
        h, r = self.subset.load_cookie_data()
        self.assertEqual(h, ['cookie', 'timestamp'])
        self.assertEqual(len(r), 19)

    def test_header_val(self):
        """
        Test that correct header labels get chosen.
        """
        h, r = self.subset.load_cookie_data()
        c = self.subset.validate_headers(h, "cookie")
        t = self.subset.validate_headers(h, "timestamp")
        self.assertEqual(c, 0)
        self.assertEqual(t, 1)

    def test_parse_count(self):
        """
        Test that parsing gets the right number of cookies.
        """
        h, r = self.subset.load_cookie_data()
        cookies = len(self.subset.parse_cookie_data(h, r))
        self.assertEqual(cookies, 2)

    def test_parse_accuracy(self):
        """
        Test that parsing gets the right cookies.
        """
        h, r = self.subset.load_cookie_data()
        cookies = self.subset.parse_cookie_data(h, r)
        self.assertEqual(cookies, ['AtY0laUfhglK3IC7', 'iEuBn3fvb654bw3F'])

    def test_parse_accuracy_2(self):
        """
        Test that parsing gets the right cookies.
        """
        h, r = self.subset_2.load_cookie_data()
        cookies = self.subset_2.parse_cookie_data(h, r)
        self.assertEqual(cookies, ['iEuBn3fvb654bw3F'])


if __name__ == '__main__':
    unittest.main()
