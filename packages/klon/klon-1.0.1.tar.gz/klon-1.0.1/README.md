[![Build Status](https://travis-ci.org/saintamh/klon.svg?branch=master)](https://travis-ci.org/saintamh/klon)
[![PyPI version](https://badge.fury.io/py/klon.svg)](https://pypi.org/project/klon/)

Klon is a collection of utilities for building ElementTrees.

```python
from klon import build_etree

etree = build_etree(
    'html',
    [
        'head',
        ['title', 'Test Document'],
    ],
    [
        'body',
        ['h1#title', 'This is a test'],
        ['img', {'src': 'https://website.com/image'}],
    ]
)
```

Under the hood this just builds the tree using the standard
[xml.etree.ElementTree.Element()](https://docs.python.org/3.7/library/xml.etree.elementtree.html)

If you change the import line instead to this:

```python
from klon.lxml import build_etree
```

then you get a version with the same interface but that builds the tree using `lxml.etree.Element()` instead (note that you don't
need LXML installed if you're not using `klon.lxml`).
