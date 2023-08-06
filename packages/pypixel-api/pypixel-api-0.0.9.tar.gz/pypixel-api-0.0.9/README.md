# PyPixel

An asynchronous wrapper for the Hypixel API.


## Installing

**Python 3.6 or higher is required**

Once published, you should be able to install with the following command.

```sh
# Linux/macOS
python3 -m pip install -U pypixel-api

# Windows
py -3 -m pip install -U pypixel-api
```

## A quick example
```py
import PyPixel

hypixel = PyPixel.Hypixel(api_key='your Hypixel API key')

player = hypixel.get_player('uuid')
guild = hypixel.get_guild('guild_name', 'name')
```
