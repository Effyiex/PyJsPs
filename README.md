# PyJsPs

The simplest solution to communication between a Python-Server and a Javascript-Client.

# Dependencies

It relies on Asyncio and the Python Websockets API.

# Implementation

- Clientside: 
```xml 
<script src="https://effyiex.github.io/PyJsPs/pyjsps.js"> </script>
```
- Serverside:
  - https://github.com/Effyiex/PyRequire/releases
  - Add "require.py" to your project 
  - ````python
    from require import require_url     
    pyjsps = require_url("https://effyiex.github.io/PyJsPs/pyjsps.py")
    ````

