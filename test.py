import unittest
from bs4 import BeautifulSoup
from parse import *

class TestParseBedBathFeet(unittest.TestCase):
    def setUp(self):
        html1 = '''
        <div class="mapAndAttrs">
        <div class="mapbox">
        <div id="map" class="viewposting" data-latitude="45.514200" data-longitude="-122.498500" data-accuracy="22"></div>
        <div class="mapaddress">19909 SE Washington Ct</div>
        <p class="mapaddress">
        <small>
        (<a target="_blank" href="https://maps.google.com/?q=loc%3A+%31%39%39%30%39+SE+Washington+Ct+Portland+OR+US">google map</a>)
        </small>
        </p>
        </div>   <p class="attrgroup">
        <span><b>3BR</b> / <b>1.5Ba</b></span>
        <span><b>1100</b>ft<sup>2</sup></span>
        <span class="housing_movein_now property_date" data-date="2017-01-07"
        data-today_msg="available now">available jan 7</span>
        </p>
        <p class="attrgroup">
        <span>duplex</span><br>
        <span>w/d hookups</span><br>
        <span>attached garage</span><br>
        </p>
        </div>
        '''
        self.b1 = BeautifulSoup(html1, "html.parser")
        self.bedbathfeet, _ = attributes(self.b1)

    def test_bed_int(self):
        bed, bath, feet = bedbathfeet(self.bedbathfeet)
        self.assertEqual(bed, 3, 'parsing out the wrong number of beds')
        self.assertEqual(bath, 1.5, 'parsing out the wrong number of baths')
        self.assertEqual(feet, 1100)

    def


if __name__ == '__main__':
    unittest.main()