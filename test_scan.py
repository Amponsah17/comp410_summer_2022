import unittest
from scan import show_aggie_pride


class ScanTests(unittest.TestCase):
    def test_aggie_pride(self):
        slogans = show_aggie_pride()

        self.assertIn('Aggie Pride - Worldwide', slogans)


if __name__ == '__main__':
    unittest.main()
