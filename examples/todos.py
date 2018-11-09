
from concurrent.futures import ThreadPoolExecutor, as_completed
import logging
from pprint import pprint

import memosa
import requests

logging.basicConfig(level=logging.INFO)

@memosa.memoize1
def getTodo(id):
    url = 'https://jsonplaceholder.typicode.com/todos/%s' % id
    return requests.get(url).json()

with memosa.json('todos.json') as context:

    print(getTodo('1'))
    print(getTodo('2'))

    with ThreadPoolExecutor() as executor:
        for todo in (
            future.result()
            for future in as_completed(
                executor.submit(context.run, getTodo, str(i))
                for i in range(1, 10)
            )
        ):
            pprint(todo)
