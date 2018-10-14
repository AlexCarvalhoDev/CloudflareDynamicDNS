import requests

EMAIL   = ""  # your clouflare login email
KEY     = ""  # your cloudflare API key
ZONE_ID = ""  # your DNS zone ID (you can get it in the DNS Overview)
NAME    = ""  # the DNS record full name
TYPE    = ""  # the DNS record type

login_headers = {
    "X-Auth-Email": EMAIL,
    "X-Auth-Key": KEY,
    "Content-Type": "application/json"
    }

server_ip = requests.get('https://api.ipify.org?format=json')
server_ip = server_ip.json()['ip']

print 'Server IP Address: ' + server_ip

cf_ip = requests.get('https://api.cloudflare.com/client/v4/zones/' + ZONE_ID + '/dns_records?type=' + TYPE + '&name=' + NAME,
                     headers=login_headers)
dns_id = cf_ip.json()['result'][0]['id']
cf_ip  = cf_ip.json()['result'][0]['content']


print 'Cloudflare DNS IP Address: ' + cf_ip

data = {
    "type": TYPE,
    "name": NAME,
    "content": server_ip,
    "ttl": 120,
    "proxied": False
}

if server_ip != cf_ip:
    requests.put('https://api.cloudflare.com/client/v4/zones/' + ZONE_ID + '/dns_records/' + dns_id,
                 headers=login_headers,
                 json=data)

new_cf_ip = requests.get('https://api.cloudflare.com/client/v4/zones/' + ZONE_ID + '/dns_records?type=' + TYPE + '&name=' + NAME,
                         headers=login_headers)
new_cf_ip = new_cf_ip.json()['result'][0]['content']

print 'New Cloudflare DNS IP Address: ' + new_cf_ip
