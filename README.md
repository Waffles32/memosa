# Memosa: Serve cold
==========================

Behold, the power of Memosa:

``` {.sourceCode .python}
from memosa import memoize1
from memosa.json import context
import requests

@memoize1
def getTodo(id):
    url = 'https://jsonplaceholder.typicode.com/todos/%s' % id
    return requests.get(url).json()

with context('todos.json'):    
    print(getTodo(1))
    print(getTodo(2))
```

Features
---------------

-   memoization decorators
-   persistent cache context

Memosa officially supports Python 3.6 & 3.7.

Installation
------------

To install Memosa, simply use pip:

``` {.sourceCode .bash}
$ pip install memosa
```

Documentation
-------------

check out the [examples](https://github.com/Waffles32/memosa/tree/master/examples)
