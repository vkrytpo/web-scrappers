import re,os,csv,requests ,urllib.request
from bs4 import BeautifulSoup as bs
root_url='https://www.dillards.com'
import signal

def signal_handler(signum, frame):
    raise Exception("Timed out!")

signal.signal(signal.SIGALRM, signal_handler)
signal.alarm(10) #10 sec



def get_pdp_details(pdp_url):
    pdp_url='https://www.dillards.com'+pdp_url
    c=requests.get(pdp_url).content
    soup = bs(c ,'html.parser')
    price_elem= soup.find_all('span',{'class':'price'})
    img_all= soup.find_all('img')
    prod_sku=soup.find('span' ,{'class':'item-number'}).text.replace('Item ','')
    prod_name= soup.find('span',{'class':'product__title--brand m-b-10'}).text
    prod_tags= soup.find('span',{'class':'product__title--desc m-b-10'}).text
    prod_DMS=soup.find('span',{'class':'dept-mic-style'}).text.replace('DMS: ','')
    size_elems=soup.find_all('li',{'class':'available'})
    prod_images=[]
    prod_prices=[]
    prod_sizes=[]
    for size_elem in size_elems:
        prod_sizes.append(size_elem.text)
    for price in price_elem:
        prod_prices.append(price.text)
    for img in img_all:
        if '//dimg.dillards.com/is/image/DillardsZoom/alt' in img['src']:
            url=img['src'].replace('//dimg' ,'https://www')
            url=url.replace('/alt','/main')
            prod_images.append(url)
    ctx= {'Product Name':prod_name 
		,'Product Images':prod_images
		,'Available Sizes':prod_sizes 
		,'Product Tags':prod_tags
	   	,'Product DMS':prod_DMS 
		,'SKU':prod_sku
		,'Prices':prod_prices}
    return ctx

with open('product_details.csv', 'w') as f:  
    header=['Product Name','Product Images','Available Sizes','Product Tags','Product DMS','SKU','Prices']
    w = csv.DictWriter(f, header)
    w.writeheader()

prod_details=[]
for href in open('pdp_links.csv'):
    print('now crawling to : ' ,root_url+str(href))
    try:
        pdp_data=get_pdp_details(str(href))
        with open('product_details.csv', 'a') as f:  
            w = csv.DictWriter(f, pdp_data.keys())
            w.writerow(pdp_data)
    except :
        print( "Timed out!")     
        
