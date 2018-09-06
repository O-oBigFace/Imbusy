import os
import requests
import json

serviceurl = 'http://maps.googleapis.com/maps/api/geocode/json'



path = os.path.join(os.getcwd(), 'org_null.csv')
result = os.path.join(os.getcwd(), 'result')

proxy_host = "proxy.crawlera.com"
proxy_port = "8010"
proxy_auth = "0b3d10012b61488aa0667b27c829d5de:"

proxies = {"https": "https://{}@{}:{}/".format(proxy_auth, proxy_host, proxy_port),
           "http": "http://{}@{}:{}/".format(proxy_auth, proxy_host, proxy_port)}

f = open(path, 'r', encoding='utf-8')
f_res = open(result, 'w', encoding='utf-8')

for eachline in f.readlines():
    payloads = {
        'sensor': 'false',
        'address': eachline,
    }

    c = requests.get(serviceurl, proxies=proxies, params=payloads, verify=False)
    data = c.text

    try:
        js = json.loads(data)
    except:
        js = None
		
    if js is None:
        print('ERROR')
        f_res.write('\n')
        continue
    if 'status' not in js or js['status'] != 'OK':
        print('===Failed To Retrieve===')
        f_res.write('\n')
        continue

    lat = js['results'][0]['geometry']['location']['lat']
    lng = js['results'][0]['geometry']['location']['lng']
    # print('lat:', lat, 'lng:', lng)
    location = js['results'][0]['formatted_address']
    # print(location)
    res =  '\" location \"' + str(lat) + ' | ' + str(lng) + ' | ' + '\n'
    print(res)
    f_res.write(res)
f.close()
f_res.close()