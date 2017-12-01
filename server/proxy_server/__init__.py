# -*- coding: utf-8 -*-
import sys

sys.path.append('..')
sys.path.append('../..')
from public.config import Config

config = Config('config.json')

from .app import app
from .models import bind_models
