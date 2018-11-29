
from concurrent.futures import ThreadPoolExecutor, as_completed
import logging
from pprint import pprint

from memosa import memoize1
from memosa.json import context
import requests

logging.basicConfig(level=logging.INFO)

@memoize1
def getTodo(id):
    url = 'https://jsonplaceholder.typicode.com/todos/%s' % id
    return requests.get(url).json()

with context('todos.json'):

    print(getTodo(1))
    print(getTodo(2))

    with ThreadPoolExecutor() as executor:
        for todo in (
            future.result()
            for future in as_completed(
                executor.submit(getTodo, i)
                for i in range(1, 10)
            )
        ):
            pprint(todo)
