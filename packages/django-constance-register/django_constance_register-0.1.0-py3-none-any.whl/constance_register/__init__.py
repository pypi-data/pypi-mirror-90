from .conf import conf
from django.utils.functional import LazyObject

__version__ = '0.1.0'

default_app_config = 'constance_register.apps.ConstanceRegisterConfig'


class LazyConfig(LazyObject):
    def _setup(self):
        from .conf import conf
        self._wrapped = conf.to_settings()[0]

config = LazyConfig()
