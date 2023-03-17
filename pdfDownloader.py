import getpass
import signal
import sys
import urllib

import requests
from bs4 import BeautifulSoup
from pip import main

erabiltzailea = ""
izena = ""
pasahitza = ""
cookie = ""
token = ""

def datuakEskatu():
    global erabiltzailea
    global izena
    global pasahitza

    if len(sys.argv) == 3:
        erabiltzailea = sys.argv[1]
        izena = sys.argv[2]
        pasahitza = getpass.getpass("\n-----------------------------------------------------------------------\n"+ izena + " sartu zure pasahitza: ")
    else:
        print("ERROR! Erabilera: python pdfDownloader.py erabiltzailea \"Izena abizena\"")
        exit(0)

def eskaera1():
    global cookie
    global token

    metodoa = 'GET'
    uria = 'https://egela.ehu.eus/login/index.php'
    # Python "hiztegi" baten moduan adierazten dira goiburuak
    goiburua = {'Host': 'egela.ehu.eus'}
    edukia = ''

    # "requests" liburutegia erabiliko dugu HTTP mezuak kudeatzeko
    response = requests.request(metodoa, uria, headers=goiburua, data=edukia,
                                 allow_redirects=False)

    html_fitxategia = response.content
    orria = BeautifulSoup(html_fitxategia, 'html.parser')
    form_zerrenda= orria.find_all('form', {'class':'m-t-1 ehuloginform'})
    formularioa=form_zerrenda[0]
    token_z=formularioa.find_all('input', {'name':'logintoken'})
    token=token_z[0]['value']

    kode = str(response.status_code)
    deskripzio = response.reason
    cookie = response.headers['Set-Cookie'].split(";")[0]
    if int(kode)//100==3: lokazio=response.headers['Location']
    else: lokazio = ""
    printeatuEskaera(metodoa, uria, edukia)
    printeatuErantzuna(kode, deskripzio, cookie, lokazio)



def eskaera2():
    global cookie
    global token
    global pasahitza
    global erabiltzailea

    metodoa = 'POST'
    uria = 'https://egela.ehu.eus/login/index.php'
    # Python "hiztegi" baten moduan adierazten dira goiburuak
    goiburua = {'Host': 'www.ehu.eus', 'Cookie': cookie,
                'Content-Type': 'application/x-www-form-urlencoded'}
    # "requests" liburutegia erabiliko dugu HTTP mezuak kudeatzeko
    edukia = {'logintoken': token, 'username': erabiltzailea, 'password': pasahitza}
    edukia_encoded = urllib.parse.urlencode(edukia)
    goiburua['Content-Length'] = str(len(edukia_encoded))

    response = requests.request(metodoa, uria, headers=goiburua,  params= edukia,
                                allow_redirects=False)  # berbidalketak (host, 30x kodedun erantzunak)

    html_fitxategia = response.content
    orria2 = BeautifulSoup(html_fitxategia, 'html.parser')

    html_edukia = response.content
    orria = BeautifulSoup(html_edukia, 'html.parser')  # Cookie horiek dituen orrialdea aurkitu (log-in orrialdea)
    formulario = orria.find('body').find('form')  # Orrialde horretan dagoen betetzeko formularioa atera
    token = formulario.find('input', {'name': 'logintoken'})['value']
    print(token)

    kode = str(response.status_code)
    deskripzio = response.reason
    if int(kode) // 100 == 3:
        lokazio = response.headers['Location']
    else:
        lokazio = ""
    # printeatuEskaera(metodoa, uria, edukia)
    # printeatuErantzuna(kode, deskripzio, cookie, lokazio)


def eskaera3():
    global pasahitza
    global erabiltzailea
    global cookie
    global token

    metodoa = 'POST'
    uria = 'https://egela.ehu.eus/login/index.php'
    # Python "hiztegi" baten moduan adierazten dira goiburuak
    goiburua = {'Host': 'www.ehu.eus', 'Cookie': cookie, 'Content-Type': 'application/x-www-form-urlencoded'}
    # "requests" liburutegia erabiliko dugu HTTP mezuak kudeatzeko
    edukia = {'logintoken': token, 'username': erabiltzailea, 'password': pasahitza}
    edukia_encoded = urllib.parse.urlencode(edukia)
    goiburua['Content-Length'] = str(len(edukia_encoded))

    response = requests.request(metodoa, uria, headers=goiburua, data=edukia_encoded,
                                allow_redirects=False)  # berbidalketak (host, 30x kodedun erantzunak)

    html_fitxategia = response.content
    orria2 = BeautifulSoup(html_fitxategia, 'html.parser')

    print("ORRIA DA HAU:::::::::::::::::::::::::::::::::::::"+str(response.content))
    kode = str(response.status_code)
    deskripzio = response.reason
    if int(kode) // 100 == 3:
        lokazio = response.headers['Location']
    else:
        lokazio = ""
    # printeatuEskaera(metodoa, uria, edukia)
    # printeatuErantzuna(kode, deskripzio, cookie, lokazio)

    metodoa = 'POST'
    uria = lokazio
    # Python "hiztegi" baten moduan adierazten dira goiburuak
    goiburua = {'Host': 'www.ehu.eus', 'Cookie': cookie, 'Content-Type': 'application/x-www-form-urlencoded'}
    # "requests" liburutegia erabiliko dugu HTTP mezuak kudeatzeko
    edukia = {'logintoken': token, 'username': erabiltzailea, 'password': pasahitza}
    edukia_encoded = urllib.parse.urlencode(edukia)
    goiburua['Content-Length'] = str(len(edukia_encoded))

    response = requests.request(metodoa, uria, headers=goiburua, data=edukia_encoded,
                                allow_redirects=False)  # berbidalketak (host, 30x kodedun erantzunak)

    html_fitxategia = response.content
    orria2 = BeautifulSoup(html_fitxategia, 'html.parser')

    kode = str(response.status_code)
    deskripzio = response.reason
    if int(kode) // 100 == 3:
        lokazio = response.headers['Location']
    else:
        lokazio = ""
    # printeatuEskaera(metodoa, uria, edukia)
    # printeatuErantzuna(kode, deskripzio, cookie, lokazio)


def printeatuEskaera(metodo, uri, edukia):
    print("\n-----------------------------------------------------------------------\n"
          "\nMETODOA: " + metodo +
          "\nURI: " + uri +
          "\nEDUKIA: " + str(edukia))

def printeatuErantzuna(status, deskribapena, cookie, location):
    print("\nESKAERAREN EGOERA: " + status + " " + deskribapena +
          "\nCOOKIE: " + cookie +
          "\nLOCATION: " + location+
          "\nTOKEN: " + token)

if __name__== '__main__':
    datuakEskatu()
    eskaera1()
    eskaera2()
    #eskaera3()