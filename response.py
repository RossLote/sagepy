class FakeResponse(object):
    def __init__(self, string):
        self._str = string
        
    def read(self):
        return self._str
    
network_error_response = (
    'Status=NETWORKFAIL\r\n'
    'StatusDetail=Network failed connecting to card processor\r\n'
    'VPSProtocol=3.00\r\n'
)

class Response(object):
    """
    Encapsulate a SagePay response
    Response object needs the response string itself and the data (dict) that was originally sent to the gateway.
    """
    
    def __init__(self, response, data):
        self.raw_response = response
        self._response = self._decode_transaction_response(response)
        self.data = data

    def _decode_transaction_response(self, response):
        return dict(line.split('=', 1) for line in response.read().strip().split("\r\n"))

    def get_raw_response(self):
        return self.raw_response
    
    @classmethod
    def get_network_error_response(klass, payload):
        r = klass(FakeResponse(network_error_response), payload)
        return r
    
    @property
    def status(self):
        """
        Gets and returns the status of the response.
        :return: returns status i.e. OK, MALFORMED etc.
        """
        return self._response.get('Status')
    
    @property
    def status_detail(self):
        """
        Gets and returns the message status of the response.
        If the status is not OK, the StatusDetail field will give
        more information about the status.
        :return:
        """
        if self.is_successful():
            return "Status was OK, no details"
        else:
            return self._response['StatusDetail']

    def is_successful(self):
        """
        Confirms if a response was successful.
        :return: boolean True if status OK is found in the response.
        """
        return self.status == 'OK'
    
    def is_network_error(self):
        return self.status == 'NETWORKFAIL'
    
    def is_declined(self):
        return self.status == 'NOTAUTHED'

    def is_rejected(self):
        return self.status == 'REJECTED'
    
    @property
    def protocol(self):
        return self._response.get('VPSProtocol', '3.00')
    
    @property
    def avs_cv2(self):
        return self._response.get('AVSCV2', '')
    
    @property
    def address_result(self):
        return self._response.get('AddressResult', '')
    
    @property
    def postcode_result(self):
        return self._response.get('PostCodeResult', '')
    
    @property
    def cv2_result(self):
        return self._response.get('CV2Result', '')
    
    @property
    def three_d_status(self):
        return self._response.get('3DSecureStatus', '')
    
    @property
    def cavv(self):
        return self._response.get('CAVV', '')
    
    @property
    def token(self):
        return self._response.get('Token')
    
    @property
    def fraud_reponse(self):
        return self._response.get('FraudResponse')
    
    @property
    def surcharge(self):
        return self._response.get('Surcharge')
    
    @property
    def expiry_date(self):
        return self._response.get('ExpiryDate', '')
    
    @property
    def bank_auth_code(self):
        return self._response.get('BankAuthCode')
    
    @property
    def bank_decline_code(self):
        return self._response.get('DeclineCode')
    
    @property
    def vps_tx_id(self):
        """
        VPSTxId, is a unique transaction reference only given if auth was OK.
        :return:
        """
        return self._response.get('VPSTxId', '')
    
    @property
    def security_key(self):
        return self._response.get('SecurityKey', '')
    
    @property
    def vendor_tx_code(self):
        return self.data['VendorTxCode']
    
    @property
    def tx_auth_no(self):
        return self._response.get('TxAuthNo')
    
    @property
    def md(self):
        return self._response.get('MD')
    
    @property
    def acs_url(self):
        return self._response.get('ACSURL')
    
    @property
    def pa_req(self):
        return self._response.get('PAReq')
    
    