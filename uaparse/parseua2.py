from ua_parser import user_agent_parser

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


if __name__ == "__main__":
    print(parse_ua_text('Mozilla/5.0 (iPhone; CPU iPhone OS 14_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/87.0.4280.77 Mobile/15E148 Safari/604.1'))
   