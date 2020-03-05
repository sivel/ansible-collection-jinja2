# (c) 2020, Matt Martz <matt@sivel.net>
# 3-Clause BSD License (see https://opensource.org/licenses/BSD-3-Clause)

# Make coding more python3-ish
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


from ansible_collections.sivel.jinja2.plugins.module_utils.jinja2.filters import FILTERS


class FilterModule:
    def filters(self):
        return FILTERS.copy()
