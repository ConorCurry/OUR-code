#S-17 Script to download learning agreements, using Wufoo API

import requests
import os

def download_doc(fn, folder, url):
    _, extension = os.path.splitext(url)
    fn += extension
    fn = os.path.join(folder, fn)
    r = requests.get(url, auth=auth)
    with open(fn, "wb") as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
    return

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
entries.reverse()

last = len(entries) + 1
processed_students = set()
print("Downloading Documents...")
for e in entries:
    assert int(e['EntryId']) < last
    last = int(e['EntryId'])
    name = '{}_{}'.format(e['Field15'].strip(), e['Field14'].strip()).lower()
    
    if name in processed_students:
        print('Skipping duplicate\tName: {}\tentry#: {}'.format(name, e['EntryId']))
        continue
    else:
        print('Saving Document\tName: {}\tentry#: {}'.format(name, e['EntryId']))        
        processed_students.add(name)
        download_doc(name, "downloaded_agreements", e['Field21'])
        

        
    
    




#response = requests.get(entries_url, auth=auth)
#print()

