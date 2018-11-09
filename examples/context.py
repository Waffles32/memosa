
import logging
logging.basicConfig(level=logging.INFO)

import memosa
import requests

get = memosa.memoize1(requests.get)

with memosa.context():

    response = get('http://ipv4.download.thinkbroadband.com/5MB.zip')

    print('same?', response is get('http://ipv4.download.thinkbroadband.com/5MB.zip'))

    with memosa.context():

        print('same?', response is get('http://ipv4.download.thinkbroadband.com/5MB.zip'))

    print('same?', response is get('http://ipv4.download.thinkbroadband.com/5MB.zip'))

print('same?', response is get('http://ipv4.download.thinkbroadband.com/5MB.zip'))
