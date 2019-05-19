#!/usr/bin/env python
from datetime import datetime as dt
from bs4 import BeautifulSoup
from requests import get

class Scraper():
    def __init__(self, url):
        self.url = url
        
    def __check_response(self, rsp):
        contentType = rsp.headers['Content-Type'].lower()
        return (
            rsp.status_code == 200
            and contentType is not None
            and contentType.find('html') > -1
        )
    
    def get_html(self):
        try:
            with get(self.url, stream=True) as rsp:
                if self.__check_response(rsp):
                    return rsp.content
        except Exception as e:
            print(e)
        return False

    def parse_html(self, html):
        return BeautifulSoup(html, 'html.parser')

def main():
    s = Scraper('https://www.nasdaq.com/symbol/bynd')
    page = s.get_html()
    
    if page:
        soup = s.parse_html(page)
        stock, price = '', ''
        for div in soup.select('div'):
            try:
                if 'symbol' in div['class'][0]:
                    stock = div.text.strip()
                elif 'dollar' in div['class'][0]:
                    price = div.text.strip()
                if stock and price:
                    break
            except:
                continue
        print('%s: %s' % (stock, price))


if __name__ == '__main__':
    s = dt.now()
    main()
    print('Time elapsed: %s' % (dt.now() - s))
