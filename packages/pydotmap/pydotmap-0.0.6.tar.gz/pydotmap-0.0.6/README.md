# pydotmap
[![built with Python3](https://img.shields.io/badge/built%20with-Python3.x-red.svg)](https://www.python.org/)

### This package is just a wrapper to python standard library `dict`. It will allow you to use python dict or dictionary as dot notation just like javascript object. <br><br>

### How to use?
```
from pydotmap import DotMap
from pydotmap import OrderedDotMap


author = DotMap(name="atul", sirname="singh", addr=[{"country": "India"}])
print(author.name)
print(author.sirname)
del author.sirname
print(author.sirname)
print(author.get("sirname", "singh"))  # you can use your default value same as dict
print(author.addr[0].country)


# Ordered Map - This will maintain the order of your dictionary

author = OrderedDotMap(name="atul", sirname="singh", addr=[{"country": "India"}])
print(author)

```
