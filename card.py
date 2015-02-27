from utils import (
    build_urls, clean_card_number, get_card_type,
    luhnChecksum, expiry_date_valid, get_expiry_date,
    convert_date, reverse_convert_date
)

import pysagepay

class Card(object):
    
    def __init__(self,**kwargs):
        super(Card, self).__init__()
        self._card = {}
        self._connection = None
        for key, value in kwargs.iteritems():
            if key == 'holder':
                self.holder = value
            elif key == 'number':
                self.number = value
            elif key == 'expiry':
                self.expiry = value
            elif key == 'cv2':
                self.cv2 = value
            elif key == 'connection':
                self.set_connection(value)
        
        self.turn_on_cv2()
    
    def __str__(self):
        return str(self._card)
    
    def __repr__(self):
        return repr(self._card)
    
    def set_connection(self, connection):
        if not isinstance(connection, pysagepay.gateway.SagePay):
            raise TypeError('Connection must be a SagePay instance')
        connection.card = self
        self._connection = connection
    
    @property
    def connection(self):
        return self._connection
    
    @property
    def holder(self):
        return self._card.get('CardHolder')
    
    @holder.setter
    def holder(self, value):
        self._card['CardHolder'] = value
    
    @property
    def number(self):
        return self._card.get('CardNumber')
    
    @number.setter
    def number(self, value):
        card_number = clean_card_number(value)
        
        self._card['CardNumber'] = clean_card_number(card_number)
        self._card['CardType'] = get_card_type(card_number)
    
    @property
    def expiry(self):
        return self._card.get('ExpiryDate')
    
    @expiry.setter
    def expiry(self, value):
        self._card['ExpiryDate'] = convert_date(value)
    
    @property
    def expiry_as_date(self):
        return reverse_convert_date(self.expiry)
    
    @property
    def type(self):
        return self._card.get('CardType')
    
    @property
    def cv2(self):
        return self._card.get('CV2')
    
    @cv2.setter
    def cv2(self, value):
        self._card['CV2'] = value
    
    def copy(self):
        return self._card.copy()
    
    def is_valid(self):
        return all([self._has_not_expired(), self._has_valid_number()])
    
    def _has_not_expired(self):
        date_str = '01' + self.expiry
        return expiry_date_valid(date_str)
            
    def _has_valid_number(self):
        return luhnChecksum(self.number)
    
    def cv2_required(self):
        return self._cv2_required
    
    def turn_off_cv2(self):
        self._cv2_required = False
    
    def turn_on_cv2(self):
        self._cv2_required = True
    
    def is_ready(self):
        try:
            valid = (self.is_valid() and
                    self.holder and
                    self.type)
        except:
            return False
        
        if self.cv2_required() and not self.cv2:
            valid = False
        
        return valid
    
    def register(self):
        return self._connection.register_token()