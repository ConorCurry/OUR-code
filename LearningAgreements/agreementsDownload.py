#S-17 Script to download learning agreements, using Wufoo API

import requests
import os
import pickle

def download_doc(fn, folder, url):
    _, extension = os.path.splitext(url)
    fn += extension
    fn = os.path.join(folder, fn)
    print(repr(url))
    r = requests.get(url)
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

print("Getting submission entries from Wufoo...")

entry_count = int(requests.get(count_url, auth=auth).json()['EntryCount'])
entries = []
print("\rEntries remaining: {}".format(entry_count))
while (entry_count//100) > 0:
    r = requests.get(entries_url.format(len(entries), 100), auth=auth)
    entries.extend(r.json()['Entries'])
    entry_count -= 100
    print("\rEntries remaining: {}".format(entry_count))
r = requests.get(entries_url.format(len(entries), entry_count%100), auth=auth)
entries.extend(r.json()['Entries'])
entry_count = 0
print("\rEntries remaining: {}".format(entry_count))

entries.reverse()
last = len(entries) + 1
processed_students = set()
download_errors = []
error_file = 'errors.txt'
dloaded_file = 'dloaded.txt'
try:
    with open(dloaded_file, 'rb') as handle:
        dloaded = pickle.loads(handle.read())
except FileNotFoundError:
    dloaded = {}
    
print("Downloading Documents...")
try:
    for e in entries:
        assert int(e['EntryId']) < last
        last = int(e['EntryId'])
        name = '{}_{}'.format(e['Field15'].strip(), e['Field14'].strip()).lower()  
        name = name.replace(' ', '-')  
        if name in processed_students:
            print('Skip Duplicate\tName: {:25}\tentry#: {:5}'.format(name, e['EntryId']))
            continue
        else:       
            processed_students.add(name)
            #remove text cruft from url
            url = e['Field21'].split('(')[1][:-1]
            #try:
            if name not in dloaded or dloaded[name] != e['EntryId']:
                download_doc(name, "downloaded_agreements", url)
                dloaded[name] = e['EntryId']
                print('Saving Document\tName: {:25}\tentry#: {:5}'.format(name, e['EntryId']))
            else:
                print('Document Exists\tName: {:25}\tentry#: {:5}'.format(name, e['EntryId']))
            #except:
            #    download_errors.append(e)
            #    print("ERROR downloading agreement for {}".format(name))
except KeyboardInterrupt:
    print("Ending program...")
finally:
    #with open(error_file, 'w') as f:
    #    for line in download_errors:
    #        f.write(line + '\n')
    with open(dloaded_file, 'wb') as f:
        pickle.dump(dloaded, f)
        
print('{} Attempted Downloads, {} Download Errors.'.format(len(processed_students), len(download_errors)))
print('Check {} for info on failed downloads'.format(error_file))
        

        
    
    




#response = requests.get(entries_url, auth=auth)
#print()

