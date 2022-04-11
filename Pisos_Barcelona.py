from bs4 import BeautifulSoup
from urllib.request import urlopen
import os
import csv

# Funció que fa scrapping d'un pis a partir de l'enllaç de l'anunci, i emmagatzema la informació en una llista
def scrappingpis(url, elementList):
    # Llegeix l'enllaç del pis
    html = urlopen(url).read()
    bs = BeautifulSoup(html, 'html.parser')

    # Busca el títol del pis, i si no el troba li assigna el valor "n/a"
    title = bs.find("h1").text
    try:
        barri = bs.find("a", class_="jqVerMapaZonaTooltip link-map-location").text.strip()
    except:
        barri = 'n/a'

    # Busca totes les característiques del pis que hi ha a la web, i les emmagatzema en "features"
    features = bs.findAll("li", class_="feature")
    # Busca els m2 del pis, i si no el troba li assigna el valor "n/a"
    try:
        m2 = features[0].text.split()[0]
    except:
        m2 = 'n/a'
    # Busca les habitacions del pis, i si no el troba li assigna el valor "n/a"
    try:
        habitacions = features[1].text.split()[0]
    except:
        habitacions = 'n/a'
    # Busca els lavabos del pis, i si no el troba li assigna el valor "n/a"
    try:
        lavabos = features[2].text.split()[0]
    except:
        lavabos = 'n/a'
    # Busca el preu/m2 del pis, i si no el troba li assigna el valor "n/a"
    try:
        preum2 = features[3].text.split()[0]
    except:
        preum2 = 'n/a'
    # Busca el preu del pis, i si no el troba li assigna el valor "n/a"
    try:
        preu = features[4].text.split()[0]
    except:
        preu = 'n/a'
    # Busca la immobiliaria del pis, i si no el troba li assigna el valor "n/a"
    try:
        immobiliaria = bs.find("span", class_="title").text
    except:
        immobiliaria = 'n/a'
    # Busca les característiques del pis, i si no les troba li assigna el valor "n/a"
    try:
        Caracteristicas = bs.findAll("article", class_="has-aside")
    except:
        Caracteristicas = 'n/a'

    CaracteristicasGenerales = ''
    # Emmagatzema les diferents característiques generals en un string, separades pel símbol "+"
    # Si no les troba li assigna el valor "n/a"
    try:
        for i in Caracteristicas[2].ul.findAll("li")[0:-1]:
            CaracteristicasGenerales = CaracteristicasGenerales + ' + ' + i.text
    except:
        CaracteristicasGenerales = 'n/a'

    # Emmagatzema els diferents equipaments comunitaris en un string, separades pel símbol "+"
    # Si no els troba li assigna el valor "n/a"
    EquipamientoComunitario = ''
    try:
        for i in Caracteristicas[3].ul.findAll("li"):
            EquipamientoComunitario = EquipamientoComunitario + ' + ' + i.text
            # Busca els 4 apartats del certificat energetic del pis
            CertificadoEnergetico = bs.findAll("div", class_="rating-box")
    except:
        EquipamientoComunitario = 'n/a'

    # Assigna els 4 apartats del certificat energetic del pis a les seves variables corresponents
    # Si no els troba li assigna el valor "n/a"
    try:
        if len(CertificadoEnergetico) == 0:
            ConsumoEtiqueta = 'n/a'
            ConsumokW = 'n/a'
            EmisionesEtiqueta = 'n/a'
            Emisioneskg = 'n/a'
        else:
            ConsumoEtiqueta = CertificadoEnergetico[0].text.split()[1]
            ConsumokW = CertificadoEnergetico[0].text.split()[2]
            EmisionesEtiqueta = CertificadoEnergetico[1].text.split()[1]
            Emisioneskg = CertificadoEnergetico[1].text.split()[2]
    except:
        ConsumoEtiqueta = 'n/a'
        ConsumokW = 'n/a'
        EmisionesEtiqueta = 'n/a'
        Emisioneskg = 'n/a'

    # Busca la data de modificació de l'anunci del pis, i si no la troba li assigna el valor "n/a"
    try:
        ultima_modificació = bs.find("p", class_="time-tag").contents[1].text
    except:
        ultima_modificació = 'n/a'

    # Guarda les característiques del pis i ho genta amb els altres pisos
    pis = [title, barri, m2, habitacions, lavabos, preum2, preu, immobiliaria, CaracteristicasGenerales,
           EquipamientoComunitario, ConsumoEtiqueta, ConsumokW, EmisionesEtiqueta, Emisioneskg, ultima_modificació]
    elementList.append(pis)
    return pis

# Funció que obté els links als diferents anuncis de pisos que hi ha en una pàgina d'habitaclia
def getlinks(url):
    html = urlopen(url).read()
    bs = BeautifulSoup(html, 'html.parser')
    links_pisos = []
    for i in bs.findAll("h3", class_="list-item-title"):
        links_pisos.append(i.a["href"])
    # Quan link_seguent és igual a 0 el script pararà perquè vol dir que s'ha arribat al final
    try:
        link_seguent = bs.find("li", class_="next").a["href"]
    except:
        link_seguent = 0
    return links_pisos, link_seguent

# Funció per guardar les dades extretes en un csv
def writetocsv(filePath, pisLlista):
    with open(filePath, 'w', newline='') as csvFile:
        writer = csv.writer(csvFile)
        for pis in pisLlista:
            writer.writerow(pis)

# Creació de la capçalera del csv
pisLlista = []
headerList=["title", "barri", "m2", "habitacions", "lavabos", "preum2", "preu", "immobiliaria", "CaracteristicasGenerales",
           "EquipamientoComunitario", "ConsumoEtiqueta", "ConsumokW", "EmisionesEtiqueta", "Emisioneskg", "Data anunci"]
pisLlista.append(headerList)

#Current directory where is located the script
currentDir = os.path.dirname(__file__)
filename = "barcelona_pisos_dataset5.csv"
filePath = os.path.join(currentDir, filename)

# Obté els links dels pisos de la primera pàgina, i el link per accedir a la següent pàgina
links_pisos, link_seguent = getlinks("https://www.habitaclia.com/viviendas-barcelona.htm")

# Mentre existeixi una pàgina següent fa scrapping dels pisos i guarda les dades en un csv
while link_seguent != 0:
    for link in links_pisos[0:-1]:
        scrappingpis(link,pisLlista)
    writetocsv(filePath, pisLlista)
    # Quan acaba en una pàgina busca el link de la següent i repeteix el procés
    links_pisos, link_seguent= getlinks(link_seguent)

# Scrapping per la última pàgina, quan link_seguent és igual a 0
for link in links_pisos[0:-1]:
    scrappingpis(link,pisLlista)
    writetocsv(filePath, pisLlista)
