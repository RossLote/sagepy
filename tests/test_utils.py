from unittest import TestCase
from pysagepay import utils
from nose.tools import *
import datetime

class TestUtils(TestCase):

    def test_luhnChecksum(self):
        valid_number = '4018724994588611'
        invalid_number = '1020304050607089'
        
        ok_(utils.luhnChecksum(valid_number))
        ok_(not utils.luhnChecksum(invalid_number))
        
    def test_build_urls(self):
        urls = utils.build_urls('live')
        eq_(urls['refund'], 'https://live.sagepay.com/gateway/service/refund.vsp')
        eq_(urls['register-token'], 'https://live.sagepay.com/gateway/service/directtoken.vsp')
        eq_(urls['use-token'], 'https://live.sagepay.com/gateway/service/vspdirect-register.vsp')
        
        urls = utils.build_urls('test')
        eq_(urls['refund'], 'https://test.sagepay.com/gateway/service/refund.vsp')
        eq_(urls['register-token'], 'https://test.sagepay.com/gateway/service/directtoken.vsp')
        eq_(urls['use-token'], 'https://test.sagepay.com/gateway/service/vspdirect-register.vsp')
        
        self.assertRaises(ValueError, utils.build_urls, 'badname')
        
    def test_build_url(self):
        url = utils._build_url('live', 'some-end-point')
        eq_(url, 'https://live.sagepay.com/gateway/service/some-end-point.vsp')
        
        url = utils._build_url('test', 'some-other-end-point')
        eq_(url, 'https://test.sagepay.com/gateway/service/some-other-end-point.vsp')
        
    def test_build_token_urls(self):
        urls = utils._build_token_urls('live')
        eq_(urls['register-token'], 'https://live.sagepay.com/gateway/service/directtoken.vsp')
        eq_(urls['use-token'], 'https://live.sagepay.com/gateway/service/vspdirect-register.vsp')
        
        urls = utils.build_urls('test')
        eq_(urls['register-token'], 'https://test.sagepay.com/gateway/service/directtoken.vsp')
        eq_(urls['use-token'], 'https://test.sagepay.com/gateway/service/vspdirect-register.vsp')
    
    def test_clean_card_number(self):
        number = '0987098767578263'
        eq_(number, utils.clean_card_number(number))
        
        eq_(number, utils.clean_card_number('0987 0987 6757 8263'))
        
        eq_(number, utils.clean_card_number(' 09 870987 67 578 263 '))
        
    def test_get_end_of_month(self):
        date_1 = datetime.date(2014, 1, 10)
        date_2 = datetime.date(2014, 1, 31)
        eq_(date_2, utils.get_end_of_month(date_1))
        
        date_1 = datetime.date(2014, 1, 31)
        eq_(date_2, utils.get_end_of_month(date_1))
        
    def test_expiry_date_valid(self):
        self.assertFalse(utils.expiry_date_valid('0112'))
        self.assertTrue(utils.expiry_date_valid('0119'))
        
    def test_get_new_transaction_id(self):
        code = utils.get_new_transaction_id()
        self.assertNotEqual(code, utils.get_new_transaction_id())
        
        code = utils.get_new_transaction_id()
        self.assertNotEqual(code, utils.get_new_transaction_id())
        
        code = utils.get_new_transaction_id()
        self.assertNotEqual(code, utils.get_new_transaction_id())
        
    def test_generate_transaction_id(self):
        code = utils.get_new_transaction_id()
        self.assertNotEqual(code, utils._generate_transaction_id())
        
        code = utils.get_new_transaction_id()
        self.assertNotEqual(code, utils._generate_transaction_id())
        
        code = utils.get_new_transaction_id()
        self.assertNotEqual(code, utils._generate_transaction_id())
        
    def test_get_expiry_month(self):
        eq_('01', utils._get_expiry_month(1))
        eq_('01', utils._get_expiry_month(01))
        eq_('01', utils._get_expiry_month('1'))
        eq_('01', utils._get_expiry_month('01'))
        eq_('09', utils._get_expiry_month(9))
        eq_('09', utils._get_expiry_month('9'))
        eq_('09', utils._get_expiry_month('09'))
        eq_('10', utils._get_expiry_month(10))
        eq_('10', utils._get_expiry_month('10'))
        
        self.assertRaises(ValueError, utils._get_expiry_month, 13)
        self.assertRaises(ValueError, utils._get_expiry_month, '13')
        self.assertRaises(ValueError, utils._get_expiry_month, 0)
        self.assertRaises(ValueError, utils._get_expiry_month, '0')
        self.assertRaises(ValueError, utils._get_expiry_month, '00')
    
    def test_get_expiry_year(self):
        eq_('01', utils._get_expiry_year(2001))
        eq_('01', utils._get_expiry_year('2001'))
        eq_('01', utils._get_expiry_year('01'))
        eq_('15', utils._get_expiry_year(2015))
        eq_('15', utils._get_expiry_year('2015'))
        eq_('15', utils._get_expiry_year('15'))
        eq_('99', utils._get_expiry_year(1999))
        eq_('99', utils._get_expiry_year('1999'))
        eq_('99', utils._get_expiry_year('99'))
    
    def test_get_expiry_date(self):
        eq_('0101', utils.get_expiry_date(2001, 1))
        eq_('0101', utils.get_expiry_date('2001', 1))
        eq_('0101', utils.get_expiry_date(2001, '01'))
        
        eq_('0999', utils.get_expiry_date(1999, 9))
        eq_('0999', utils.get_expiry_date('1999', 9))
        eq_('0999', utils.get_expiry_date(1999, '09'))
        
    def test_reverse_convert_date(self):
        date = '0120'
        eq_(datetime.date(2020,1,31), utils.reverse_convert_date(date))
        
    def test_convert_date(self):
        date = datetime.date(2013, 3, 15)
        eq_('0313', utils.convert_date(date))
        
    def test_get_card_type(self):
        visa = '4647340240520479'
        visa13 = '4539869291891'
        mc = '5189404886776125'
        dc = '6011197912741046'
        amex = '375125874463021'
        unknown = '098098098098098'
        
        eq_('VISA', utils.get_card_type(visa))
        eq_('VISA', utils.get_card_type(visa13))
        eq_('MC', utils.get_card_type(mc))
        eq_('DC', utils.get_card_type(dc))
        eq_('AMEX', utils.get_card_type(amex))
        eq_('Unknown', utils.get_card_type(unknown))
    
    def test_encode_transaction_request(self):
        d = {
            'willy' : 'wonka',
            'foo' : 'bar',
            'winger' : 'singer blinger'
        }
        expected = 'willy=wonka&foo=bar&winger=singer+blinger'
        eq_(expected, utils.encode_transaction_request(d))