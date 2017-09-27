# -*- coding: utf-8 -*-
import unittest

import os
from ipgeo import IpGeo

DB_PATH = os.path.split(os.path.realpath('__FILE__'))[0] + '/GeoLite2-City.mmdb'


class TestIpGeo(unittest.TestCase):
    def setUp(self):
        self.ip_geo = IpGeo.open_reader(DB_PATH)(ip_address='128.101.101.101')

    def test_position_format(self):
        position_str = self.ip_geo.position()
        position_tmpl_str = self.ip_geo.position('{latitude}, {longitude}')
        self.assertEqual(position_str, '(44.9759, -93.2166)')
        self.assertEqual(position_tmpl_str, '44.9759, -93.2166')

    def test_postal_code_output(self):
        zip_code = self.ip_geo.zip_code
        postal_code = self.ip_geo.postal_code()
        self.assertEqual(zip_code, postal_code)
        postal_with_desc = self.ip_geo.postal_code(most=False)
        self.assertDictEqual(postal_with_desc, {'desc': 'must be ' + zip_code, 'code': zip_code})

    def test_export(self):
        json_geo = IpGeo.export('128.101.101.101')
        self.assertEqual(json_geo, {
            'ip_address': '128.101.101.101',
            'location_label': 'United States, Minneapolis',
            'postal_code': '55414'
        })

    def test_location_label(self):
        location_label = self.ip_geo.location_label()
        self.assertEqual(location_label, 'United States, Minneapolis')
        location_tmpl_label = self.ip_geo.location_label('{country}|{city}')
        self.assertEqual(location_tmpl_label, 'United States|Minneapolis')

    def test_locale(self):
        zh_cn_ip_geo = IpGeo('128.101.101.101', 'zh-CN')
        self.assertEqual(zh_cn_ip_geo.country_name, '美国')


if __name__ == '__main__':
    unittest.main()
