
__author__    = 'RADICAL-Consulting'
__email__     = 'devel@radical-consulting.com'
__copyright__ = 'Copyright date 2019-2021'
__license__   = 'LGPL.v3 *or* commercial license'


# FIXME: we want atfork imported first, specifically before os and logging

from .tunnel   import Tunnel
from .proxy    import Proxy


# ------------------------------------------------------------------------------
#
import os as            _os
import radical.utils as _ru

_mod_root = _os.path.dirname (__file__)

version_short, version_detail, version_base, \
               version_branch, sdist_name,   \
               sdist_path = _ru.get_version(_mod_root)
version = version_short


# ------------------------------------------------------------------------------

