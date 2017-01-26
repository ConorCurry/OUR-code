#S-17 Script to download learning agreements, using Wufoo API

import requests

base_url = 'https://pitt.wufoo.com/api/v3/'
with open("API.key", "r") as f:
    user = f.readline().strip()
password = 'notused'
form_hash = 'z1p6grwu02kuwi7'

auth = (user, password)
count_url = base_url+'forms/{}/entries/count.json'.format(form_hash)
entries_url = base_url+'forms/{}/entries.json'.format(form_hash)
entries_url += '?pageStart={}&pageSize={}'

entry_count = int(requests.get(count_url, auth=auth).json()['EntryCount'])
entries = []

while (entry_count//100) > 0:
    r = requests.get(entries_url.format(len(entries), 100), auth=auth)
    entries.extend(r.json()['Entries'])
    entry_count -= 100
    print("Entries remaining: {}".format(entry_count))
r = requests.get(entries_url.format(len(entries), entry_count%100), auth=auth)
entries.extend(r.json()['Entries'])
entry_count = 0

print(len(entries))
    




#response = requests.get(entries_url, auth=auth)
#print()

