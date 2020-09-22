import requests
import getpass
from datetime import datetime
from bs4 import BeautifulSoup

url = "https://warrior.uwaterloo.ca"
now = str(datetime.now())


def get_book_date(now):
    book_date = int(now[8:10]) + 5
    return book_date

def get_book_time(now):
    book_time = (int(now[11:13]))
    if book_time > 12:
        book_time -= 12
    return book_time

def login():
    with requests.session() as login:
        email = input('Enter your UWaterloo email:\n > ')
        password =  getpass.getpass('Enter Password for {}:\n > '.format(email))
        #params needed to verify user access
        params = {
            'returnURL' : '/',
            'isAdmin' : 'false'
        }
        loginPopup = login.get(url + '/Account/GetLoginOptions', data=params) #to get to the login with watIAM popup
        soup = BeautifulSoup(loginPopup.text, 'html.parser') #init beautiful soup
        inputValue = soup.find(id='frmExternalLogin').contents[0]['value'] #scrape for __RequestVerificationToken
        params = {
            '__RequestVerificationToken' : inputValue,
            'provider' : 'Shibboleth',
        }
        popupScrape = login.post(url + '/Account/ExternalLogin?ReturnUrl=%2F', data=params, allow_redirects = True)
        soup = BeautifulSoup(popupScrape.text, 'html.parser')
        postURL = soup.find(id='options')['action'] #scrape for url to Post to
        params = {
            'UserName': email,
            'Password': password,
            'AuthMethod': 'FormsAuthentication'
        }
        res3 = login.post(postURL, data=params, allow_redirects = True)
        soup = BeautifulSoup(res3.text, 'html.parser')
        params = {
            'SAMLResponse': soup.findAll('input')[0]['value'],
            'RelayState': soup.findAll('input')[1]['value'],
        }
        redirectURL = 'https://warrior.uwaterloo.ca:443/Shibboleth.sso/SAML2/POST'
        gymURL = 'https://warrior.uwaterloo.ca/Program/GetProgramDetails?courseId=cc2a16d7-f148-461e-831d-7d4659726dd1&semesterId=b0d461c3-71ea-458e-b150-134678037221'
        login.post(redirectURL, data=params, allow_redirects = True)
        res5 = login.get(gymURL)
        soup = BeautifulSoup(res5.text, 'html.parser')
        print(res5.text)
        #eventURL = soup.find() find unique property of event wanted
        

if __name__ == "__main__":
    login() 