import re
import urllib

from vendor.BeautifulSoup import BeautifulSoup


URL = "http://www.tasty-babelsberg.de/das-restaurant/wochenkarte/"


soup = BeautifulSoup(urllib.urlopen(URL))

burgerArray = soup.findAll(text=re.compile('[^A-Za-z]burger', re.IGNORECASE))
print burgerArray

burger_element = None
for item in burgerArray:
    if re.search(r'veggie', item, re.IGNORECASE) == None:
        burger_element = item

if(burger_element):
    parent_burger_p = burger_element.findParent(name='p')
    if(parent_burger_p):
        string = ''.join(parent_burger_p.findAll(text=True))
        print unicode(string)
    else:
        print unicode(burger_element)