from typing import Dict, List
from functools import reduce
import logging

from django.conf import settings
from django.utils.module_loading import import_string


class Conf():
    def __init__(self):
        self._registry = {}

    def _get_configs(self) -> Dict:
        if not self._registry:
            return {}

        return reduce(lambda a, b: {**a, **b}, [_['settings'] for _ in self._registry.values()])

    def _get_fieldsets(self) -> Dict:
        if not self._registry:
            return {}

        fieldsets = [_['fieldset'] for _ in self._registry.values()]

        return reduce(lambda a, b: {**a, **b}, fieldsets)

    def load(self):
        configs = getattr(settings, 'CONSTANCE_REGISTRY', [])
        config_attributes = [
            'CONFIG', 'app_name', 'FIELDSET'
        ]

        for config in configs:
            attributes = import_attributes(config, config_attributes)
            fieldset = attributes.get('FIELDSET', {})
            config = attributes.get('CONFIG', {})
            app_name = attributes.get('app_name', {})

            if not fieldset:
                fieldset = {app_name: list(config.keys())}

            self._registry[app_name] = {
                'settings': config,
                'fieldset': fieldset
            }

    def settings(self):
        return self._get_configs()

    def fieldsets(self):
        return self._get_fieldsets()


conf = Conf()


def import_attributes(module_path: str, attributes: List[str], config_path: str = 'config'):
    imported = {}

    for attribute in attributes:
        try:
            imported[attribute] = import_string(f'{module_path}.{config_path}.{attribute}')
        except ImportError as e:
            msg = "Could not import '%s.%s' for CONFIG setting '%s'. %s: %s." % (module_path, config_path, attribute, e.__class__.__name__, e)
            logging.warning(msg)

    return imported
