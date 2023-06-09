import getpass
import os
import signal
import sys
import urllib
from pathlib import Path

import requests
from bs4 import BeautifulSoup
from pip import main

user = ''
nameSurname = ''
password = ''
cookie = ''
loginToken = ''
uriRequest = ''
uriRequestSubmission = ''
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

    # GET THE NEW COOKIE VALUE AND CHECK THE PASSWORD'S VALIDITY
    if (response.headers['Location'] != "https://egela.ehu.eus/login/index.php"):
        cookie = response.headers['Set-Cookie'].split(';')[0]
        print("2nd REQUEST COOKIE --> " + cookie)
    else:
        print("THE PASSWORD IS NOT CORRECT")
        exit(0)

    # CHECK IF LOCATION URI EXISTS OR NOT
    if ('Location' in response.headers) is True:
        uriRequest = response.headers['Location']

    # PRINT THE URI FOR THE NEXT REQUEST
    print("URI FOR THE 3rd REQUEST --> " + uriRequest)


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

    # CHECK IF LOCATION URI EXISTS OR NOT
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
    global uriRequestSubmission

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

    else:
        print("THE LOGIN DATA IS NOT CORRECT! TRY AGAIN...")
        sys.exit(0)

    # GET THE NAME OF THE USER
    name = soup.find('span', {'class': 'usertext mr-1'})
    print("MY NAME --> " + name.text)

    input("PRESS ENTER TO DOWNLOAD PDF FILES")

    # GET THE NAMES OF THE SUBJETCS IN EGELA
    rows = soup.find_all('div', {'class': 'info'})

    # ITERATE ROWS TO SEE THE NAMES OF THE DIFFERENT SUBJECTS IN EGELA
    for idx, row in enumerate(rows):
        subject = row.h3.a.text

        # CATCH THE ROW THAT CONTAINS THE SUBJECT "Web Sistemak"
        if (subject == 'Web Sistemak'):
            # GET THE URI THAT REFERS TO "Web Sistemak" SUBJECT
            uriRequest = row.a['href']
            uriRequestSubmission = uriRequest
            print("SUBJECT --> ", subject)
            print("URI FOR THE 5th REQUEST ", uriRequest)


def fifthRequest():

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
        if (link['src'].find("/pdf") != -1):  # IF NOT FOUND -1
            print("\n A NEW PDF HAS BEEN FOUND")
            pdf_link = link['src']
            uriRequest = link.parent['href']  # GET THE URI OF THE RESOURCE
            infoPDF = pdfRequest()
            downloadPDFRequest(infoPDF[0], infoPDF[1])


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

    # GET THE REQUEST'S CONTENT (HTML)
    html = response.content

    # PARSE THE HTML CODE TO GET THE PDF FILES
    soup = BeautifulSoup(html, 'html.parser')
    pdf = soup.find('div', {'class': 'resourceworkaround'})

    # GET THE NAMES AND THE URI OF THE PDF FILES
    uriPDF = pdf.a['href']
    namePDF = uriPDF.split('/')[-1]
    print("PDF_URI --> ", uriPDF)
    print("PDF_NAME --> ", namePDF)
    return uriPDF, namePDF


def downloadPDFRequest(uriPDF, namePDF):

    global countPDF

    print(" ---- DOWNLOADING PDF FILE ----")

    # SET THE REQUEST
    method = 'GET'
    headers = {'Host': uriPDF.split('/')[2], 'Cookie': cookie}
    response = requests.get(uriPDF, headers=headers, allow_redirects=False)
    code = response.status_code
    description = response.reason

    # SAVE THE PDF CONTENT ON A FILE
    contentPDF = response.content
    file = open("./pdf/" + namePDF, "wb")
    file.write(contentPDF)
    file.close()

    print(" ---- SUCCESSFULLY DOWNLOADED ----")

    # UPDATE THE PDF COUNT VARIABLE
    countPDF = countPDF + 1


