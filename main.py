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
    print("1st REQUEST'S METHOD AND URI --> " + method + " " + uri)
    print("1st REQUEST --> " + str(code) + " " + description)

    # GET THE COOKIE VALUE
    cookie = response.headers['Set-Cookie'].split(';')[0]
    print("1st REQUEST'S COOKIE --> " + cookie)

    # CHECK IF LOCATION URI EXISTS OR NOT
    if ('Location' in response.headers) is False:
        uriRequest = uri

    # PRINT THE URI FOR THE NEXT REQUEST
    print("URI FOR THE 2nd REQUEST --> " + uriRequest)

    # GET THE REQUEST CONTENT (HTML)
    html = response.content

    # PARSE THE HTML CODE TO GET LOGINTOKEN VALUE
    soup = BeautifulSoup(html, 'html.parser')
    token = soup.find('input', {'name': 'logintoken'})

    if token.has_attr('value'):
        loginToken = token['value']
        print("LOGIN TOKEN --> ", loginToken)


def secondRequest():
    #########################################################################
    # GET /login/index.php HTTP / 1.1
    # Host: egela.ehu.eus
    #########################################################################

    # MAKE THE VARIABLES GLOBAL TO BE ACCESSIBLE FROM EVERYWHERE
    global cookie
    global uriRequest  # IT HAS THE VALUE GOTTEN FROM THE LOCATION HEADER AT THE PREVIOUS REQUEST
    global loginToken

    # SET THE REQUEST
    method = "POST"
    headers = {'Host': 'egela.ehu.eus', 'Cookie': cookie, 'Content-Type': 'application/x-www-form-urlencoded'}
    content = {'logintoken': loginToken, 'username': user, 'password': password}
    encoded_content = urllib.parse.urlencode(content)
    headers['Content-Length'] = str(len(encoded_content))


    # GET REQUEST'S RESPONSE
    response = requests.post(uriRequest, headers=headers, data=content, allow_redirects=False)
    code = response.status_code
    description = response.reason
    print("2nd REQUEST'S METHOD AND URI --> " + method + " " + uriRequest)
    print("2nd REQUEST CONTENT --> ", content)
    print("2nd REQUEST --> " + str(code) + " " + description)

    # GET THE NEW COOKIE VALUE
    cookie = response.headers['Set-Cookie'].split(';')[0]
    print("2nd REQUEST COOKIE --> " + cookie)


    # CHECK IF LOCATION URI EXISTS OR NOT
    if ('Location' in response.headers) is True:
        uriRequest = response.headers['Location']

    # PRINT THE URI FOR THE NEXT REQUEST
    print("URI  FOR THE 3rd REQUEST --> " + uriRequest)


if __name__ == '__main__':
    data_request()
    firstRequest()
    secondRequest()
