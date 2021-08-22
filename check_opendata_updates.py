import requests
import hashlib

URIS = {
  'details': 'https://stopcovid19.metro.tokyo.lg.jp/data/130001_tokyo_covid19_details_testing_positive_cases.csv',
  'patients': 'https://stopcovid19.metro.tokyo.lg.jp/data/130001_tokyo_covid19_patients.csv'
}

with open('./data_hashes.csv', 'w', newline='') as output:
    print('file,bytes,md5', file=output)

    for key, uri in URIS.items():
        response = requests.get(uri)

        row = [
                key,
                str(len(response.content)),
                hashlib.md5(response.text.encode('utf-8')).hexdigest()
                ]

        print(','.join(row), file=output)
