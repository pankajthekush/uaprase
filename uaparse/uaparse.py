import csv
from ua_parser import user_agent_parser
from sqlinsert import UserAgent
from sqlinsert import return_session

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


def parse_ua_csv(in_filename,out_filename):
    csv_out_file = open(out_filename,'w',newline='',encoding='utf-8-sig')
    cwriter = csv.writer(csv_out_file)



    with open(in_filename,'r',newline='',encoding='utf-8-sig') as f:
        creader = csv.reader(f)
        for row in creader:
            csv_data = parse_ua_text(row[0])
            cwriter.writerow(csv_data)
        
        csv_out_file.close()


def insert_to_db(in_file_name):
    session = return_session()


    with open(in_file_name,'r',newline='',encoding='utf-8-sig') as f:
        creader = csv.reader(f)
        for row in creader:
            ua = UserAgent(user_agent = row[0],browser_name =row[1],browser_version= row[2] ,
                            os_name =row[3] ,os_version =row[4] ,device_name= row[5] ,device_brand =row[6] ,
                            device_model=row[7] ,remarks = ''
                         )
            session.merge(ua)

    session.commit()
    session.close()




if __name__ == "__main__":
    #parse_ua_csv('useragentdb.csv','outcsv.csv')
    insert_to_db('outcsv.csv')