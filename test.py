import re
import urllib

from vendor.BeautifulSoup import BeautifulSoup


URL = "http://www.tasty-babelsberg.de/das-restaurant/wochenkarte/"


soup = BeautifulSoup(urllib.urlopen(URL))

burgerArray = soup.findAll(text=re.compile('[^A-Za-z]burger', re.IGNORECASE))
print burgerArray

burger = burgerArray[1]
parent_burger_p = burger.findParent(name='p')
string = ''.join(parent_burger_p.findAll(text=True))

print unicode(string)
