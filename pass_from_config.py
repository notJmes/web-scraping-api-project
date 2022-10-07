import configparser

def get_cred():
    parser = configparser.ConfigParser()
    parser.read('cred.config')
    username = parser.get('credentials','username')
    pwd = parser.get('credentials', 'password')
    return username, pwd

def get_token():
    parser = configparser.ConfigParser()
    parser.read('cred.config')
    token = parser.get('discord','token')
    return token
    
def get_captcha():
    parser = configparser.ConfigParser()
    parser.read('cred.config')
    token = parser.get('captcha','token')
    return token	
