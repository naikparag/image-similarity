import pandas as pd
data = pd.read_json('test.json')
import requests
import ssl
import os

ssl._create_default_https_context = ssl._create_unverified_context




for index, row in data.iterrows():
    url = row['images']['url'][0]
    print(url)
    filename = 'resources/file'+str(index)+'.jpg'
    try:

        r = requests.get(url, timeout=0.5)

        if r.status_code == 200:
            with open(filename, 'wb') as f:
                f.write(r.content)
    except:
        print(filename+"ERROR")



