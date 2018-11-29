
import logging
logging.basicConfig(level=logging.INFO)

import memosa
import requests

get = memosa.memoize1(requests.get)

url = 'https://jsonplaceholder.typicode.com/todos/1'

with memosa.context():

    response = get(url)

    # True
    print('same?', response is get(url))

    with memosa.context():
        # False
        print('same?', response is get(url))

    # True
    print('same?', response is get(url))

# False
print('same?', response is get(url))
