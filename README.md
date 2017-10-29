# Requirements:
```
  Python 2.7 or higher
```

# Install requirements
`pip install -r requirements.txt`

# Setup configuration
> open: config/app.py
```
HOST = "0.0.0.0"
DEBUG = True / False
PORT = 8000
```

# RUN
> python start.py
```
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 131-964-042
 * Running on http://127.0.0.1:8000/ (Press CTRL+C to quit)
 ```


# Register blueprint

### flask blueprint documentation

> https://github.com/aiscenblue/flask-blueprint

> docs http://flask-starter-kit.readthedocs.io/en/latest/

`NOTE :: if it's a sub directory it must consist a __init__.py
file to be recognize as a package`

```
from flask import Blueprint, make_response

""" blueprint module for url handler """
method = Blueprint(__name__, __name__)


@method.route("/", methods=['GET'])
def index():
    return make_response("Welcome to flask starter kit!", 200)
      
```

# Configure application core
`configurations are modified in start.py`
> https://github.com/aiscenblue/flask-app-core
