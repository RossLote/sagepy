from utils import (
    build_urls, clean_card_number, get_card_type,
    convert_date, get_expiry_date, luhnChecksum, expiry_date_valid,
    get_new_transaction_id, ADDRESS_FIELDS
)
from .card import Card
from .request import Request
from .address import SagePayAddress
from decimal import Decimal

class SagePay(object):
    
    def __init__(self, vendor, mode, description='', currency=''):
        if not mode in ('live', 'test'):
            raise ValueError('mode must be either live or test')
        
        self._transaction_mode = mode
        self._vendor = vendor
        self._description = description
        self._urls = build_urls(mode)
        self.tx_id = None
        self._card = None
        if currency:
            self.set_currency(currency)
        
    def _add_address(self, address, address_type):
        setattr(self,'{}_address'.format(address_type.lower()),
                SagePayAddress(address_type, address))
    
    def add_billing_address(self, address):
        self._add_address(address, 'billing')
    
    def add_delivery_address(self, address):
        self._add_address(address, 'delivery')
    
    def add_address(self, address):
        self._add_address(address, 'billing')
        self._add_address(address, 'delivery')
    
    @property
    def description(self):
        return self._description
    
    @description.setter
    def description(self, value):
        self._description = value
    
    @property
    def vendor(self):
        return self._vendor
    
    @vendor.setter
    def vendor(self, vendor):
        if not isinstance(vendor, str):
            raise TypeError('vendor must be a string')
        
        self._vendor = vendor
    
    def set_currency(self, currency):
        if not any([isinstance(currency, str), isinstance(currency, unicode)]):
            raise TypeError('currency must be of type string or unicode')
        if len(currency) > 3:
            raise ValueError('no more than 3 charactes allowed in currency')
        self.currency = currency.upper()
        
    def _build_params(self, tx_type, extras = {}):
        params = {
            'VPSProtocol': '3.00',
            'TxType': tx_type.upper(),
            'Vendor': self.vendor,
        }
        if hasattr(self, 'currency') and self.currency:
            params['Currency'] = self.currency
        params.update(extras)
        return params
    
    def _do_request(self, url_key, payload):
        url = self._urls[url_key]
        
        request = Request(
            url = url,
            payload = payload
        )
        
        return request.send()
    
    def _do_transaction(self, url_key, payload):
        if not self.tx_id:
            self.tx_id = get_new_transaction_id()
        payload.update(
            {'VendorTxCode' : self.tx_id}
        )
        return self._do_request(url_key, payload)
    
    def generate_tx_id(self):
        self.tx_id = get_new_transaction_id()
        return self.tx_id
    
    @property
    def card(self):
        return self._card
    
    @card.setter
    def card(self, card):
        if isinstance(card, Card):
            self._card = card
        else:
            raise TypeError('card must be an instance of Card')
    
    def addresses_valid(self, ):
        valid = True
        for address in ['delivery', 'billing']:
            if not self._address_valid(address):
                valid = False
        
        return valid

    def _address_valid(self, prefix):
        if hasattr(self, '{}_address'.format(prefix)):
            address = getattr(self, '{}_address'.format(prefix))
            return address.is_valid()
        return False
    
    def _check_description(self):
        if not self.description:
            raise Exception('Please set transaction description')
    
    def register_token(self):
        if not self.card:
            raise Exception('There are no card details attached')
        if self.card.is_ready():
            payload = self._build_params('token', self.card.copy())
            return self._do_request('register-token', payload)
        else:
            raise Exception(
                'The card is not valid. Did you complete all details?'
            )
        
    def register_and_charge(self, amount, extra_data={}):
        
        self._check_description()
        
        if self.addresses_valid():
            extra_data.update(self.delivery_address.copy())
            extra_data.update(self.billing_address.copy())
            extra_data.update(self.card.copy())
            extra_data['Amount'] = amount
            extra_data['Description'] = self.description
            extra_data['CreateToken'] = 1
            payload = self._build_params('payment', extra_data)
            return self._do_transaction('use-token', payload)
        else:
            raise Exception('Your address details are incomplete')
    
    def charge_token(
        self, token, amount, store_token = 1,
        tx_type = 'payment', continuous=True, extra_data={}):
        
        self._check_description()
        
        if self.addresses_valid():
            extra_data.update(self.delivery_address.copy())
            extra_data.update(self.billing_address.copy())
            extra_data['Amount'] = amount
            extra_data['Token'] = token
            extra_data['Description'] = self.description
            extra_data['StoreToken'] = store_token
            if continuous:
                extra_data['AccountType'] = 'C'
            payload = self._build_params(tx_type, extra_data)
            return self._do_transaction('use-token', payload)
        else:
            raise Exception('Your address details are incomplete')
    
    def three_d_secure(self,
                       md=None,
                       pa_res=None):
        payload = {
            'MD' : md,
            'PARes' : pa_res
        }
        
        return self._do_request('3d-secure', payload)
    
    def release(
                self,
                amount,
                vendor_tx_id = None,
                vps_tx_id = None,
                security_key = None,
                tx_auth_no = None
            ):
        if isinstance(amount, int):
            amount = Decimal('{}.00'.format(amount))
        data = {
            'VendorTxCode' : vendor_tx_id,
            'VPSTxId' : vps_tx_id,
            'SecurityKey' : security_key,
            'TxAuthNo' : tx_auth_no,
            'amount' : amount,
        }
        payload = self._build_params('release', data)
        return self._do_request('release', payload)
    
    def remove_token(self, token):
        payload = self._build_params('removetoken', {'token' : token})
        if payload.get('currency'):
            del payload['Currency']
        return self._do_request('remove-token', payload)
        
    def refund(self, amount,
                vps_tx_id = None,
                vendor_tx_id = None,
                security_key = None,
                tx_auth_no = None
            ):
        
        self._check_description()
            
        
        data = {
            'Amount' : amount,
            'RelatedVPSTxId' : vps_tx_id,
            'RelatedVendorTxCode' : vendor_tx_id,
            'RelatedSecurityKey' : security_key,
            'RelatedTxAuthNo' : tx_auth_no,
            'Description' : self.description
        }
        
        payload = self._build_params('refund', data)
        return self._do_transaction('refund', payload)
    
    def void(self,
            vps_tx_id = None,
            vendor_tx_id = None,
            security_key = None,
            tx_auth_no = None):
            
        data = {
            'VPSTxId' : vps_tx_id,
            'VendorTxCode' : vendor_tx_id,
            'SecurityKey' : security_key,
            'TxAuthNo' : tx_auth_no,
        }
        
        payload = self._build_params('void', data)
        return self._do_request('void', payload)