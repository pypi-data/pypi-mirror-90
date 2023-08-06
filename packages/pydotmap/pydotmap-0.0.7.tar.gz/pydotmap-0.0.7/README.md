# pydotmap
[![built with Python3](https://img.shields.io/badge/built%20with-Python3.x-red.svg)](https://www.python.org/)

### This package is just a wrapper to python standard library `dict` and `OrderedDict` from python`collections` library with support of pickling and unpickling. It will allow you to use python dict or dictionary as dot notation just like javascript object. <br><br>

### How to initialize?

```
author = DotMap(name="Atul", sirname="Singh")
```

Or

```
from pydotmap import DotMap

author = DotMap()
author.name = "Atul"
author.sirname = "Singh"
```

### How to use?
```
from pydotmap import DotMap
from pydotmap import OrderedDotMap


author = DotMap(name="Atul", sirname="Singh", addr=["country": "India"])
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

### You can pickle it also. How? <br><br>

```
from pydotmap import DotMap
import pickle

author = DotMap(name="Atul")

print(pickle.dumps(author))
```

OUTPUT

```
b'\x80\x04\x952\x00\x00\x00\x00\x00\x00\x00\x8c\x0epydotmap.pymap\x94\x8c\x06DotMap\x94\x93\x94)\x81\x94\x8c\x04name\x94\x8c\x04Atul\x94sh\x03b.'
```
#### you can use OrderedDotMap same way as DotMap to create pickle dump