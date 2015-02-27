from unittest import TestCase
from pysagepay.gateway import SagePay
from pysagepay.address import SagePayAddress
from pysagepay.card import Card
from pysagepay.response import FakeResponse
from nose.tools import *
import mock
import datetime
from .responses import *

class TestSagePay(TestCase):
    def setUp(self):
        self.sp = SagePay(vendor='tester',mode='test')
        self.a = {
            'firstnames' : 'Ross Adam',
            'surname' : 'Lote',
            'address1' : '1 street name',
            'address2' : 'somewhere',
            'city' : 'somecity',
            'state' : 'Utah',
            'postcode' : 'ab12 3cd',
            'country' : 'uk',
            'phone' : '07898767656'
        }
        self.b = {
            'BillingAddress1': '1 street name',
            'BillingAddress2': 'somewhere',
            'BillingCity': 'somecity',
            'BillingCountry': 'UK',
            'BillingFirstnames': 'Ross Adam',
            'BillingPhone': '07898767656',
            'BillingPostCode': 'AB12 3CD',
            'BillingSurname': 'Lote'
        }
        self.d = {
            'DeliveryAddress1': '1 street name',
            'DeliveryAddress2': 'somewhere',
            'DeliveryCity': 'somecity',
            'DeliveryCountry': 'UK',
            'DeliveryFirstnames': 'Ross Adam',
            'DeliveryPhone': '07898767656',
            'DeliveryPostCode': 'AB12 3CD',
            'DeliverySurname': 'Lote'
        }
        
    def test__init__(self):
        def should_raise_error():
            sp = SagePay(vendor = 'vendorname', mode='badname')
        
        self.assertRaises(ValueError, should_raise_error)
        
    def test__add_address(self):
        self.sp._add_address(self.a, 'billing')
        self.sp._add_address(self.a, 'delivery')
        self.assertDictEqual(self.b, self.sp.billing_address.copy())
        self.assertDictEqual(self.d, self.sp.delivery_address.copy())
        self.assertRaises(ValueError, self.sp._add_address, self.a, 'badname')
    
    def test_add_billing_address(self):
        self.sp.add_billing_address(self.a)
        self.assertDictEqual(self.b, self.sp.billing_address.copy())
    
    def test_add_delivery_address(self):
        self.sp.add_delivery_address(self.a)
        self.assertDictEqual(self.d, self.sp.delivery_address.copy())
    
    def test_add_address(self):
        self.sp.add_address(self.a)
        self.assertDictEqual(self.b, self.sp.billing_address.copy())
        self.assertDictEqual(self.d, self.sp.delivery_address.copy())
    
    def test_description(self):
        value = 'This is a description'
        self.sp.description = value
        eq_(value, self.sp.description)
    
    def test_vendor(self):
        value = 'vendorname'
        self.sp.vendor = value
        eq_(value, self.sp.vendor)
        
        def should_raise_error():
            self.sp.vendor = 2
        
        self.assertRaises(TypeError, should_raise_error)
    
    def test_set_currency(self):
        self.assertRaises(TypeError, self.sp.set_currency, 1)
        self.assertRaises(ValueError, self.sp.set_currency, 'LONG')
        self.sp.set_currency('gbp')
        eq_(self.sp.currency, 'GBP')
    
    def test_build_params(self):
        self.sp.vendor = 'vendorname'
        self.sp.set_currency('gbp')
        params = self.sp._build_params('tx_type')
        expected = {
            'VPSProtocol': '3.00',
            'TxType': 'TX_TYPE',
            'Vendor': 'vendorname',
            'Currency': 'GBP',
        }
        self.assertDictEqual(params, expected)
        
        params = self.sp._build_params('tx_type', {'Other' : 'some other'})
        expected = {
            'VPSProtocol': '3.00',
            'TxType': 'TX_TYPE',
            'Vendor': 'vendorname',
            'Currency': 'GBP',
            'Other' : 'some other'
        }
        self.assertDictEqual(params, expected)
    
    @mock.patch('urllib2.urlopen')
    def test_do_request(self, mock_obj):
        mock_obj.side_effect = [FakeResponse(transaction_response)]
        response = self.sp._do_request('use-token', {})
        eq_(response.token, '71827364536281726354718273645362817263')
    
    @mock.patch('urllib2.urlopen')
    def test_do_transaction(self, mock_obj):
        mock_obj.side_effect = [FakeResponse(transaction_response)]
        response = self.sp._do_transaction('use-token', {})
        eq_(response.token, '71827364536281726354718273645362817263')
    
    def test_generate_tx_id(self):
        code = self.sp.generate_tx_id()
        eq_(code, self.sp.tx_id)
        self.assertNotEqual(code, self.sp.generate_tx_id())
        
        code = self.sp.generate_tx_id()
        eq_(code, self.sp.tx_id)
        self.assertNotEqual(code, self.sp.generate_tx_id())
    
    def test_card(self):
        card = Card()
        self.sp.card = card
        eq_(self.sp.card, card)
        
        def should_raise_error():
            self.sp.card = 'test'
        
        self.assertRaises(TypeError, should_raise_error)
    
    def test_addresses_valid(self):
        self.assertFalse(self.sp.addresses_valid())
        
        self.sp._add_address(self.a, 'billing')
        self.assertFalse(self.sp.addresses_valid())
        
        self.sp._add_address(self.a, 'delivery')
        self.assertTrue(self.sp.addresses_valid())
        
    def test__address_valid(self):
        self.assertFalse(self.sp._address_valid('billing'))
        self.sp._add_address(self.a, 'billing')
        self.assertTrue(self.sp._address_valid('billing'))
        
        self.assertFalse(self.sp._address_valid('delivery'))
        self.sp._add_address(self.a, 'delivery')
        self.assertTrue(self.sp._address_valid('delivery'))
    
    def test_check_description(self):
        self.assertRaises(Exception, self.sp._check_description)
        self.sp.description = 'Description'
        self.sp._check_description()
    
    @mock.patch('urllib2.urlopen')
    def test_register_token(self, mock_obj):
        mock_obj.side_effect = [FakeResponse(token_register_response)]
        d = {
            'holder' : 'Ross Lote',
            'number' : '5438023004253871',
            'expiry' : datetime.date(2019, 9, 1),
            'cv2' : '123'
        }
        card = Card(**d)
        self.sp.set_currency('gbp')
        self.sp.card = card
        response = self.sp.register_token()
        eq_(response.token, '71827364536281726354718273645362817263')
    
    @mock.patch('urllib2.urlopen')
    def test_charge_token(self, mock_obj):
        mock_obj.side_effect = [FakeResponse(transaction_response)]
        token = '71827364536281726354718273645362817263'
        self.sp.add_address(self.a)
        self.sp.description = 'Decription test'
        response = self.sp.charge_token(token=token, amount=20)
        ok_(response.is_successful())
    
    @mock.patch('urllib2.urlopen')
    def test_release(self, mock_obj):
        mock_obj.side_effect = [FakeResponse(release_response)]
        token = '71827364536281726354718273645362817263'
        response = self.sp.release(
            20,
            vendor_tx_id = '983n9e8n938en',
            vps_tx_id = '78b87yb873yb9',
            security_key = '1657156',
            tx_auth_no = '152756'
        )
        ok_(response.is_successful())
        
    @mock.patch('urllib2.urlopen')
    def test_remove_token(self, mock_obj):
        mock_obj.side_effect = [FakeResponse(token_remove_response)]
        token = '71827364536281726354718273645362817263'
        response = self.sp.remove_token(token)
        ok_(response.is_successful())
    
    @mock.patch('urllib2.urlopen')
    def test_refund(self, mock_obj):
        mock_obj.side_effect = [FakeResponse(token_remove_response)]
        self.sp.description = 'Refund description'
        response = self.sp.refund(
            10,
            vps_tx_id = '1234',
            vendor_tx_id = '124387',
            security_key = '1243737',
            tx_auth_no = '12423'
        )
        ok_(response.is_successful())