# -*- coding: utf-8 -*-
import sys

sys.path.append('..')
sys.path.append('../..')
from public.config import Config, concat_config_path

config = Config(concat_config_path(__file__, 'config.json'))

from .app import app
from .models import bind_models
