#crawler for https://www.dillards.com
import re,os,csv,requests ,urllib.request
from bs4 import BeautifulSoup as bs


root_url='https://www.dillards.com'
extra_form ='?facet=dil_shipinternational:Y'
force_extra='&forceFlatResults=forceFlatResults'
home_url=root_url+extra_form


#getting categories
c=requests.get(home_url).content
soup1 = bs(c ,'html.parser')
a_cat= soup1.find_all('a',{'class':'topCatLink'})
root_cat_href=[a['href'] for a in a_cat]


def get_url(cat_href ,page):
    return root_url+cat_href+extra_form+force_extra+'&pageNumber='+str(page)


def get_pdp_href(cat_href):
    count=1
    pdp_href=[]
    total_page=0
    while(total_page == count-1 or count < total_page):
        url=get_url(cat_href ,count)
        c=requests.get(url).content
        soup_cat = bs(c ,'html.parser')
        a_pdp_all=soup_cat.find_all("a")
        if count==1:
            c= requests.get(root_url+cat_href+extra_form+force_extra).content
            soup =bs(c,'html.parser')
            try:
                a_last=soup.find('a',{'class':'pagination__last'})['href']
                total_page=int(a_last.split('=')[-1])
                print('total paginater pages:',total_page)
            except:
                pass
        for a in a_pdp_all:
            try:
                if (str(a['href'])[0] =='/' and a['href'][1] =='p') :
                    pdp_href.append(a['href'])
            except:
                pass
        count= count+1
        print(len(set(pdp_href)))
    pdp_href=list(set(pdp_href))
    print(len(pdp_href) ,'Products Crawled from ,' ,cat_href)

    write_file = "pdp_links.csv"
    with open(write_file, "a") as output:
        for line in pdp_href:
            output.write(line + '\n')



for  href in root_cat_href:
    print('now >>>',href)
    url= get_pdp_href(href)
    
