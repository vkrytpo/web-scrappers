# author ashutosh verma 
# date of creation : 9th feb 2019
# sub dump 240 products descriptions from riverisland.com
import re,os,csv,requests ,urllib.request
from bs4 import BeautifulSoup as bs
#pdp_url
def get_url(page):
    return "https://www.riverisland.com/search?keyword=cloths&f-division=men&pg="+str(page)

pdp_href=[]
i=1
f = open('river_data.csv','w')  
for k in range(1,5):
    c=requests.get(get_url(k)).content
    soup = bs(c ,'html.parser')
    js =soup.find_all("script" ,{'id':'qubitUV'})
    sc_str=js[0].string
    ls =re.split('{' ,sc_str)
    data=[]
    for  i in range( 5 ,5+60):
        remove=['\r' ,'\n' ,' ','}']
        for r in remove:
            ls[i]= ls[i].replace(r ,'')
        data.append(ls[i])
    data_formatted=[]
    sub_data_obj={}
    for i in range(len(data)):
        s_data=data[i].split(',')
        for s in s_data:
            #print(s)
            sub_data = s.split(':' ,1)
            for d in range(len(sub_data)):
                if d%2 ==0 :
                    sub_data_key=sub_data[d]
                if d%2 == 1:
                    sub_data[d]=sub_data[d].replace('"','')
                    sub_data[d]=sub_data[d].replace(']','')
                    sub_data_val= sub_data[d]
                    sub_data_obj[sub_data_key]=sub_data_val
        data_formatted.append(sub_data_obj)
    print('entries dumped :' ,len(data_formatted))
#print(len(data_formatted))
#print(data_formatted)
# dump into csv file 
    for product in data_formatted:
        w = csv.DictWriter(f,product.keys())
        w.writerow(product)
f.close()

print('total 240 entries dumped , please check  river_data.csv file for dump data .')
