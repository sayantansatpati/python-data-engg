__author__ = 'ssatpati'
import glob
import sys
from xml.etree import ElementTree
import json as j
from bs4 import BeautifulSoup
from urllib import urlopen



def xml():
    count = 0
    sum = 0
    for name in glob.glob('xml/*'):
        doc = ElementTree.parse(name)
        for report in doc.getroot().iter('{http://weather.milowski.com/V/APRS/}report'):
        # If the attribute isn't available, we'll get a dictionary key exception
        # so we check for its existence
            if "temperature" in report.attrib:
                count += 1
                sum += int(report.attrib["temperature"])
    print("Average Temp: {0}".format(sum/count))


def json():
    for name in glob.glob('json/*.json'):
        print(name)
        f = open(name)
        with open(name, "r") as f:
            dj = j.loads(str(f.read()))
            for feature in dj["features"]:
                print(feature["geometry"]["coordinates"])

def bs():
    html = urlopen("http://sfbay.craigslist.org/").read()
    soup = BeautifulSoup(html)

    for link in soup.findAll('a'):
        print(link.get('href'))


if __name__ == '__main__':
    bs()
    #xml()
    #json()