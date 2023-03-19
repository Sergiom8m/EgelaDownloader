import getpass
import os
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
countPDF = 0


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
    # POST /login/index.php HTTP/1.1
    # Host: egela.ehu.eus
    # Cookie: MoodleSessionegela=h9u7hc7tq3td8mjbn69agpi6kerg926r
    # Content-Type: application/x-www-form-urlencoded
    # Content-Length: 78

    # logintoken=osblYrKvsyE9lz3ZHhVAX2CfTZSEbXVf&username=998069&password=Ik452531*
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


def thirdRequest():
    #########################################################################
    # GET /login/index.php?testsession=89877 HTTP/1.1
    # Host: egela.ehu.eus
    # Cookie: MoodleSessionegela=ohej2su7lkmrbbtgknkshi7sk68i91qg

    #########################################################################

    # MAKE THE VARIABLES GLOBAL TO BE ACCESSIBLE FROM EVERYWHERE
    global uriRequest
    global cookie

    # SET THE REQUEST
    method = "GET"
    headers = {'Host': uriRequest.split('/')[2], 'Cookie': cookie}

    # GET REQUEST'S RESPONSE
    response = requests.get(uriRequest, headers=headers, allow_redirects=False)
    code = response.status_code
    description = response.reason
    print("3rd REQUEST'S METHOD AND URI -->" + method + " " + uriRequest)
    print("3rd REQUEST --> " + str(code) + " " + description)

    #CHECK IF LOCATION URI EXISTS OR NOT
    if ('Location' in response.headers) is True:
        uriRequest = response.headers['Location']

    # PRINT THE COOKIE VALUE AND THE URI FOR THE NEXT REQUEST
    print("3rd REQUEST COOKIE --> ", cookie)
    print("URI FOR THE 4th REQUEST --> ", uriRequest)

def fourthRequest():
    #########################################################################
    # GET / HTTP/1.1
    # Host: egela.ehu.eus
    # Cookie: MoodleSessionegela=ohej2su7lkmrbbtgknkshi7sk68i91qg

    #########################################################################

    # MAKE THE VARIABLES GLOBAL TO BE ACCESSIBLE FROM EVERYWHERE
    global uriRequest

    # SET THE REQUEST
    method = "GET"
    headers = {'Host': uriRequest.split('/')[2], 'Cookie': cookie}

    # GET REQUEST'S RESPONSE
    response = requests.get(uriRequest, headers=headers, allow_redirects=False)
    code = response.status_code
    description = response.reason
    print("4th REQUEST'S METHOD AND URI --> " + method + " " + uriRequest)
    print("4th REQUEST --> " + str(code) + " " + description)
    print("4th REQUEST COOKIE --> " + cookie)

    # GET THE RESPONSE CONTENT (HTML)
    html = response.content
    htmlString = str(html)

    # PARSE THE HTML CODE
    soup = BeautifulSoup(html, 'html.parser')

    # ASSURE THE LOGIN DATA IS CORRECT
    if response.status_code == 200 and htmlString.find(nameSurname) != -1:
        print("LOGGED SUCCESSFULLY")

    # else:
        # print("THE LOGIN DATA IS NOT CORRECT! TRY AGAIN...")
        # sys.exit(0)

    # GET THE NAME OF THE USER
    name = soup.find('span', {'class': 'usertext mr-1'})
    print("MY NAME --> " + name.text)

    # GET THE NAMES OF THE SUBJETCS IN EGELA
    rows = soup.find_all('div', {'class': 'info'})

    # ITERATE ROWS TO SEE THE NAMES OF THE DIFFERENT SUBJECTS IN EGELA
    for idx, row in enumerate(rows):
        subject = row.h3.a.text

        # CATCH THE ROW THAT CONTAINS THE SUBJECT "Web Sistemak"
        if (subject == 'Web Sistemak'):
            # GET THE URI THAT REFERS TO "Web Sistemak" SUBJECT
            uriRequest = row.a['href']
            print("SUBJECT --> ", subject)
            print("URI FOR THE 5th REQUEST ", uriRequest)


