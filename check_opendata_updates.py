import requests
import hashlib
import constants

with open('./data_hashes.csv', 'w', newline='') as output:
    print('file,bytes,md5', file=output)

    for key, uri in constants.URIS.items():
        response = requests.get(uri)

        row = [
                key,
                str(len(response.content)),
                hashlib.md5(response.text.encode('utf-8')).hexdigest()
                ]

        print(','.join(row), file=output)