def labPageRequest():

    # THIS URI IS TAKEN FROM THE FOURTH REQUEST AD REFERS TO WEB SISTEMAK MAIN PAGE
    global uriRequestSubmission

    # SET THE REQUEST
    method = 'GET'
    headers = {'Host': uriRequestSubmission.split('/')[2], 'Cookie': cookie}

    # GET THE REQUEST'S RESPONSE
    response = requests.get(uriRequestSubmission, headers=headers, allow_redirects=False)
    code = response.status_code
    description = response.reason

    # GET THE REQUEST'S CONTENT (HTML)
    html = response.content

    # PARSE THE HTML CODE TO GET THE LABS PAGE
    soup = BeautifulSoup(html, 'html.parser')
    labs = soup.findAll('a', {'class': 'nav-link', 'title': 'Laborategiko praktikak'})

    # UPDATE uriRequestSubmission WITH THE LABS PAGE
    uriRequestSubmission = labs[0]['href']


def submissionRequest():

    # THIS VARIABLE REFERS TO WEB SISTEMAK/LABORATEGIKO PRAKTIKAK PAGE
    global uriRequestSubmission

    # SET THE REQUEST
    method = 'GET'
    headers = {'Host': uriRequestSubmission.split('/')[2], 'Cookie': cookie}

    # GET THE REQUEST'S RESPONSE
    response = requests.get(uriRequestSubmission, headers=headers, allow_redirects=False)
    code = response.status_code
    description = response.reason

    # GET THE REQUEST'S CONTENT (HTML)
    html = response.content

    # PARSE THE HTML CODE TO GET THE SUBMISSION'S LINKS
    soup = BeautifulSoup(html, 'html.parser')
    links = soup.find_all('img', {'src': 'https://egela.ehu.eus/theme/image.php/ehu/assign/1683210168/icon'})

    for link in links:

        # CHECK IF THE HTML ELEMENT CONTAINS "/ICON"
        if (link['src'].find("/icon") != -1):  # IF NOT FOUND -1
            print("\n A NEW SUBMISSION HAS BEEN FOUND")
            uriRequestSubmission = link.parent['href']  # GET THE URI OF THE RESOURCE
            getSubmissionInfo()


def getSubmissionInfo():

    # THIS VARIABLE REFERS TO ONE SUBMISSION IN THE LABORATEGIKO PRAKTIKAK PAGE
    global uriRequestSubmission

    # SET THE REQUEST
    method = 'GET'
    headers = {'Host': uriRequestSubmission.split('/')[2], 'Cookie': cookie}

    # GET THE REQUEST'S RESPONSE
    response = requests.get(uriRequestSubmission, headers=headers, allow_redirects=False)
    code = response.status_code
    description = response.reason

    # GET THE REQUEST'S CONTENT (HTML)
    html = response.content

    # PARSE THE HTML CODE TO GET THE SUBMISSION INFO
    soup = BeautifulSoup(html, 'html.parser')
    submissionName = soup.find('h2').contents[0]
    print(submissionName)
    submissionDate = soup.find('th', string='Entregatze-data').find_next('td').contents[0]
    createCSV(submissionName, submissionDate, uriRequestSubmission)


def createCSV(submissionName, submissionDate, uriRequestSubmission):

    if not os.path.exists("csv"):
        os.mkdir("csvls"
                 "")

    csv_path = Path('./csv/Submissions.csv')

    if csv_path.is_file():
        with open('./csv/Submissions.csv', 'a') as file:
            file.write("Name: " + str(submissionName) + '\n')
            file.write("Submit date: " + str(submissionDate) + '\n')
            file.write("URI: " + uriRequestSubmission + '\n\n')
    else:
        with open('./csv/Submissions.csv', 'w') as file:
            file.write("Name: " + str(submissionName) + '\n')
            file.write("Submit date: " + str(submissionDate) + '\n')
            file.write("URI: " + uriRequestSubmission + '\n\n')


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
    labPageRequest()
    print("------------------------------------------------------------")
    submissionRequest()
