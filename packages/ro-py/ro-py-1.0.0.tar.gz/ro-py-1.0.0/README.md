# Welcome to ro.py
ro.py is a Python wrapper for the Roblox web API.
## Documentation
You can view documentation for ro.py at [ro.py.jmksite.dev](https://ro.py.jmksite.dev/)

## Installation
You can install ro.py from pip:  
```
pip3 install ro-py
```

## Examples
Using the client:
```python
from ro_py.client import Client
client = Client("Token goes here")  # Token is optional, but allows for authentication!
```
Viewing a user's info:
```python
from ro_py.client import Client
client = Client()
user_id = 576059883
user = client.get_user(user_id)
print(f"Username: {user.name}")
print(f"Status: {user.get_status() or 'None.'}")
```
Find more examples in the examples folder.

## Credits
[@iranathan](https://github.com/iranathan) - maintainer
[@jmkdev](https://github.com/iranathan) - maintainer
[@nsg-mfd](https://github.com/nsg-mfd) - helped with endpoints

## Other Libraries
https://github.com/RbxAPI/Pyblox  
https://github.com/iranathan/robloxapi  
