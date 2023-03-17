import getpass
import sys
import urllib

import requests
from bs4 import BeautifulSoup

erabiltzailea = ""
izena = ""
pasahitza = ""
cookie = ""
token = ""
uri= ""
pdfkop=0

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


def irakasgaiaEskatu():
    irakasgaia = input("Sartu bilatzen ari zaren irakasgaiaren izena: ")
    return irakasgaia


def lortuIrakasgaiUri(erantzuna):
    global uri

    orria = BeautifulSoup(erantzuna, 'html.parser')
    kurtso_zerrenda = orria.find_all('a', {'class': 'ehu-visible'})
    aurkitutaWS = False
    irakasgaia = "Web Sistemak"
    #irakasgaia= irakasgaiaEskatu()
    for kurtso in kurtso_zerrenda:
        if irakasgaia.lower() in str(kurtso).lower():
        #if "Web Sistemak" in kurtso:
            uri = kurtso['href']
            aurkitutaWS=True

    if not aurkitutaWS:
        print("EZ DA AURKITU "+irakasgaia+" IRAKASGAIA. Saiatu izen osoa sartzen")
        exit(400)


def eskaera1():
    global token
    global uri

    metodoa = 'GET'
    uri = 'https://egela.ehu.eus/login/index.php'
    # Python "hiztegi" baten moduan adierazten dira goiburuak
    goiburua = {'Host': 'egela.ehu.eus'}
    edukia = ''

    # "requests" liburutegia erabiliko dugu HTTP mezuak kudeatzeko
    response = requests.request(metodoa, uri, headers=goiburua, data=edukia,
                                 allow_redirects=False)

    html_fitxategia = response.content
    orria = BeautifulSoup(html_fitxategia, 'html.parser')
    formularioa= orria.find_all('form', {'class':'m-t-1 ehuloginform'})[0]
    token=formularioa.find_all('input', {'name':'logintoken'})[0]['value']

    printeatuEskaera(metodoa, uri, edukia)
    printeatuErantzuna(response)


def eskaera2():
    global uri
    global cookie

    metodoa = 'POST'
    # Python "hiztegi" baten moduan adierazten dira goiburuak
    goiburua = {'Host': 'egela.ehu.eus', 'Cookie': cookie,
                'Content-Type': 'application/x-www-form-urlencoded'}
    # "requests" liburutegia erabiliko dugu HTTP mezuak kudeatzeko
    edukia = {'logintoken': token, 'username': erabiltzailea, 'password': pasahitza}
    edukia_encoded = urllib.parse.urlencode(edukia)
    goiburua['Content-Length'] = str(len(edukia_encoded))

    response = requests.request(metodoa, uri, headers=goiburua,  data= edukia,
                                allow_redirects=False)  # berbidalketak (host, 30x kodedun erantzunak)

    printeatuEskaera(metodoa, uri, edukia)
    printeatuErantzuna(response)


def eskaera3():
    global uri
    global cookie

    metodoa = 'GET'
    # Python "hiztegi" baten moduan adierazten dira goiburuak
    goiburua = {'Host': 'egela.ehu.eus', 'Cookie': cookie}
    edukia = ''

    # "requests" liburutegia erabiliko dugu HTTP mezuak kudeatzeko
    response = requests.request(metodoa, uri, headers=goiburua, data=edukia,
                                allow_redirects=False)

    printeatuEskaera(metodoa, uri, edukia)
    printeatuErantzuna(response)


def eskaera4():
    global uri
    global cookie

    metodoa = 'GET'
    # Python "hiztegi" baten moduan adierazten dira goiburuak
    goiburua = {'Host': 'egela.ehu.eus', 'Cookie': cookie}
    edukia = ''

    # "requests" liburutegia erabiliko dugu HTTP mezuak kudeatzeko
    response = requests.request(metodoa, uri, headers=goiburua, data=edukia,
                                allow_redirects=False)

    printeatuEskaera(metodoa, uri, edukia)
    printeatuErantzuna(response)

    lortuIrakasgaiUri(response.content)


#--------------------------BEHIN EGELARA SARTUTA-----------------------------
def pdfDeskargatu(link, izena):
    global pdfkop
    global cookie
    print("*************************"+str(pdfkop+1)+" PDF-a deskargatzen*************************")

    metodoa = 'GET'
    goiburua = {'Host': link.split('/')[2], 'Cookie': cookie}
    edukia = ''

    response = requests.request(metodoa, uri, headers=goiburua, data=edukia,
                                allow_redirects=False)

    file = open("./pdf/" + izena, "wb")
    file.write(response.content)
    file.close()

    pdfkop = pdfkop + 1


def eskuratuPDF():
    global uri

    metodoa = 'GET'
    goiburua = {'Host': 'egela.ehu.eus', 'Cookie': cookie}
    edukia = ''

    response = requests.request(metodoa, uri, headers=goiburua, data=edukia,
                                allow_redirects=False)
    orria = BeautifulSoup(response.content, 'html.parser')
    a_zerrenda = orria.find_all('div', {'class': 'resourceworkaround'})
    for a in a_zerrenda:
        link = a.find_all('a')[0]['href']
        izena = link.split('/')[-1]
        pdfDeskargatu(link, izena)


def eskaera5():
    global uri
    global cookie

    metodoa = 'GET'
    goiburua = {'Host': 'egela.ehu.eus', 'Cookie': cookie}
    edukia = ''

    response = requests.request(metodoa, uri, headers=goiburua, data=edukia,
                                allow_redirects=False)
    orria = BeautifulSoup(response.content, 'html.parser')
    link_zerrenda =  orria.find_all('img', {'class': 'iconlarge activityicon'})
    for link in link_zerrenda:
        if '/pdf' in link['src']:
            uri=link.parent['href']
            eskuratuPDF()

def printeatuEskaera(metodo, uri, edukia):
    print("\n-----------------------------------------------------------------------\n"
          "\nMETODOA: " + metodo +
          "\nURI: " + uri +
          "\nEDUKIA: " + str(edukia))


def printeatuErantzuna(response):
    global cookie
    global token
    global uri
    kode = str(response.status_code)
    deskripzio = response.reason
    if int(kode) // 100 == 3:
        lokazio = response.headers['Location']
        uri=lokazio
    else:
        lokazio = ""
    try: c = response.headers['Set-Cookie'].split(";")[0]
    except Exception: c=cookie
    else: cookie=c

    print("\nESKAERAREN EGOERA: " + kode + " " + deskripzio +
          "\nCOOKIE: " + c +
          "\nLOCATION: " + lokazio+
          "\nTOKEN: " + token)

    if izena in str(response.content):
        print("\n\n"
              "SAIOA HASITA "+izena+"!!!!!!!!!!!!!!")


if __name__== '__main__':
    datuakEskatu()
    eskaera1()
    eskaera2()
    eskaera3()
    eskaera4()
    print("\n\n-------------------------PDF-ak deskargatzen...-------------------------")
    eskaera5()
    print("-------------------------PDF-ak deskargatuta!!!-------------------------")