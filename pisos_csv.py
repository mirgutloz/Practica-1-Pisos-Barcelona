from bs4 import BeautifulSoup
from urllib.request import urlopen
import os
import csv


def scrappingpis(url,elementList):
    html = urlopen(url).read()
    bs = BeautifulSoup(html, 'html.parser')

    title = bs.find("h1").text
    try:
        barri = bs.find("a", class_="jqVerMapaZonaTooltip link-map-location").text.strip()
    except:
        barri = []

    features = bs.findAll("li", class_="feature")
    try:
        m2 = features[0].text.split()[0]
    except:
        m2 = 'n/a'
    try:
        habitacions = features[1].text.split()[0]
    except:
        habitacions = 'n/a'
    try:
        lavabos = features[2].text.split()[0]
    except:
        lavabos = 'n/a'
    try:
        preum2 = features[3].text.split()[0]
    except:
        preum2 = 'n/a'
    try:
        preu = features[4].text.split()[0]
    except:
        preu = 'n/a'
    try:
        immobiliaria = bs.find("span", class_="title").text
    except:
        immobiliaria = 'n/a'
    try:
        Caracteristicas = bs.findAll("article", class_="has-aside")
    except:
        Caracteristicas = 'n/a'

    CaracteristicasGenerales = ''
    try:
        for i in Caracteristicas[2].ul.findAll("li")[0:-1]:
            CaracteristicasGenerales = CaracteristicasGenerales + ' + ' + i.text
    except:
        CaracteristicasGenerales = 'n/a'

    EquipamientoComunitario = ''
    try:
        for i in Caracteristicas[3].ul.findAll("li"):
            EquipamientoComunitario = EquipamientoComunitario + ' + ' + i.text
            CertificadoEnergetico = bs.findAll("div", class_="rating-box")
    except:
        EquipamientoComunitario = 'n/a'

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
    pis = [title, barri, m2, habitacions, lavabos, preum2, preu, immobiliaria, CaracteristicasGenerales,
           EquipamientoComunitario, ConsumoEtiqueta, ConsumokW, EmisionesEtiqueta, Emisioneskg]
    elementList.append(pis)
    return 


def getlinks(url):
    html = urlopen(url).read()
    bs = BeautifulSoup(html, 'html.parser')
    links = []
    for i in bs.findAll("h3", class_="list-item-title"):
        links.append(i.a["href"])
    return links

pisLlista = []
headerList=["title", "barri", "m2", "habitacions", "lavabos", "preum2", "preu", "immobiliaria", "CaracteristicasGenerales",
           "EquipamientoComunitario", "ConsumoEtiqueta", "ConsumokW", "EmisionesEtiqueta", "Emisioneskg"]
pisLlista.append(headerList)

links = getlinks("https://www.habitaclia.com/viviendas-barcelona.htm")
for link in links[0:-1]:
    scrappingpis(link,pisLlista)

#Current directory where is located the script
currentDir = os.path.dirname(__file__)
filename = "barcelona_pisos_dataset.csv"
filePath = os.path.join(currentDir, filename)

with open(filePath, 'w', newline='') as csvFile:
    writer = csv.writer(csvFile)
    for pis in pisLlista:
        writer.writerow(pis)
