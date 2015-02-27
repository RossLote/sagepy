from unittest import TestCase
from pysagepay.address import SagePayAddress
import ast

class TestAddress(TestCase):
    def setUp(self):
        self.address = SagePayAddress(address_type='billing')
        self.test_dict = {
            'BillingPostCode': None,
            'BillingFirstnames': None,
            'BillingPhone': None,
            'BillingAddress2': None,
            'BillingAddress1': None,
            'BillingSurname': None,
            'BillingCountry': None,
            'BillingCity': None
        }
        self.test_dict_2 = {
            'DeliveryPostCode': None,
            'DeliveryFirstnames': None,
            'DeliveryPhone': None,
            'DeliveryAddress2': None,
            'DeliveryAddress1': None,
            'DeliverySurname': None,
            'DeliveryCountry': None,
            'DeliveryCity': None
        }
        self.test_dict_3 = {
            'firstnames' : 'Ross',
            'surname' : 'Lote',
            'address1' : '23 Blah Blah road',
            'address2' : 'Somewhere',
            'city' : 'Citiesville',
            'postcode' : 'AB12 7YG',
            'country' : 'UK',
            'phone' : '098098098'
        }
    
    def assertDictStringsEqual(self, dict_str1, dict_str2):
        dict1 = ast.literal_eval(dict_str1)
        dict2 = ast.literal_eval(dict_str2)
        self.assertDictEqual(dict1, dict2)
        return True
    
    def test__init__(self):
        dd = {}
        for key, value in self.test_dict_3.iteritems():
            if key == 'postcode':
                dd['{}PostCode'.format('Billing')] = value
            else:
                dd['{}{}'.format('Billing', key.title())] = value
        
        address = SagePayAddress(
            address_type = 'billing',
            address_dict = self.test_dict_3
        )
        
        self.assertDictEqual(dd, address.copy())
        
        
    def test__str__(self):
        self.assertDictStringsEqual(str(self.address), str(self.test_dict))
        self.address.surname = 'Lote'
        self.test_dict['BillingSurname'] = 'Lote'
        self.assertDictStringsEqual(str(self.address), str(self.test_dict))
    
    def test__repr__(self):
        self.assertDictStringsEqual(repr(self.address), repr(self.test_dict))
        self.address.firstnames = 'Ross Adam'
        self.test_dict['BillingFirstnames'] = 'Ross Adam'
        self.assertDictStringsEqual(str(self.address), str(self.test_dict))
    
    def test_get_address_dict(self):
        self.assertDictEqual(self.address._get_address_dict(), self.test_dict)
        self.address.city = 'Somewhere'
        self.test_dict['BillingCity'] = 'Somewhere'
        self.assertDictEqual(self.address._get_address_dict(), self.test_dict)
        
        self.address.country = 'UK'
        self.assertFalse('BillingState' in self.address._get_address_dict())
        
        self.address.country = 'US'
        self.assertTrue('BillingState' in self.address._get_address_dict())
        
        self.test_dict_2['DeliveryState'] = None
        self.address.address_type = 'delivery'
        self.assertItemsEqual(self.test_dict_2.keys(), self.address._get_address_dict().keys())
        
    def test_f_p(self):
        fp = self.address._field_properties
        prop = 'max_length'
        field = 'Surname'
        self.assertEqual(fp[field][prop], self.address._f_p(field, prop))
        prop = 'required'
        self.assertEqual(fp[field][prop], self.address._f_p(field, prop))
        field = 'Country'
        self.assertEqual(fp[field][prop], self.address._f_p(field, prop))
        
    
    def test_required(self):
        fp = self.address._field_properties
        field = 'Surname'
        self.assertEqual(fp[field]['max_length'], self.address._length(field))
        field = 'Country'
        self.assertEqual(fp[field]['max_length'], self.address._length(field))
    
    def test_length(self):
        fp = self.address._field_properties
        field = 'Surname'
        self.assertEqual(fp[field]['required'], self.address._required(field))
        field = 'Country'
        self.assertEqual(fp[field]['required'], self.address._required(field))
    
    def test_copy(self):
        self.assertDictEqual(self.address.copy(), self.test_dict)
    
    def test_from_dict(self):
        dd = {}
        for key, value in self.test_dict_3.iteritems():
            if key == 'postcode':
                dd['{}PostCode'.format('Billing')] = value
            else:
                dd['{}{}'.format('Billing', key.title())] = value
        self.address.from_dict(self.test_dict_3)
        self.assertDictEqual(dd, self.address.copy())
    
    def test_is_valid(self):
        a = self.address
        self.assertFalse(a.is_valid())
        
        a.firstnames = 'Ross'
        a.surname = 'Lote'
        a.address1 = '1 somewhere road'
        a.city = 'birmingburgh'
        a.country = 'uk'
        self.assertFalse(a.is_valid())
        
        a.postcode = 'gj10 4wr'
        self.assertTrue(a.is_valid())
        
        a.country = 'us'
        self.assertFalse(a.is_valid())
        
        a.state = 'Utah'
        self.assertTrue(a.is_valid())
        
        a.country = 'Uk'
        self.assertTrue(a.is_valid())
    
    def test_address_type(self):
        self.assertDictEqual(self.address.copy(), self.test_dict)
        self.address.address_type = 'delivery'
        self.assertEqual(self.address.address_type.title(), 'Delivery')
        self.assertDictEqual(self.address.copy(), self.test_dict_2)
        
        def shouldRaiseException():
            self.address.address_type = 'random_string'
        
        self.assertRaises(ValueError, shouldRaiseException)
    
    def test_surname(self):
        name = 'Thisisareallylonglastname'
        self.address.surname = name
        self.assertEqual(self.address.surname, name[:20])
    
    def test_firstnames(self):
        name = 'These are really long firstnames'
        self.address.firstnames = name
        self.assertEqual(self.address.firstnames, name[:20])
    
    def test_address1(self):
        value = 'This is a really long string for the first line of the address, needs to be more than 100 charaters long'
        self.address.address1 = value
        self.assertEqual(self.address.address1, value[:100])
    
    def test_address2(self):
        value = 'This is a really long string for the second line of the address, needs to be more than 100 charaters long'
        self.address.address2 = value
        self.assertEqual(self.address.address2, value[:100])
    
    def test_city(self):
        value = 'This is a really long name for a city, seriously'
        self.address.city = value
        self.assertEqual(self.address.city, value[:40])
    
    def test_state(self):
        value = 'Utah'
        self.address.state = value
        self.assertEqual(self.address.state, value[:2].upper())
    
    def test_postcode(self):
        value = 'postcode of10chars'
        self.address.postcode = value
        self.assertEqual(self.address.postcode, value[:10].upper())
    
    def test_country(self):
        value = 'uk'
        self.address.country = value
        self.assertEqual(self.address.country, value[:2].upper())
    
    def test_phone(self):
        value = '098987876765654543432321'
        self.address.phone = value
        self.assertEqual(self.address.phone, value[:20])