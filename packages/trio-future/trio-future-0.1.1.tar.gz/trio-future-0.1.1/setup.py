# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['trio_future']

package_data = \
{'': ['*']}

install_requires = \
['trio>=0.17.0,<0.18.0']

setup_kwargs = {
    'name': 'trio-future',
    'version': '0.1.1',
    'description': 'Capture the return values of concurrently executed trio functions',
    'long_description': '# trio-future\n\n## Overview\n\n`trio-future` allows you to capture the return values of concurrently executed trio functions. It\'s an altnerative to using trio channels to communicate results between tasks that feels more like programming with normal functions.\n\nConsider an example with this simple echo function:\n```python\nasync def echo(a: str) -> str:\n    await trio.sleep(0.5)\n    return a\n```\nWe can call our function and get its result back later when we are ready:\n```python\nasync with trio.open_nursery() as nursery:\n    # Call trio_future.run to synchronously get back a Future\n    future = trio_future.run(nursery, echo, "hello")\n    # When we call `await` and yield to scheduler, our function begins executing\n    await trio.sleep(0.1)\n    # We can `await` the function when we are ready\n    hello = await future.get() \n    # hello == "hello"\n```\nA common use-case is to run several tasks concurrently and wait for them all to complete. `trio-future` has a `gather` function like `asyncio.gather` to do this:\n```python\nasync with trio.open_nursery() as nursery:\n    fut_1 = run(nursery, echo, "hello")\n    fut_2 = run(nursery, echo, "world")\n    # Call `gather` to package the two Futures into a single Future object.\n    # Note that this is again a synchronous function.\n    joined_future = gather(nursery, [fut_1, fut_2])\n    # Again, when we `await` the result, we yield to the scheduler. This time, both\n    # of our futures will execute concurrently.\n    hello_world = await join_future.get()\n    # hello_world = ["hello", "world"]\n```\n',
    'author': 'Dan Frank',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/danielhfrank/trio-future',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
