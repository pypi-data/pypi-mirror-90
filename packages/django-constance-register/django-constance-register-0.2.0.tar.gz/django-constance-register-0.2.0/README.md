## Constance register - constance for third-party packages

### Features:

* Easily add settings to global constance config from third-party packages or project applications


### How to use it

Install constance and constance register

```bash
>>> pip install django-constance django-constance-register
```

Add constance to `INSTALLED_APPS`

```python
INSTALLED_APPS = (
    ...
    'constance',
    'constance.backends.database',
    'constance_register',
    ...
```

At the end of settings file add 

```python
from constance_register.conf import conf

# Path to your files with configs. 
# NOTE: Files are loaded before apps are ready
CONSTANCE_REGISTRY = [
    'library.apps.shelf',
    'library.apps.staff'
]
# Load settings
conf.load()

# Add third-party settings to global settings
CONSTANCE_CONFIG = {
     'THE_ANSWER': (42, 'Answer to the Ultimate Question of Life, '
                       'The Universe, and Everything'),
    **conf.settings()
}
# Same with fieldsets
CONSTANCE_CONFIG_FIELDSETS = {
    **conf.fieldsets()
}
```

Add your settings to `config.py` file. 
Config file example.

```python
# library.apps.staff.config.py
from datetime import date

app_name = 'staff'

CONFIG = {
    'DATE_ESTABLISHED': (date(1972, 11, 30), "the shop's first opening"),
    'MY_SELECT_KEY': ('yes', 'select yes or no', 'yes_no_null_select'),
    'MULTILINE': ('Line one\nLine two', 'multiline string'),
}

FIELDSET = {
    'General Options': {
        'fields': ('DATE_ESTABLISHED', 'MY_SELECT_KEY'),
        'collapse': True
    },
    'Theme Options': ('MULTILINE',),
}
```
