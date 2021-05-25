"""
Add the settings to be overriden in the live system

REST_FRAMEWORK.update({'COMPACT_JSON': True})
"""
from ..settings import *  # noqa: F403,F401
from .databases import *  # noqa: F403,F401
