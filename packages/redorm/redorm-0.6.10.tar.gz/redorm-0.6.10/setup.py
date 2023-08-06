# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['redorm']

package_data = \
{'': ['*']}

install_requires = \
['dataclasses-jsonschema[fast-validation]>=2.13.0,<3.0.0',
 'environs>=9.3.0,<10.0.0',
 'fakeredis>=1.4.5,<2.0.0',
 'redis>=3.5.3,<4.0.0']

setup_kwargs = {
    'name': 'redorm',
    'version': '0.6.10',
    'description': 'A simple redis ORM',
    'long_description': '# RedORM\n\nA simple Redis ORM that only a madman would use in production.  \nThe red in RedORM both means Redis as well as the color red, as red is the fastest colour!\n\n## Quick Start\n\nTo install `pip install redorm`\n\n```python\nfrom dataclasses import dataclass\nfrom redorm import RedormBase, one_to_one, one_to_many, many_to_one, many_to_many\n\n\n@dataclass\nclass Person(RedormBase):\n    name: str\n    age: int\n    siblings = many_to_many(foreign_type="Person", backref="siblings")\n    dad = many_to_one(foreign_type="Person", backref="children")\n    children = one_to_many(foreign_type="Person", backref="dad")\n    favourite_color = one_to_one("Color", backref="liker")\n\n\n@dataclass\nclass Color(RedormBase):\n    name: str\n    liker = one_to_one(Person, backref="favourite_color")\n```\n```python\n>>> red = Color.create(name="Red")\n>>> homer = Person.create(name="Homer", age=50, favourite_color=red)\n>>> print(repr(homer.favourite_color))\nColor(id=\'dcb9aa50-554a-40a5-9acf-7d86c982e5ee\', name=\'Red\')\n>>> print(repr(homer.children))\n[]\n>>> bart = Person.create(name="Bart", age=11, dad=homer)\n>>> print(repr(homer.children))\n[Person(id=\'424cd574-5382-4d34-89da-7233b3928405\', name=\'Bart\', age=11)]\n>>> print(repr(bart.favourite_color))\nNone\n>>> blue = Color.create(name="Blue", liker=bart)\n>>> print(repr(bart.favourite_color))\nColor(id=\'dc9df3c2-c592-4d87-a45e-f88a346342b4\', name=\'Blue\')\n>>> print(repr(blue.liker))\nPerson(id=\'424cd574-5382-4d34-89da-7233b3928405\', name=\'Bart\', age=11)\n>>> lisa = Person.create(name="Lisa", age=9, dad=homer.id, siblings=[bart])\n>>> print(repr(homer.children))\n[Person(id=\'205a459a-572c-41af-bae3-e6e730aada97\', name=\'Lisa\', age=9), Person(id=\'424cd574-5382-4d34-89da-7233b3928405\', name=\'Bart\', age=11)]\n>>> bart.dad = None\n>>> print(repr(homer.children))\n[Person(id=\'205a459a-572c-41af-bae3-e6e730aada97\', name=\'Lisa\', age=9)]\n```\n\n## Why Redorm?\n\n- Thread Safe\n- Very fast\n- Super simple to use\n- Very little boilerplate\n\n# Why not Redorm?\n\n- Made in an afternoon\n- Unlikely to be maintained\n- Not thoroughly tested\n- NOT THOROUGHLY TESTED\n- Writing your own ORM is fantastic for learning, but you should not use it in prod\n',
    'author': 'Jack Adamson',
    'author_email': 'jack@mrfluffybunny.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)
