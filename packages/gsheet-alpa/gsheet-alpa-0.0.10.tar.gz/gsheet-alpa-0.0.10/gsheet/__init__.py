import pkg_resources
__version__ = pkg_resources.get_distribution("gsheet-alpa").version

from .gsheet import *
