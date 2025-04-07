import argparse
import requests
from bs4 import BeautifulSoup
import json
import re


def parse_itemssold(text):
    '''
    Take as input a string and returns the number of items sold, as specified in the string

    >>> parse_itemssold('38 sold')
    38
    >>> parse_itemssold('14 watchers')
    0
    >>> parse_itemssold('Almost gone')
    0
    '''
    numbers = ''
    for characters in text:
        if characters in '1234567890':
            numbers += characters
    if 'sold' in text:
        return int(numbers)
    else:
        return 0


def parse_shipping(tag):
    '''
    >>> parse_shipping('Free delivery')
    0
    >>> parse_shipping('+$8.00 delivery')
    800
    '''
    if 's-item__freeXDays' in tag.get('class',[]):
        return 0
    text = tag.text.strip()
    text_lower = text.lower()
    if "free delivery" in text_lower:
        return 0
    match = re.search(r'\$([\d,]+(?:\.\d{1,2})?)', text)
    if match:
        price_str = match.group(1).replace(',', '')
        if '.' in price_str:
            dollars_str, cents_str = price_str.split('.')
            dollars = int(dollars_str)
            cents = int(cents_str.ljust(2,'0'))
        else: 
            dollars = int(price_str)
            cents = 0
        shipping_cents = dollars * 100 + cents
        return shipping_cents
    return None


def parse_price(text):
    text = text.strip()
    match = re.search(r'\$?\s*([\d,]+(?:\.\d{1,2})?)', text)
    if match:
        price_str = match.group(1).replace(',', '')
        if '.' in price_str:
            dollars_str, cents_str = price_str.split('.')
            dollars = int(dollars_str)
            cents = int(cents_str.ljust(2, '0')[:2])
        else:
            dollars = int(price_str)
            cents = 0
        return dollars * 100 + cents
    return None



parser = argparse.ArgumentParser(description= 'Download information form ebay and convert to JSON.')
parser.add_argument('search_term')
args = parser.parse_args()

print('args.search_term=',args.search_term)

#list of all items found in all ebay webpages
items = []


for page_number in range (1,10):
   #build url
    url = 'https://www.ebay.com/sch/i.html?_nkw=' + args.search_term + '&_sacat=0&_from=R40&_pgn=' + str(page_number)
    print('url=', url)

    #download html
    r = requests.get(url)
    status = r.status_code
    print('status=', status)

    html = r.text

    #process html
    soup = BeautifulSoup(html, 'html.parser')
    
    tags_items = soup.select('.s-item')
    for tag_item in tags_items:

        #name
        tags_name = tag_item.select('.s-item__title')
        name = None
        for tag in tags_name:
            name = tag.text
        
        #price
        price = None
        tags_price = tag_item.select('.s-item__price')
        for tag in tags_price:
            price = parse_price(tag.text)

        #status
        tags_status = tag_item.select('.SECONDARY_INFO')
        status = None
        for tag in tags_status:
            status = tag.text

        #shipping
        shipping = None
        tags_shipping = tag_item.select('.s-item__logisticsCost, .s-item__freeXDays')
        for tag in tags_shipping:
            shipping = parse_shipping(tag)
            if shipping is not None:
                break

        #free returns
        freereturns = False
        tags_freereturns = tag_item.select('.s-item__free-returns')
        for tag in tags_freereturns:
            freereturns = True

        #items sold
        items_sold = None
        tags_itemssold = tag_item.select('.BOLD')
        for tag in tags_itemssold:
            items_sold = parse_itemssold(tag.text)
            #print('tag=',tag)

        

        item = {
            'name':name,
            'price':price,
            'status':status,
            'shipping':shipping,
            'free_returns':freereturns,
            'items_sold':items_sold,
        }
        items.append(item)
    

    print('len(tags_items)=',len(tags_items))
    print('len(items)=',len(items))


filename = args.search_term+'.json'
with open(filename, 'w', encoding='ascii') as f:
    f.write(json.dumps(items))