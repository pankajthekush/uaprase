import csv
from ua_parser import user_agent_parser
from sqlinsert import UserAgent
from sqlinsert import return_session
import glob
from bs4 import BeautifulSoup
from urllib.parse import urlparse,urljoin


def parse_ua_text(ua_text):
    #parsed_string = user_agent_parser.Parse(ua_text)
    #print(parsed_string)
    browser_data = user_agent_parser.ParseUserAgent(ua_text)
    os_data = user_agent_parser.ParseOS(ua_text)
    device_data = user_agent_parser.ParseDevice(ua_text)
    
    browser_name = str(browser_data['family'])
    browser_version = str(browser_data['major'])
    
    os_name = str(os_data['family'])
    os_version = str(os_data['major'])

    device_name = str(device_data['family'])
    device_brand = str(device_data['brand'])
    device_model  = str(device_data['model'])


    csv_data = [ua_text,browser_name,browser_version,os_name,os_version,device_name,device_brand,device_model]
  
    return csv_data


def parse_ua_csv(out_filename='outcsv.csv',in_filename='uahtml.csv'):

    csv_out_file = open(out_filename,'w',newline='',encoding='utf-8-sig')
    cwriter = csv.writer(csv_out_file)


    with open(in_filename,'r',newline='',encoding='utf-8-sig') as f:
        creader = csv.reader(f)
        for row in creader:
            csv_data = parse_ua_text(row[0])
            polularity = row[1]
            csv_data.append(polularity)
            cwriter.writerow(csv_data)
        
        csv_out_file.close()


def insert_to_db(in_file_name = 'outcsv.csv'):

    session = return_session()
    with open(in_file_name,'r',newline='',encoding='utf-8-sig') as f:
        creader = csv.reader(f)
        for index,row in enumerate(creader):
            
            ua = UserAgent(user_agent = row[0],browser_name =row[1],browser_version= row[2] ,
                            os_name =row[3] ,os_version =row[4] ,device_name= row[5] ,device_brand =row[6] ,
                            device_model=row[7] ,remarks = '',popularity = row[8]
                         )
            session.merge(ua)
            
            if index % 1000 == 0:
                session.commit()
                
        
    session.commit()
    session.close()

def ua_from_html():
    parse_page  = input('parse page too y/n :')

    all_files = glob.glob('*.html')
    f = open('uahtml.csv','w',encoding='utf-8',newline='')
    cwriter = csv.writer(f)
    for fname in all_files:
        with open(fname,'r',encoding='utf-8') as f:
            soup = BeautifulSoup(f.read(),'html.parser')
            all_user_agents = soup.select('.table > tbody > tr')
            for column in all_user_agents:
                user_agent = column.select('td > a')[0].text
                popularity = column.select('td:nth-child(5)')[0].text
                cwriter.writerow([user_agent,popularity])
            
            #get pagination links
            if parse_page.upper() == 'Y':
                gt_pages(soup=soup)
    f.close()
        

def gt_pages(soup:BeautifulSoup):

    f = open('pagination.csv','a',encoding='utf-8',newline='')
    cwrite = csv.writer(f)

    last_page_text = soup.select('#pagination > a')
    if (len(last_page_text) == 0):
        return 0
    else:
        home_link = 'https://developers.whatismybrowser.com/'
        last_url = last_page_text[-1]['href']

        base_page_url = (urljoin(home_link,last_url))[0:-1]

        page_num = last_page_text[-1].text
        lst_page = ''.join(chr for chr in page_num if chr.isnumeric() )
        lst_page = int(lst_page.strip())

        for n in range(lst_page,1,-1):
            page_url = urljoin(base_page_url,str(n))
            cwrite.writerow([page_url])

    f.close()

def parse_upload():
    ua_from_html()
    parse_ua_csv()
    insert_to_db()

if __name__ == "__main__":
    insert_to_db()
   