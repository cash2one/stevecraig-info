"""
This contains all the main app settings
"""

class BUTL:
    API = {
        'cookie_secret': 'rofloptimusprime',
        'host_pattern': r'localhost',
        'host_port': '8888'
    }

class TWILIO:
    ACCOUNT = {
        'sid': 'butts',
        'auth_token': 'lmao',
        'number': '+4135962244',
        'split_long_sms': True
    }

class DATABASE:
    MYSQL = {
        'server': 'osto.us',
        'port': 3306,
        'user': 'butl',
        'password': 'dbpass', 
        'schema': 'Hammoocks'
    }