def fifthRequest():
    # Web Sistema ikasgaiko eskaera egindo da metodo honetan.
    # GET /course/view.php?id=57996 HTTP / 1.1
    # Host: egela.ehu.eus
    # Cookie: MoodleSessionegela = u47586166f8ag046jf14eau8vbhjr1a2

    global uriRequest

    # SET THE REQUEST
    method = 'GET'
    headers = {'Host': uriRequest.split('/')[2], 'Cookie': cookie}

    # GET REQUEST'S RESPONSE
    response = requests.get(uriRequest, headers=headers, allow_redirects=False)
    code = response.status_code
    description = response.reason
    print("5th REQUEST'S METHOD AND URI --> " + method + " " + uriRequest)
    print("5th REQUEST --> " + str(code) + " " + description)
    print("5th REQUEST COOKIE --> " + cookie)

    # GET THE REQUEST CONTENT (HTML)
    html = response.content

    # PARSE THE HTML CODE TO GET ALL THE FILES
    soup = BeautifulSoup(html, 'html.parser')
    links = soup.find_all('img', {'class': 'iconlarge activityicon'})

    # ITERATE ALL THE LINKS TO GET THE PDF LINKS
    for link in links:

        # CHECK IF THE HTML ELEMENT CONTAINS "/PDF"
        if(link['src'].find("/pdf") != -1): # IF NOT FOUND -1
            print("\n A NEW PDF HAS BEEN FOUND")
            pdf_link = link['src']
            uriRequest = link.parent['href'] # GET THE URI OF THE RESOURCE
            print(pdf_link)
            print(uriRequest)
            infoPDF = pdfRequest()
            print("INFO OF THE PDF --> ", infoPDF)
            downloadRequest(infoPDF[0], infoPDF[1])

def pdfRequest():

    global uriRequest

    # CREATE A FOLDER FOR THE DOWNLOADED PDF FILES
    if not os.path.exists("pdf"):
        os.mkdir("pdf")

    # SET THE REQUEST
    method = 'GET'
    headers = {'Host': uriRequest.split('/')[2], 'Cookie': cookie}

    # GET THE REQUEST'S RESPONSE
    response = requests.get(uriRequest, headers=headers, allow_redirects=False)
    code = response.status_code
    description = response.reason
    print("PDF REQUEST'S METHOD AND URI --> " + method + " " + uriRequest)
    print("PDF REQUEST --> " + str(code) + " " + description)
    print("PDF REQUEST COOKIE --> " + cookie)

    # GET THE REQUEST'S CONTENT (HTML)
    html = response.content

    # PARSE THE HTML CODE TO GET THE PDF FILES
    soup = BeautifulSoup(html, 'html.parser')
    pdf = soup.find('div', {'class': 'resourceworkaround'})

    # GET THE NAMES AND THE URI OF THE PDF FILES
    uriPDF = pdf.a['href']
    namePDF = uriPDF.split('/')[-1]
    print("PDF_URI --> ", uriPDF)
    print("PDF_IZENA --> ", namePDF)
    return uriPDF, namePDF

def downloadRequest(uriPDF, namePDF):

    global countPDF

    print(" ---- DOWNLOADING PDF FILE ----")

    # SET THE REQUEST
    method = 'GET'
    headers = {'Host': uriPDF.split('/')[2], 'Cookie': cookie}
    response = requests.get(uriPDF, headers=headers, allow_redirects=False)
    code = response.status_code
    description = response.reason
    print("DOWNLOAD REQUEST METHOD AND URI --> " + method + " " + uriPDF)
    print("DOWNLOAD REQUEST --> " + str(code) + " " + description)
    print("DOWNLOAD REQUEST COOKIE --> " + cookie)

    # SAVE THE PDF CONTENT ON A FILE
    contentPDF = response.content
    file = open("./pdf/" + namePDF, "wb")
    file.write(contentPDF)
    file.close()

    print("----" + namePDF + " HAS BEEN DOWNLOADED ----")

    # UPDATE THE PDF COUNT VARIABLE
    countPDF = countPDF + 1


if __name__ == '__main__':
    print("------------------------------------------------------------")
    data_request()
    print("------------------------------------------------------------")
    firstRequest()
    print("------------------------------------------------------------")
    secondRequest()
    print("------------------------------------------------------------")
    thirdRequest()
    print("------------------------------------------------------------")
    fourthRequest()
    print("------------------------------------------------------------")
    fifthRequest()
    print("------------------------------------------------------------")



