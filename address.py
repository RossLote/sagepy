from utils import (
    build_urls, clean_card_number, get_card_type,
    convert_date, get_expiry_date, luhnChecksum, expiry_date_valid,
    get_new_transaction_id, ADDRESS_FIELDS, ADDRESS_TYPES, POSTCODE_COUTRIES
)

class SagePayAddress(object):
    def __init__(self, address_type=None, address_dict = None):
        self._address = {}
        self._field_properties = {}
        for field, length, required in ADDRESS_FIELDS:
            self._address[field] = None
            self._field_properties[field] = {
                'max_length' : length,
                'required' : required
            }
            attr = field.lower()
        if address_dict:
            self.from_dict(address_dict)
        self.address_type = address_type
    
    def __str__(self):
        d = self._get_address_dict()
        return str(d)
    
    def __repr__(self):
        d = self._get_address_dict()
        return repr(d)
    
    def _get_address_dict(self):
        d = {}
        for key, value in self._address.iteritems():
            if key == 'State':
                if self.country == 'US':
                    d['{}{}'.format(self.address_type, key)] = value
            else:
                d['{}{}'.format(self.address_type, key)] = value
            
        return d
    
    def _f_p(self, field, prop):
        return self._field_properties[field][prop]
    
    def _required(self, field):
        return self._f_p(field, 'required')

    def _length(self, field):
        return self._f_p(field, 'max_length')
    
    def copy(self):
        return self._get_address_dict()
    
    def from_dict(self, address_dict):
        for key, value in address_dict.iteritems():
            if hasattr(self, key.lower()):
                setattr(self, key.lower(), value)
    
    def is_valid(self):
        required_values = []
        for key, value in self._address.iteritems():
            if self._required(key):
                if key == 'PostCode':
                    if self.country in POSTCODE_COUTRIES:
                        required_values.append(value)
                else:
                    required_values.append(value)
        if self.country == 'US':
            required_values.append(self.state)
            
        return all(required_values)
    
    ##############
    # Properties #
    ##############
    
    @property
    def address_type(self):
        return self._address_type.title()
    
    @address_type.setter
    def address_type(self, value):
        if value.lower() in ADDRESS_TYPES:
            self._address_type = value.lower()
        else:
            raise ValueError('Address type must be either billing or delivery')
    
    @property
    def surname(self):
        return self._address['Surname']
    
    @surname.setter
    def surname(self, value):
        l = self._length('Surname')
        self._address['Surname'] = value[:l]
        
    @property
    def firstnames(self):
        return self._address['Firstnames']
    
    @firstnames.setter
    def firstnames(self, value):
        l = self._length('Firstnames')
        self._address['Firstnames'] = value[:l]
        
    @property
    def address1(self):
        return self._address['Address1']
    
    @address1.setter
    def address1(self, value):
        l = self._length('Address1')
        self._address['Address1'] = value[:l]
        
    @property
    def address2(self):
        return self._address['Address2']
    
    @address2.setter
    def address2(self, value):
        l = self._length('Address2')
        self._address['Address2'] = value[:l]
        
    @property
    def city(self):
        return self._address['City']
    
    @city.setter
    def city(self, value):
        l = self._length('City')
        self._address['City'] = value[:l]
        
    @property
    def state(self):
        return self._address['State']
    
    @state.setter
    def state(self, value):
        l = self._length('State')
        self._address['State'] = value[:l].upper()
        
    @property
    def postcode(self):
        return self._address['PostCode']
    
    @postcode.setter
    def postcode(self, value):
        l = self._length('PostCode')
        self._address['PostCode'] = value[:l].upper()
        
    @property
    def country(self):
        return self._address['Country']
    
    @country.setter
    def country(self, value):
        l = self._length('Country')
        self._address['Country'] = value[:l].upper()
        
    @property
    def phone(self):
        return self._address['Phone']
    
    @phone.setter
    def phone(self, value):
        l = self._length('Phone')
        self._address['Phone'] = value[:l]
        
    ##################
    # End Properties #
    ##################