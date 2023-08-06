# h4cktools

[![Build Status](https://travis-ci.com/WhatTheSlime/h4cktools.svg?token=UzY5CygRhRpeZibSxKUz&branch=master)](https://travis-ci.com/WhatTheSlime/h4cktools)
[![codecov](https://codecov.io/gh/WhatTheSlime/h4cktools/branch/master/graph/badge.svg?token=0IZSUXFECQ)](https://codecov.io/gh/WhatTheSlime/h4cktools)
[![PyPI Version](https://img.shields.io/pypi/v/h4cktools.svg)](https://pypi.python.org/pypi/h4cktools/)

## Purpose
h4cktools is a python library containing usefull helpers for penetration testing and security challenges.
It include all python library that can be useful, implements several new functions ond objects and add shorcuts for functions and payloads.

The project is compatible with Windows and Unix based systems.

It is Web Pentest Oriented, it is not inclding [pwntools](https://pypi.org/project/pwntools/) and it does not have not the same purpose.

## Disclaimer
This project is in not intended to be used for illegal purpose and h4cktools developers are in no way responsible for its use etc...

## Summary
- [How to install](#installation)
- [How to Use](#usage)

## Installation
Install from pip
```bash
$ pip install h4cktools
```

Install from github
```bash
$ pip install git+https://github.com/WhatTheSlime/h4cktools.git
```

## Usage
h4cktools library has been developped for be used in a python prompt like [IPython](https://ipython.org/).

To use it just open a python prompt and import all components of the library:
```python
>>> from h4cktools import *
```

## HTTPSession
HTTP library aims to execute HTTP requests and parse its content easily. It overrides [requests library](https://requests.readthedocs.io/en/master/) to be quicker and addapted to pentesting.

### Initialization:
```python
>>> s = HTTPSession()
```

### Navigate into a host
#### Goto

The main feature of HTTPSession is to send get requests by using *goto* method:
```python
>>> s.goto("https://www.google.com")
<[200] http://www.google.com/>
```

HTTP Session works as a browser, when you reach an url the session store the response in *page* attributes:
```python
>>> s.goto("https://www.google.com")
<[200] http://www.google.com/>
>>> s.page
<[200] http://www.google.com/>
```
Page attributes is a requests.Response wrapper that add parsing attributes and methods. (See Response parsing section)

If url contains scheme and domain name, *host* attribute will be set .
When the *host* is set, you can navigate into the host using local path:
```python
>>> s.goto("/webph")
<[200] https://www.google.com/webhp>

>>> s.goto("webph")
<[200] https://www.google.com/webhp>
```

Scope can also be initialize at HTTPSession declaration or set after without doing any requests:
```python
>>> s = HTTPSession("https://www.google.com")

>>> s.host
'https://www.google.com'

>>> s.host = "https://facebook.com"

>>> s.host
'https://facebook.com'

```

Note that redirection following is disable by default. When a response must redirect, you can use *follow* method to go on:
```python
>>> s.goto("https://google.com")
<[301] https://google.com/>

>>> s.follow()
<[200] https://www.google.com/>

```

#### Web tree navigation

*goin* and *goout* methods allow you to navigate in web tree, similar to **cd <Local_Path>** and cd ../ unix commands (but using goin with a paramater starting with a / will not bring you to the url root):
```python
>>> s = HTTPSession("https://www.google.com")

>>> s.goto("search")
<[302] https://www.google.com/search>

>>> s.goin("test") # or s.goin("/test")
<[404] https://www.google.com/search/test>

>>> s.goout()
<[302] https://www.google.com/search>

>>> s.follow()
<[200] https://www.google.com/webhp>

```

To check your current path, simply check the *page* attribute or, if you only want the path, use the page.path attribute:
```python
>>> s.goto("https://www.google.com")
<[200] https://www.google.com/>

>>> s.page
<[200] https://www.google.com/>

>>> s.page.path
'/'

```

#### Historic

HTTPSession keep visited pages as a browser, historic is cached in hist attribute:
```python
>>> s.goto("https://google.com")
<[301] https://google.com/>
>>> s.follow()                                                                                      
<[200] https://www.google.com/>
>>> s.hist                                                    
[<[301] https://google.com/>, <[200] https://www.google.com/>]
```

You can also reach previous and next page using *prev* and *next* methods:
```python
>>> s.goto("https://www.google.com")
<[200] https://www.google.com/>
>>> s.goto("https://www.google.com/webhp")
<[200] https://www.google.com/webhp>
>>> s.prev()
<[200] https://www.google.com/>
>>> s.next()
<[200] https://www.google.com/webhp>
```

### Asynchronous Requests
With this library, it is not possible to call *get* or *post* method like requests library.
In fact, if you try to do it, it will not return send a request and not return a response:
```python
>>> s.get("https://www.google.com")
<Future pending cb=...
```
Return of get method is a prepared request as asyncio Future object.

To send this request you need to call await the task:
```python
>>> await s.get("https://www.google.com")
[<[200] https://www.google.com/>]
```

Or use the *run* method:
```python
>>> s.run(s.get("https://www.google.com"))
[<[200] https://www.google.com/>]
```

Futures object allow you to send requests concurrently:
```python
>>> rqs = [s.get(f"https://www.google.com/{i}") for i in range(1, 5)]
>>> s.run(*rqs)
[<[404] https://google.com/4>,
 <[404] https://google.com/0>,
 <[404] https://google.com/1>,
 <[404] https://google.com/2>,
 <[404] https://google.com/3>]
```

You can define worker number at HTTPSession initialization or after:
```python
>>> s = HTTPSession(workers=5)
>>> s.workers = 5
```

Note that doing requests in this way will note populate the history and set current page of th HTTPSession.

### Responses Parsing
Every requests method of **HTTPSession** will return an **HTTPResponse** object and store it in the **page** attribute:
```python
>>> r = s.goto("search")

>>> s.page
>>> <[302] https://www.google.com/search>
```

The HTTPResponse Object is a wrapper of **requests.Response** object and add new attributes and methods.


## Encoder

## Display
Display library include following functions:
- cat: display all python basic object in form of a string

### cat
Example:
```python
# Lists
>>> cat()
>>> cat()

# Dicts
>>> d = {1: "first", 2: "second"}
1: first
2: second
```

## References
