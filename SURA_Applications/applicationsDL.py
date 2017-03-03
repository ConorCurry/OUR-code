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

def get_entries(base_url, form_hash, auth):
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
    return entries

base_url = 'https://pitt.wufoo.com/api/v3/'
with open("API.key", "r") as f:
    user = f.readline().strip()
password = 'notused'
form_hash = 'z6elkqo1ppqp06'
auth = (user, password)

entries = get_entries(base_url, form_hash, auth)

last = len(entries) + 1
processed_students = set()
new_docs = 0
dloaded_file = 'dloaded'
try:
    with open(dloaded_file, 'rb') as handle:
        dloaded = pickle.loads(handle.read())
except FileNotFoundError:
    dloaded = {}
    
#Field3   -> Last name
#Field2   -> First name
#Field20  -> Proposal
#Field444 -> Community Statement
print("Downloading Documents...")
try:
    for e in entries:
        #assert int(e['EntryId']) < last
        #last = int(e['EntryId'])
        name = '{}_{}'.format(e['Field3'].strip(), e['Field2'].strip()).lower()
        name = name.replace(' ', '-')  
        if name == '_':
            #entry wasn't completed
            continue
        if name in processed_students:
            print('Skip Duplicate\tName: {:25}\tentry#: {:5}'.format(name, e['EntryId']))
            continue
        else:       
            processed_students.add(name)
            #remove text cruft from url, and select docs we want downloaded
            url_start_idx = e['Field20'].find('http')
            proposal_url = e['Field20'][url_start_idx : -1]
            url_start_idx = e['Field444'].find('http')
            statement_url = e['Field444'][url_start_idx : -1]
            
            if name not in dloaded or dloaded[name] != e['EntryId']+e['DateUpdated']:
                if proposal_url: 
                    download_doc(name+"-PROPOSAL", "proposals", proposal_url)
                if statement_url:
                    download_doc(name+"-STATEMENT", "statements", statement_url)
                if proposal_url or statement_url:
                    new_docs += 1
                    dloaded[name] = e['EntryId']+e['DateUpdated']
                    print('Saving Documents\tName: {:25}\tentry#: {:5}'.format(name, e['EntryId']))
            else:
                print('Documents Exist\tName: {:25}\tentry#: {:5}'.format(name, e['EntryId']))
except KeyboardInterrupt:
    print("Ending program...")
finally:
    with open(dloaded_file, 'wb') as f:
        pickle.dump(dloaded, f)        
    print('{} Total Submissions'.format(len(processed_students)))
        

