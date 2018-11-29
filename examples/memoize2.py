import logging

from memosa import context, memoize2

logging.basicConfig(level=logging.INFO)

@memoize2
def add(x, y):
    yield f'{x}+{y}'
    yield x + y

with context():
    for i in range(3):
        print(add(1, 2))
