import getpass
import os
import sys
from pathlib import Path

import urllib
import requests
from bs4 import BeautifulSoup

erabiltzailea = ""
izena = ""
pasahitza = ""
cookie = ""
token = ""
uri= ""
irakasgaiUri = ""
pdfkop=0


#-----------------------------------------HASIERAKO DATUAK-----------------------------------------
def datuakEskatu():
    global erabiltzailea
    global izena
    global pasahitza

    if len(sys.argv) == 3:
        erabiltzailea = sys.argv[1]
        izena = sys.argv[2]
        pasahitza = getpass.getpass("\n-----------------------------------------------------------------------\n"+ izena + " sartu zure eGela-ko pasahitza: ")
    else:
        print("ERROR! Erabilera: python pdfDownloader.py erabiltzailea \"Izena abizena\"")
        exit(0)


def irakasgaiaEskatu():
    irakasgaia = input("Sartu bilatzen ari zaren irakasgaiaren izena: ")
    return irakasgaia


def lortuIrakasgaiUri(erantzuna):
    global uri
    global irakasgaiUri

    orria = BeautifulSoup(erantzuna, 'html.parser')
    kurtso_zerrenda = orria.find_all('a', {'class': 'ehu-visible'})
    aurkitutaWS = False
    irakasgaia = "Web Sistemak"
    #irakasgaia = irakasgaiaEskatu()         #Beste irakasgai baten PDF-ak deskargatu nahi izatekotan

    for kurtso in kurtso_zerrenda:
        if irakasgaia.lower() in str(kurtso).lower():
            uri = kurtso['href']
            irakasgaiUri=uri
            aurkitutaWS = True

    if not aurkitutaWS:
        print("EZ DA AURKITU " + irakasgaia + " IRAKASGAIA. ")
        exit(400)


#-----------------------------------------LOG-IN EGITEKO ESKAERAK-----------------------------------------
def eskaera1():
    global token
    global uri

    metodoa = 'GET'
    uri = 'https://egela.ehu.eus/login/index.php'
    goiburua = {'Host': 'egela.ehu.eus'}
    edukia = ''

    response = requests.request(metodoa, uri, headers=goiburua, data=edukia,
                                 allow_redirects=False)

    html_fitxategia = response.content
    orria = BeautifulSoup(html_fitxategia, 'html.parser')
    formularioa= orria.find_all('form', {'class': 'm-t-1 ehuloginform'})[0]
    token=formularioa.find_all('input', {'name': 'logintoken'})[0]['value']

    printeatuEskaera(metodoa, uri, edukia)
    printeatuErantzuna(response)


