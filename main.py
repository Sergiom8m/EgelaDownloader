import getpass
import signal
import sys
import urllib

import requests
from bs4 import BeautifulSoup
from pip import main

user = ''
nameSurname = ''
password = ''
cookie = ''
loginToken = ''
uriRequest = ''
pdfcount = 0


def data_request():
    # MAKE THE VARIABLES GLOBAL TO BE ACCESSIBLE FROM EVERYWHERE
    global user
    global password
    global nameSurname

    if len(sys.argv) != 3:
        print("ERROR! YOU HAVE INTRODUCED A SINGLE ARGUMENT OR MORE THAN 2 ARGUMENTS")
        print("INTRODUCE 2 ARGUMENTS. FOR EXAMPLE: python.exe nameProgram.py user \"name surname\"")
        sys.exit(0)

    else:
        user = sys.argv[1]
        nameSurname = sys.argv[2].upper()  # CAPITALIZE THE STRING

    print("ENTERED USER AND NAME --> " + user + ", " + nameSurname);

    try:
        password = getpass.getpass(prompt='PASSWORD: ', stream=None)
    except Exception as error:
        print('ERROR', error)
    else:
        print('PASSWORD ENTERED --> ', password)


def firstRequest():

    #########################################################################
    # GET /login/index.php HTTP / 1.1
    # Host: egela.ehu.eus
    #########################################################################

    # MAKE THE VARIABLES GLOBAL TO BE ACCESSIBLE FROM EVERYWHERE
    global cookie
    global loginToken
    global uriRequest

    # SET THE REQUEST
    method = 'GET'
    uri = "https://egela.ehu.eus/login/index.php"
    headers = {'Host': 'egela.ehu.eus'}

    # GET REQUEST'S RESPONSE
    response = requests.get(uri, headers=headers, allow_redirects=False)
    code = response.status_code
    description = response.reason
    print("1º REQUEST'S METHOD AND URI --> " + method + " " + uri)
    print("1º REQUEST --> " + str(code) + " " + description)

    # GET THE COOKIE VALUE
    cookie = response.headers['Set-Cookie'].split(';')[0]
    print("1º REQUEST'S COOKIE --> " + cookie)

    # CHECK IF LOCATION URI EXISTS OR NOT
    if ('Location' in response.headers) is False:
        uriRequest = uri

    # PRINT THE URI FOR THE NEXT REQUEST
    print("URI REQUEST --> " + uriRequest)

    # GET THE REQUEST CONTENT (HTML)
    html = response.content

    # PARSE THE HTML CODE TO GET LOGINTOKEN VALUE
    soup = BeautifulSoup(html, 'html.parser')
    token = soup.find('input', {'name': 'logintoken'})

    if token.has_attr('value'):
        loginToken = token['value']
        print("LOGIN TOKEN --> ", loginToken)

if __name__ == '__main__':
    data_request();
    firstRequest();
