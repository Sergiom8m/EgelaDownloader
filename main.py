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


def firstRequest():
    # ASK FOR INDEX.PHP PAGE
    method = "GET"
    uri = "https://egela.ehu.eus/login/index.php"
    headers = {'Host': 'egela.ehu.eus'}

    print("---------------LEHEN ESKAERA--------------\n")

    print(method + "\n")
    print(uri + "\n")

    print("---------------LEHEN ESKAERAREN ERANTZUNA--------------\n")

    response = requests.request(method, uri, headers=headers, allow_redirects=False)

    code = response.status_code
    description = response.reason
    print("STATUS: " + str(code) + " DESKRIBAPENA: " + description)
    content = response.content

    # GET LOGIN TOKEN VALUE
    document = BeautifulSoup(content, 'html.parser')
    token = document.find('input', {'name': 'logintoken'})
    if token.has_attr('value'):
        logintoken = token["value"]
        print("Logintoken: " + logintoken + "\n")

    # GET THE COOKIE VALUE FROM INDEX.PHP PAGE
    Cookie = response.headers['Set-Cookie'].split(";")[0]
    print("Set-Cookie: " + Cookie + "\n")

    # GET THE URI FOR THE NEXT REQUEST
    if ('Location' in response.headers) is False:
        uriRequest = uri

    print("URI REQUEST ", uriRequest)

def data_request():
    # MAKE THE VARIABLES GLOBAL TO BE ACCESSIBLE FROM EVERYWHERE
    global user
    global password
    global nameSurname

    if len(sys.argv) == 3:
        user = sys.argv[1]
        nameSurname = sys.argv[2].upper()  # CAPITALIZE THE STRING

    else:
        print("ERROR! YOU HAVE INTRODUCED A SINGLE ARGUMENT OR MORE THAN 2 ARGUMENTS")
        print("INTRODUCE 2 ARGUMENTS. FOR EXAMPLE: python.exe nameProgram.py user \"name surname\"")
        sys.exit(0)

    print(user, nameSurname)

    try:
        password = getpass.getpass(prompt='Password: ', stream=None)
    except Exception as error:
        print('ERROR', error)
    else:
        print('Password entered: ', password)


if __name__ == '__main__':
    firstRequest();
    data_request();