def eskaera2():
    global uri
    global cookie

    metodoa = 'POST'
    goiburua = {'Host': 'egela.ehu.eus', 'Cookie': cookie,
                'Content-Type': 'application/x-www-form-urlencoded'}
    edukia = {'logintoken': token, 'username': erabiltzailea, 'password': pasahitza}
    edukia_encoded = urllib.parse.urlencode(edukia)
    goiburua['Content-Length'] = str(len(edukia_encoded))

    response = requests.request(metodoa, uri, headers=goiburua,  data= edukia,
                                allow_redirects=False)  # berbidalketak (host, 30x kodedun erantzunak)

    if(response.headers['Location'].__eq__("https://egela.ehu.eus/login/index.php")):
        print("\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print("Pasahitza ez da egokia, saiatu zaitez berriro")
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n")
        sys.exit(0)

    printeatuEskaera(metodoa, uri, edukia)
    printeatuErantzuna(response)


def eskaera3():
    global uri
    global cookie

    metodoa = 'GET'
    goiburua = {'Host': 'egela.ehu.eus', 'Cookie': cookie}
    edukia = ''

    response = requests.request(metodoa, uri, headers=goiburua, data=edukia,
                                allow_redirects=False)

    printeatuEskaera(metodoa, uri, edukia)
    printeatuErantzuna(response)


def eskaera4():
    global uri
    global cookie

    metodoa = 'GET'
    goiburua = {'Host': 'egela.ehu.eus', 'Cookie': cookie}
    edukia = ''

    response = requests.request(metodoa, uri, headers=goiburua, data=edukia,
                                allow_redirects=False)

    printeatuEskaera(metodoa, uri, edukia)
    printeatuErantzuna(response)

    lortuIrakasgaiUri(response.content)


#-----------------------------------------BEHIN EGELARA SARTUTA-----------------------------------------
def eskaera5():
    global uri
    global cookie
    print("Eskaera 5: "+uri)

    metodoa = 'GET'
    goiburua = {'Host': 'egela.ehu.eus', 'Cookie': cookie}
    edukia = ''

    response = requests.request(metodoa, uri, headers=goiburua, data=edukia,
                                allow_redirects=False)

    orria = BeautifulSoup(response.content, 'html.parser')
    link_zerrenda = orria.find_all('img', {'class': 'iconlarge activityicon'})

    for link in link_zerrenda:
        if '/pdf' in link['src']:
            uri = link.parent['href']
            eskuratuPDF()


def eskuratuPDF():
    global uri
    print("Eskaera eskuratu pdf: "+ uri)

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


def pdfDeskargatu(link, izena):
    global pdfkop
    global cookie
    print("\n*************************" + str(pdfkop+1) + ". PDF-a deskargatzen*************************")
    print("Deskargatzen ari den PDF-aren link-a:\n" + link)

    metodoa = 'GET'
    goiburua = {'Host': link.split('/')[2], 'Cookie': cookie}
    edukia = ''

    response = requests.request(metodoa, link, headers=goiburua, data=edukia,
                                allow_redirects=False)

    file = open("./pdf/" + izena, "wb")
    file.write(response.content)
    file.close()

    pdfkop = pdfkop + 1



#-----------------------------------------CSV SORTU-----------------------------------------
def eskaera6():
    global irakasgaiUri
    global cookie

    print("Eskaera 6: "+irakasgaiUri)



    metodoa = 'GET'
    goiburua = {'Host': 'egela.ehu.eus', 'Cookie': cookie}
    edukia = ''

    response = requests.request(metodoa, irakasgaiUri, headers=goiburua, data=edukia,
                                allow_redirects=False)

    orria = BeautifulSoup(response.content, 'html.parser')
    lab_praktikak = orria.find_all('a', {'class': 'nav-link', 'title':'Laborategiko praktikak'})
    irakasgaiUri = lab_praktikak[0]['href']
    print("Irakasgai uri ------->  "+irakasgaiUri)

def eskaera7():
    global irakasgaiUri
    global cookie
    print("Eskaera 7: "+irakasgaiUri)


    metodoa = 'GET'
    goiburua = {'Host': 'egela.ehu.eus', 'Cookie': cookie}
    edukia = ''

    response = requests.request(metodoa, irakasgaiUri, headers=goiburua, data=edukia,
                                allow_redirects=False)

    orria = BeautifulSoup(response.content, 'html.parser')

    #ADI!!! IRUDIA ALDATZEN BADA KODEA EZ DU FUNTZIONATZEN
    zerrenda = orria.find_all('img', {'src': 'https://egela.ehu.eus/theme/image.php/ehu/assign/1683210168/icon'})

    for z in zerrenda:
        if '/icon' in z['src']:
            irakasgaiUri= z.parent['href']
            eskaera8()

def eskaera8():
    global irakasgaiUri
    global cookie
    print("Eskaera 8: "+irakasgaiUri)

    metodoa = 'GET'
    goiburua = {'Host': 'egela.ehu.eus', 'Cookie': cookie}
    edukia = ''

    response = requests.request(metodoa, irakasgaiUri, headers=goiburua, data=edukia,
                                allow_redirects=False)

    orria = BeautifulSoup(response.content, 'html.parser')
    izena = orria.find('h2')
    data = orria.find('th', string='Entregatze-data').find_next('td')

    csv_path = Path('./csv/Zereginak.csv')
    if csv_path.is_file():
        with open('./csv/Zereginak.csv', 'a') as file:
            file.write("Izena: " + str(izena.contents[0]) + '\n')
            file.write("Entregatze data: " + str(data.contents[0]) + '\n')
            file.write("Esteka: " + irakasgaiUri + '\n\n')
    else:
        with open('./csv/Zereginak.csv', 'w') as file:
            file.write("Izena: " + str(izena.contents[0])+'\n')
            file.write("Entregatze data: " + str(data.contents[0])+'\n')
            file.write("Esteka: " + irakasgaiUri + '\n\n')


#-----------------------------------------PRINT METODOAK-----------------------------------------
def karpetakSortu():
    if not os.path.exists("pdf"):
        os.mkdir("pdf")
    if not os.path.exists("csv"):
        os.mkdir("csv")


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
          "\nLOCATION: " + lokazio)

    if izena in str(response.content):
        print("\n\nSAIOA HASITA "+izena+"!!!")


if __name__== '__main__':
    datuakEskatu()
    print("Login prozesua burutzen:\n")
    eskaera1()
    eskaera2()
    eskaera3()
    eskaera4()
    input("Orrialdeko PDF-ak deskargatzen hasteko enter sakatu:")
    karpetakSortu()
    print("\n\n-------------------------PDF-ak deskargatzen...-------------------------\n")
    eskaera5()
    print("\n-------------------------PDF-ak deskargatuta!!!-------------------------\n")
    print("PDF-ak /pdf karpetan aurkituko dituzu.")
    print("\n---------Irakasgaiak dituen laborategi zereginak gordeko dira CSV batean---------\n")
    eskaera6()
    eskaera7()
    print("\n----------------------------Zereginak.csv sortu da!!!----------------------------\n")

