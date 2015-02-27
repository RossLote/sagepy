from pysagepay.response import Response, FakeResponse
from unittest import TestCase
from .responses import *

response = FakeResponse(transaction_response)

class TestFakeResponse(TestCase):
    
    def test__init__(self):
        r = FakeResponse(transaction_response)
        assert r._str == transaction_response
    
    def test_read(self):
        r = FakeResponse(transaction_response)
        assert r.read() == transaction_response
    
class TestResponse(TestCase):
    def setUp(self):
        data = {'VendorTxCode' : '20'}
        self.r = Response(response, data)
        
    def test_status(self):
        assert self.r.status == 'OK'
        
    def test_status_detail(self):
        self.assertEqual(self.r.status_detail, "Status was OK, no details")
        self.r._response['Status'] = 'NOTAUTHED'
        self.assertEqual(self.r.status_detail, 'Some Other Message')
        
    def test_get_raw_response(self):
        self.assertEqual(self.r.get_raw_response(), response)
        
    def test_is_successful(self):
        self.assertTrue(self.r.is_successful())
        self.r._response['Status'] = 'NOTAUTHED'
        self.assertFalse(self.r.is_successful())
        
    def test_is_declined(self):
        self.assertFalse(self.r.is_declined())
        self.r._response['Status'] = 'NOTAUTHED'
        self.assertTrue(self.r.is_declined())
        
    def test_is_rejected(self):
        self.assertFalse(self.r.is_rejected())
        self.r._response['Status'] = 'REJECTED'
        self.assertTrue(self.r.is_rejected())
        
    def test_protocol(self):
        self.assertEqual(self.r.protocol, '3.00')
        
    def test_avs_cv2(self):
        self.assertEqual(self.r.avs_cv2, 'ALL MATCH')
        
    def test_address_result(self):
        self.assertEqual(self.r.address_result, 'MATCHED')
        
    def test_postcode_result(self):
        self.assertEqual(self.r.postcode_result, 'MATCHED')
        
    def test_cv2_result(self):
        self.assertEqual(self.r.cv2_result, 'MATCHED')
        
    def test_three_d_status(self):
        self.assertEqual(self.r.three_d_status, 'OK')
        
    def test_cavv(self):
        self.assertEqual(self.r.cavv, '76528763987098307838798')
        
    def test_token(self):
        self.assertEqual(self.r.token, '71827364536281726354718273645362817263')
        
    def test_fraud_reponse(self):
        self.assertEqual(self.r.fraud_reponse, 'ACCEPT')
        
    def test_surcharge(self):
        self.assertEqual(self.r.surcharge, '1.00')
        
    def test_expiry_date(self):
        self.assertEqual(self.r.expiry_date, '1115')
        
    def test_bank_auth_code(self):
        self.assertEqual(self.r.bank_auth_code, 'a6b2c3')
    
    def test_bank_decline_code(self):
        self.assertEqual(self.r.bank_decline_code, '02')
        
    def test_vps_tx_id(self):
        self.assertEqual(self.r.vps_tx_id, '71827364536281726354718273645362817263')
        
    def test_security_key(self):
        self.assertEqual(self.r.security_key, 'a1b2c3d4e5')
        
    def test_vendor_tx_code(self):
        self.assertEqual(self.r.vendor_tx_code, '20')
        
    def test_tx_auth_no(self):
        self.assertEqual(self.r.tx_auth_no, '1234567890')
        
    def test_md(self):
        self.assertEqual(self.r.md, '')
        