from __future__ import unicode_literals

import logging
import os

from mopidy import config, ext


__version__ = '0.2.2'


logger = logging.getLogger(__name__)


class Extension(ext.Extension):

    dist_name = 'Mopidy-RadioNet'
    ext_name = 'radionet'
    version = __version__

    def get_default_config(self):
        conf_file = os.path.join(os.path.dirname(__file__), 'ext.conf')
        return config.read(conf_file)

    def get_config_schema(self):
        schema = super(Extension, self).get_config_schema()
        schema['language'] = config.String()
        schema['min_bitrate'] = config.String()
        schema['favorite_stations'] = config.List()
        return schema

    def setup(self, registry):
        from .backend import RadioNetBackend
        registry.add('backend', RadioNetBackend)
