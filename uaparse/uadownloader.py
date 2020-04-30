#imports
from slre.slre import RemoteSelenium
import os
from bs4 import BeautifulSoup
from urllib.parse import urlparse,urljoin
from requests import session
import requests
import glob
import random





#start code
def return_file_name(fname,folder_name):
    if os.path.exists(folder_name):
        pass
    else:

        os.mkdir(folder_name)
    r_fname = ''.join(c for c in fname if c.isalnum())
    
    return os.path.join( folder_name, r_fname +'.html')

# rs = RemoteSelenium()
# driver = rs.driver


def scrape_this_page(foldername):
    while True:
        try:
            uinput = input('scrape Y/N ?: ')
            if uinput.upper() =='Y':
                fname = driver.current_url
                pg_source =driver.page_source
                fname = return_file_name(fname,foldername)
                with open(fname,'w',encoding='utf-8') as f:
                    f.write(pg_source)
                break
            elif uinput.upper() == 'N':
                break
        except Exception:
            pass

def parse_main_page():
    html = None
    with open('list_page\httpsdeveloperswhatismybrowsercomuseragentsexplore.html') as f:
        html = f.read()
    
    soup = BeautifulSoup(html,'html.parser')
    all_urls = soup.select('#listing-by-field-name>li>p> a:nth-child(1)')
    base_url = 'https://developers.whatismybrowser.com/useragents/explore/'

    all_return_url = list()
    for url in all_urls:
        furl = urljoin(base_url,url['href'])
        all_return_url.append(furl)
    return all_return_url



def get_category():
    home_category_link = parse_main_page()
    
    for home_url in home_category_link:
        fname = return_file_name(home_url,'category')
        driver.get(home_url)
        r = driver.page_source
        input('continue')

        with open(fname,'w',encoding='utf-8') as f:
            f.write(r.text)

def get_sub_subcat():
    all_files = glob.glob("category\*.html")
    file_data = dict()
    for h_file in all_files:
        with open(h_file,'r',encoding='utf-8') as f:
            soup = BeautifulSoup(f.read(),'html.parser')
            all_category = soup.find_all('a',{'class':'maybe-long'})
            base_url = 'https://developers.whatismybrowser.com/useragents/explore/'

            all_return_url = list()
            for url in all_category:
                furl = urljoin(base_url,url['href'])
                all_return_url.append(furl)
        file_data[h_file] = all_return_url
    return file_data

        

def download_all_pages():
    dict_data =  get_sub_subcat()
    for key,value in dict_data.items():
        folder = key
        for url in value:
            driver.get(url)
            scrape_this_page(key.replace('.html',''))
   
import csv
if __name__ == "__main__":
        
    #download_all_pages()
    dict_data =  get_sub_subcat()
    f = open('out.csv','w',encoding='utf-8',newline='')
    cwriter = csv.writer(f)
    for k,v in dict_data.items():
        for url in v:
            cwriter.writerow([url])
          
        
    f.close()