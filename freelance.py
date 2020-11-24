import requests
from bs4 import BeautifulSoup
import shutil
import logging
import time
import re
import os

station_names = []
bitrate = []
urls = []
genres = []
pls = []
mtu = []

query = input("Search URL: ")


def downloadEntirePage():
    threadse = []
    resp = requests.get(query)  # 'https://www.internet-radio.com/search/?radio=' + query + '#')
    soup = BeautifulSoup(resp.content, 'html.parser')

    for item in soup.find_all('tr'):

        x = item.find(class_='text-danger', attrs={'style': 'display: inline;'})
        station_names.append(x.get_text())

        x = item.find(class_='text-right hidden-xs')
        lines = x.find('p', attrs={'style': 'margin-bottom: 4px;'}).get_text()
        table = lines.splitlines()
        del table[0]
        del table[0]
        string = table[0]
        num = ''.join([n for n in string if n.isdigit()])
        bitrate.append(num)

        x = item.find('a', class_='small text-success')
        if x:
            ret = x.get_text()
        else:
            ret = "No URL Specified."
        urls.append(ret)

        td = item.find(class_='text-danger', attrs={'style': 'display: inline;'})
        td = td.parent
        x = item.find_all('a', attrs={'onclick': True, 'target': False, 'href': True})
        itm = td.get_text().splitlines()

        for i in itm:
            if "Genres" in i:
                tb = i.split()
                del tb[0]
                genres.append(tb)

                break

        x = "https://www.internet-radio.com" + item.find('a', {'title': "PLS Playlist File"})['href']
        pls.append(x)
        x = "https://www.internet-radio.com" + item.find('a', {'title': "M3U Playlist File"})['href']
        mtu.append(x)


# if os.path.exists("radio_output.txt"):
#  os.remove("radio_output.txt")
name = input("Program has completed. File name:")

# input("Program has completed. File name:")
PATH = './' + name + ".txt"
while os.path.isfile(PATH) and os.access(PATH, os.R_OK):
	print("Invalid filename. File already exists.")
	name = input("File name:")
	PATH = './' + name + ".txt"

f = open(name + ".txt", "a")

downloadEntirePage()

for i in range(len(station_names)):
    print("Name: ", station_names[i])
    print("Source URL: ", urls[i])
    print("Streaming URL (.m3u): ", mtu[i])
    print("Streaming URL (.pls): ", pls[i])
    print("Genres: ", end="")
    for item in genres[i]:
        print("%s " % item, end="")
    print("\n-----------------------------------------------------------------\n")

    f.write("Name: " + station_names[i] + "\n")
    f.write(("Source URL: " + urls[i]) + "\n")
    f.write("Streaming URL (.m3u): " + mtu[i] + "\n")
    f.write("Streaming URL (.pls): " + pls[i] + "\n")

    f.write("Genres: ")
    for item in genres[i]:
        f.write("%s " % item)
    f.write("\n\n-----------------------------------------------------------------\n\n")

f.write("\nEnd of Search\n\n\n")

f.close()

wait = input("\nDone! Hit Enter to close the program.")