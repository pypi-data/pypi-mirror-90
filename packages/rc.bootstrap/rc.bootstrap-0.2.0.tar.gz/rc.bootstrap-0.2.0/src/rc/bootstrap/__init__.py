

import os            as _os
import radical.utils as _ru

_mod_root = _os.path.dirname (__file__)

version_short, version_detail, version_base, \
               version_branch, sdist_name,   \
               sdist_path = _ru.get_version(_mod_root)
version = version_short

