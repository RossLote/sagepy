transaction_response = (
    'Status=OK\r\n'
    'StatusDetail=Some Other Message\r\n'
    'VPSProtocol=3.00\r\n'
    'AVSCV2=ALL MATCH\r\n'
    'AddressResult=MATCHED\r\n'
    'PostCodeResult=MATCHED\r\n'
    'CV2Result=MATCHED\r\n'
    '3DSecureStatus=OK\r\n'
    'CAVV=76528763987098307838798\r\n'
    'Token=71827364536281726354718273645362817263\r\n'
    'FraudResponse=ACCEPT\r\n'
    'Surcharge=1.00\r\n'
    'ExpiryDate=1115\r\n'
    'BankAuthCode=a6b2c3\r\n'
    'DeclineCode=02\r\n'
    'VPSTxId=71827364536281726354718273645362817263\r\n'
    'SecurityKey=a1b2c3d4e5\r\n'
    'TxAuthNo=1234567890\r\n'
    'MD=\r\n'
)

token_register_response = (
    'Status=OK\r\n'
    'VPSProtocol=3.00\r\n'
    'TxType=TOKEN\r\n'
    'Token=71827364536281726354718273645362817263\r\n'
)

token_register_response_invalid = (
    'Status=INVALID\r\n'
    'VPSProtocol=3.00\r\n'
    'TxType=TOKEN\r\n'
    'Token=71827364536281726354718273645362817263\r\n'
    'StatusDetail=Just a test\r\n'
)

token_register_response_4022 = (
    'Status=INVALID\r\n'
    'VPSProtocol=3.00\r\n'
    'TxType=TOKEN\r\n'
    'Token=71827364536281726354718273645362817263\r\n'
    'StatusDetail=4022\r\n'
)

token_remove_response = (
    'Status=OK\r\n'
    'VPSProtocol=3.00\r\n'
    'StatusDetail=Some Other Message\r\n'
)

release_response = (
    'Status=OK\r\n'
    'VPSProtocol=3.00\r\n'
    'StatusDetail=Some Other Message\r\n'
)

network_error_response = (
    'Status=NETWORKFAIL\r\n'
    'StatusDetail=Network failed connecting to card processor\r\n'
    'VPSProtocol=3.00\r\n'
)