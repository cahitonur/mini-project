#!usr/bin/env python
import sys
import urllib2
from bs4 import BeautifulSoup


def horoscope(sign):
    url = 'http://my.horoscope.com/astrology/free-daily-horoscope-%s.html' % sign
    html_doc = urllib2.urlopen(url)
    soup = BeautifulSoup(html_doc.read())
    text = soup.find_all(id="textline")[1].get_text()
    date = soup.find_all(id='advert')[1].get_text()
    print "%s - %s\n\n%s" % (sign.capitalize(), date, text)

if __name__ == '__main__':
    try:
        horoscope(sys.argv[1])
    except IndexError:
        print "Please enter a valid zodiac sign.\nUsage example: python horoscope.py taurus"