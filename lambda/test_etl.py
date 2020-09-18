import unittest

from etl_module import extract_nyt, extract_jh


class TestETL(unittest.TestCase):

    def test_nyt_success(self):
        
        data = """date,cases,deaths
2020-01-21,1,0
2020-01-22,1,0
2020-01-23,1,0"""
        cases, exceptions = extract_nyt(data)
        self.assertEqual(len(exceptions), 0)
        self.assertEqual(len(cases), 3)
        
    def test_nyt_fail(self):
        
        data = """date,cases,deaths
2020-01f-21,1,0
20s20-01-22,1,0
2020-01-g23,1,0"""
        cases, exceptions = extract_nyt(data)
        self.assertEqual(len(exceptions), 3)
        self.assertEqual(len(cases), 0)

        
    def test_jh_success(self):
        
        data = """Date,Country/Region,Province/State,Lat,Long,Confirmed,Recovered,Deaths
2020-01-22,US,,33.93911,67.709953,0,0,0
2020-01-23,US,,33.93911,67.709953,0,0,0
2020-01-24,US,,33.93911,67.709953,0,0,0"""

        recovered, exceptions = extract_jh(data)
        print('recovered', recovered)
        print('exceptions', exceptions)
        self.assertEqual(len(exceptions), 0)
        self.assertEqual(len(recovered), 3)
        
    def test_jh_fail(self):

        data = """Date,Country/Region,Province/State,Lat,Long,Confirmed,Recovered,Deaths
2020-01f-22,US,,33.93911,67.709953,0,0,0
20240-01-23,US,,33.93911,67.709953,0,0,0
2020-01r-24,US,,33.93911,67.709953,0,0,0"""
        recovered, exceptions = extract_jh(data)
        self.assertEqual(len(exceptions), 3)
        self.assertEqual(len(recovered), 0)


if __name__ == '__main__':
    unittest.main()