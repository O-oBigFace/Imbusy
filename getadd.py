import os
import requests
import json

serviceurl = 'http://maps.googleapis.com/maps/api/geocode/json'
surl = 'maps.googleapis.com'
purl = '/maps/api/geocode/json'
the_url = surl + purl


path = os.path.join(os.getcwd(), 'org.txt')
result = os.path.join(os.getcwd(), 'result')

proxy_host = "proxy.crawlera.com"
proxy_port = "8010"
proxy_auth = "0b3d10012b61488aa0667b27c829d5de:"

proxies = {
    "http": "socks5://127.0.0.1:1080",
    "https": "socks5://127.0.0.1:1080",
}
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
    res = str(lat) + ' | ' + str(lng) + ' | ' + location + '\n'
    print(res)
    f_res.write(res)
f.close()
f_res.close()