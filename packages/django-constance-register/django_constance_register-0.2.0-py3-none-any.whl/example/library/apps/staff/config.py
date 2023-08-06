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
