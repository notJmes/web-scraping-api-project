import requests
import datetime
import time
from bs4 import BeautifulSoup
import threading
import sys
from html_js_extract import get_html

def getDate(response):

    result = response.content.decode()
    result = result.replace('true', 'True')
    result = result.replace('false', 'False')
    result = eval(result)

    if result['success']:
        result_int = int(result['date'][7:20])
        result = datetime.datetime.fromtimestamp(result_int / 1e3).strftime('%d %B %Y')
        checking = datetime.datetime.fromtimestamp(result_int / 1e3).strftime('%Y'+'%m'.rjust(2,'0')+'%d'.rjust(2,'0'))
        return result, checking

    else:
        print(result)
        return 'Fully booked', '999999999'



def login(client, password, username, gCaptcha=''):

    response = client.get('https://www.drivingcentre.com.sg/User/Login', verify=False)
    if '__RequestVerificationToken' in client.cookies:
        print('CSRF Token is present')
    else:
        print('CSRF token missing')



    soup = BeautifulSoup(response.content, features="lxml")
    s = soup.find('input', {'name':'__RequestVerificationToken'})
    csrf_token = s.get('value')

    if gCaptcha == '':

        sel = get_html('https://www.drivingcentre.com.sg/User/Login')
        soup = BeautifulSoup(sel, features="lxml")
        s = soup.find('input', {'name':'GoogleCaptchaKey'})
        gCaptcha = s.get('value')

    print('Google Captcha:', gCaptcha)
    print('CSRF Token:',csrf_token)

    details = {'__RequestVerificationToken':csrf_token, 'GoogleCaptchaKey':gCaptcha, 'UserName': username, 'Password':password}
    response = client.post('https://www.drivingcentre.com.sg/Account/Login', data=details, headers={'Referer': 'https://www.drivingcentre.com.sg/User/Login'})
    print('User is logged in' if response.url == 'https://www.drivingcentre.com.sg/User/Information' else f'Not logged in; currently in {response.url}')

def main_scanner(client,dict={}, filter='', pwd='', username=''):

    for i in range(2):
        try:
            formdata = {'SlotId':'0',
                        'SelectedSessionNumber':'0',
                        'SellBundleId':'00000000-0000-0000-0000-000000000000',
                        'IsOrientation':'False',
                        'BookingType':'PL',
                        'SelectedLocation':'Location_A'}

            formdata_2 = {'SlotId':'0',
                        'SelectedSessionNumber':'0',
                        'SellBundleId':'00000000-0000-0000-0000-000000000000',
                        'IsOrientation':'False',
                        'BookingType':'PL',
                        'SelectedLocation':'Location_B'}

            verify = [0,0]
            response = client.post('https://www.drivingcentre.com.sg/User/Booking/GetEarliestSlotDate',data=formdata)
            result_WL, verify[0] = getDate(response)
            response = client.post('https://www.drivingcentre.com.sg/User/Booking/GetEarliestSlotDate',data=formdata_2)
            result_AMK, verify[1] = getDate(response)

            if filter != '':
                flag = False
                for date in range(len(verify)):
                    if int(verify[date]) <= int(filter):
                        flag = True
                        if date == 0:
                            dict['W'] = result_WL
                        else:
                            dict['A'] = result_AMK

                dict['F'] = f'Showing results {filter[-2:]}/{filter[-4:-2]}/{filter[0:4]} or earlier'

            else:
                flag = True
                dict['W'] = result_WL
                dict['A'] = result_AMK

            print('\n\nEarliest Slot Status:')
            print('Location_A'.ljust(10,' ')+' -', result_WL)
            print('Location_B'.ljust(10,' ')+' -', result_AMK)
            dict['T'] = datetime.datetime.now().strftime('%H:%M:%S')
            print('Recorded on', dict['T'])
            return flag

        except Exception as e:
            print('Error on line:',sys.exc_info()[2].tb_lineno)
            print(e)
            print(f'Re-login attempt {i+1}')
            login(client, pwd, username)

if __name__ == '__main__':

    pwd = input('Enter the password: ')
    client = requests.Session()
    login(client, pwd, username='788388')
