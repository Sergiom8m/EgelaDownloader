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

    ## ASK FOR INDEX.PHP PAGE
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

    ## GET THE COOKIE VALUE FROM INDEX.PHP PAGE
    Cookie = response.headers['Set-Cookie'].split(";")[0]
    print("Set-Cookie: " + Cookie + "\n")

    ##
    document = BeautifulSoup(content, 'html.parser')
    token = document.find('input', {'name': 'logintoken'})
    if (token.has_attr('value')):
        logintoken = token["value"]
        print("Logintoken: " + logintoken + "\n")


if __name__ == '__main__':
    firstRequest();
