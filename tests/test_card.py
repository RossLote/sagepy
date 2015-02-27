from unittest import TestCase
from pysagepay.card import Card
from pysagepay.gateway import SagePay
from pysagepay.response import FakeResponse
from nose.tools import *
import datetime
from dateutil.relativedelta import relativedelta
import mock
from .responses import *


class TestCard(TestCase):
    def setUp(self):
        self.card = Card()
        self.d = {
            'holder' : 'Ross Lote',
            'number' : '5438023004253871',
            'expiry' : datetime.date(2019, 9, 1),
            'cv2' : '123',
            'connection' : SagePay(vendor='tester',mode='test',currency='GBP')
        }
    
    def test__init__(self):
        
        c = Card(**self.d)
        eq_(c.holder, 'Ross Lote')
        eq_(c.number, '5438023004253871')
        eq_(c.type, 'MC')
        eq_(c.expiry, '0919')
        eq_(c.cv2, '123')
        ok_(c.is_ready())
    
    def test__str__(self):
        self.assertEqual(str(self.card), str(self.card._card))
        
    def test__repr__(self):
        self.assertEqual(repr(self.card), repr(self.card._card))
        
    def test_set_connection(self):
        sp = SagePay(
            vendor = 'tester',
            mode = 'test',
            currency = 'GBP'
        )
        self.card.set_connection(sp)
        self.assertEqual(sp, self.card._connection)
        
        test_obj = object()
        
        self.assertRaises(TypeError, self.card.set_connection, test_obj)
        
    def test_holder(self):
        value = 'Ross Lote'
        self.card.holder = value
        eq_(value, self.card.holder)
        
    def test_number(self):
        value = '5438023004253871'
        self.card.number = value
        eq_(value, self.card.number)
        
        value2 = '5438 0230 0425 3871'
        self.card.number = value2
        eq_(value, self.card.number)
        
    def test_expiry(self):
        date = datetime.date(2020, 1, 9)
        self.card.expiry = date
        eq_('0120', self.card.expiry)
        
    def test_type(self):
        value = '5438023004253871'
        self.card.number = value
        eq_('MC', self.card.type)
        
    def test_cv2(self):
        value = '123'
        self.card.cv2 = value
        eq_(value, self.card.cv2)
        
    def test_copy(self):
        d = {
            'CardHolder' : 'Ross Lote',
            'CardNumber' : '5438023004253871',
            'ExpiryDate' : '0519',
            'CardType' : 'MC',
            'CV2' : '123'
        }
        c = self.card
        
        c.holder = 'Ross Lote'
        c.number = '5438023004253871'
        c.expiry = datetime.date(2019, 5, 10)
        c.cv2 = '123'
        
        self.assertDictEqual(d, c.copy())
        
    def test_is_valid(self):
        c = self.card
        c.number = '5438023004253871'
        c.expiry = datetime.date(2019, 5, 10)
        self.assertTrue(c.is_valid())
        
        c.number = '0007802728729873'
        self.assertFalse(c.is_valid())
        
        c.expiry = datetime.date(2013, 5, 10)
        self.assertFalse(c.is_valid())
        
        c.number = '5438023004253871'
        self.assertFalse(c.is_valid())
        
    def test_has_not_expired(self):
        c = self.card
        c.expiry = datetime.date.today() + relativedelta(days=1)
        self.assertTrue(c._has_not_expired())
        
        c.expiry = datetime.date.today() - relativedelta(months=1)
        self.assertFalse(c._has_not_expired())
    
    def test_has_valid_number(self):
        c = self.card
        c.number = '5438023004253871'
        self.assertTrue(c._has_valid_number())
        
        c.number = '0007802728729873'
        self.assertFalse(c._has_valid_number())
        
    def test_cv2_required(self):
        c = self.card
        self.assertTrue(c.cv2_required())
        c.turn_off_cv2()
        self.assertFalse(c.cv2_required())
        
    def test_turn_off_cv2(self):
        c = self.card
        self.assertTrue(c._cv2_required)
        c.turn_off_cv2()
        self.assertFalse(c._cv2_required)
        
    def test_turn_on_cv2(self):
        c = self.card
        self.card._cv2_required = False
        self.assertFalse(c._cv2_required)
        c.turn_on_cv2()
        self.assertTrue(c._cv2_required)
        
    def test_is_ready(self):
        c = self.card
        self.assertFalse(c.is_ready())
        c.holder = 'Ross Lote'
        self.assertFalse(c.is_ready())
        c.number = '5438023004253871'
        self.assertFalse(c.is_ready())
        c.expiry = datetime.date(2019, 5, 10)
        self.assertFalse(c.is_ready())
        c.cv2 = '123'
        self.assertTrue(c.is_ready())
    
    @mock.patch('urllib2.urlopen')
    def test_register(self, mock_obj):
        mock_obj.side_effect = [FakeResponse(token_register_response)]
        
        sp = SagePay(vendor='tester',mode='test', currency='gbp')
        c = Card(**self.d)
        c.set_connection(sp)
        
        response = c.register()
        
        eq_(response.token, '71827364536281726354718273645362817263')