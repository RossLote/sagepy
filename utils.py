import uuid
import datetime
import calendar
from base64 import b32encode
from urllib import urlencode

TRANSACTION_MODES = (
    'live', 'test'
)

ADDRESS_TYPES = (
    'billing', 'delivery'
)

POSTCODE_COUTRIES = (
    'UK',
)

ADDRESS_FIELDS = (
   #('field',       field length,   required),
    ('Surname',     20,             True),
    ('Firstnames',  20,             True),
    ('Address1',    100,            True),
    ('Address2',    100,            False),
    ('City',        40,             True),
    ('State',       2,              False),
    ('PostCode',    10,             True),
    ('Country',     2,              True),
    ('Phone',       20,             False),
)

SAGEPAY_URL = 'https://{}.sagepay.com/gateway/service/{}.vsp'

TRANSACTION_ENDPOINTS = [
    'abort',
    'authorise',
    'cancel',
    'directrefund',
    'manual',
    'refund',
    'release',
    'repeat',
    'void',
    ''
]

TOKEN_ENDPOINTS = (
    ('remove-token',    'removetoken'),
    ('register-token',  'directtoken'),
    ('use-token',       'vspdirect-register'),
)

THREE_D_ENDPOINTS = (
    ('3d-secure',       'direct3dcallback'),
)


def luhnChecksum(card_number):
    sum = 0
    num_digits = len(card_number)
    oddeven = num_digits & 1

    for count in range(0, num_digits):
        digit = int(card_number[count])
        if not ((count & 1) ^ oddeven):
            digit = digit * 2
        if digit > 9:
            digit = digit - 9
        sum += digit

    return ((sum % 10) == 0)

def build_urls(mode):
    """
    Builds a dictionary of all of the url endpoints at sagepay.
    
    :param mode: 'live' or 'test'
    :type mode: str or unicode
    :param integration_method: 'direct' or 'server'
    
    """
    if not mode in TRANSACTION_MODES:
        raise ValueError(
            'mode must be one of the following: {}'.format(
                ', '.join([s for s in TRANSACTION_MODES])
            )
        )
        
    urls = {}
    for endpoint in TRANSACTION_ENDPOINTS:
        urls[endpoint] = _build_url(mode, endpoint)
    
    urls.update(_build_token_urls(mode))
    urls.update(_build_3d_urls(mode))
    return urls

def _build_url(mode, endpoint):
    """
    
    """
    return SAGEPAY_URL.format(mode, endpoint)

def _build_token_urls(mode):
    urls = {}
    for name, endpoint in TOKEN_ENDPOINTS:
        urls[name] = _build_url(mode, endpoint)
    return urls

def _build_3d_urls(mode):
    urls = {}
    for name, endpoint in THREE_D_ENDPOINTS:
        urls[name] = _build_url(mode, endpoint)
    return urls

def clean_card_number(number):
    number = str(number)
    return number.replace(' ', '')

def get_end_of_month(date):
    last_day_of_month = calendar.monthrange(date.year, date.month)[1]
    return datetime.date(
        date.year,
        date.month,
        last_day_of_month
    )

def expiry_date_valid(date_str):
    if len(date_str) == 4:
        date_str = '01{}'.format(date_str)
    month_start = datetime.datetime.strptime(date_str, '%d%m%y')
    month_end = get_end_of_month(month_start)
    return month_end > datetime.date.today()

def get_new_transaction_id():
    return _generate_transaction_id()

def _generate_transaction_id():
    """
    Generate a new transaction ID
    :return: unique value for each transaction.
    """
    return b32encode(uuid.uuid4().bytes).strip('=').lower()

def _get_expiry_month(month):
    if isinstance(month, str):
        month = int(month)
            
    if month < 1 or month > 12:
        raise ValueError('Month must be of value 1 - 12')
    
    month_str = str(month)
    if month < 10:
        month_str = '0' + month_str
    
    return month_str

def _get_expiry_year(year):
    
    int(year) # must be int parsable, this will raise appropriate exception
    
    return str(year)[-2:]
    
def get_expiry_date(year, month):
    
    month = _get_expiry_month(month)
    year = _get_expiry_year(year)
    
    return '{}{}'.format(month, year)

def convert_date(date):
    """
    SagePay requires date fields to be 4 digits in MMYY (Month Year) format with no separators.
    """
    return datetime.datetime.strptime(str(date), '%Y-%m-%d').strftime('%m%y')

def reverse_convert_date(date):
    return get_end_of_month(datetime.datetime.strptime('01{}'.format(date), '%d%m%y'))

def get_card_type(number):
    """
    Gets credit card type given number. Based on values from Wikipedia page
    "Credit card number".
    http://en.wikipedia.org/w/index.php?title=Credit_card_number
    MC is MasterCard. UKE is Visa Electron. MAESTRO should be used for both UK and International Maestro.
    AMEX, DC (DINERS) and PAYPAL can only be accepted if you have additional merchant accounts with thos
    e acquirers.
    """
    number = str(number)
    #group checking by ascending length of number
    if len(number) == 13:
        if number[0] == "4":
            return "VISA"
    elif len(number) == 15:
        if number[:2] in ("34", "37"):
            return "AMEX"
    elif len(number) == 16:
        if number[:4] == "6011":
            return "DC"
        if number[:2] in ("51", "52", "53", "54", "55"):
            return "MC"
        if number[0] == "4":
            return "VISA"
    return "Unknown"

def encode_transaction_request(data):
    # We're going to mutate this dict so make a copy
    data = data.copy()
    for key in data:
        if not isinstance(data[key], basestring):
            data[key] = unicode(data[key])
        data[key] = data[key].encode('utf8')

    return urlencode(data)




