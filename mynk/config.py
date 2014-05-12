# mynk -- a python library for enhancing a user's experience/workspace
# with the foundry's nuke
#
# @author: Robert Moggach <rob@moggach.com>
#
# mynk/config.py -- provides functions for custom user configuration handling: get_config, set_config
#
# mynk is all unicode internally, if you pass in strings,
# they will be explicitly coerced to unicode.
#

import os
import shutil

import nuke
from configobj import ConfigObj

from . import constants as _c
from . import LOG
from .internal import coerce_unicode


class MyNkConfig(object):
  def __init__(self):
    user_cfg_file_path = self.init_cfg()
    self.config = ConfigObj(user_cfg_file_path, indent_type=u'  ')

  def init_cfg(self):
    '''Initialize the user config by copying the provided default config file'''
    default_cfg_path = coerce_unicode(os.path.join(_c.MYNK_PATH, 'data'), _c.MYNK_CHARSET)
    default_cfg_file_path = coerce_unicode(os.path.join(default_cfg_path, 'defaults.cfg'), _c.MYNK_CHARSET)
    user_cfg_path = _c.DOTNUKE_PATH
    user_cfg_file_path = coerce_unicode(os.path.join(user_cfg_path, 'mynk.cfg'), _c.MYNK_CHARSET)
    if not os.path.isdir(user_cfg_path):
      try:
        os.makedirs(user_cfg_path)
        LOG.info("Created initial user config: %s" % user_cfg_file_path)
      except:
        if not os.path.isdir(user_cfg_path):
          raise
    if not os.path.exists(user_cfg_file_path):
      shutil.copy(default_cfg_file_path, user_cfg_file_path)
    return user_cfg_file_path

