#!/usr/bin/env python3
# (c) 2020, Matt Martz <matt@sivel.net>
# 3-Clause BSD License (see https://opensource.org/licenses/BSD-3-Clause)

# Make coding more python3-ish
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import codecs
import json
import os
import re
import shutil
import tarfile
import tempfile

from urllib.request import urlopen

from jinja2 import Environment, FileSystemLoader


here = os.path.abspath(os.path.dirname(__file__))
root = os.path.dirname(here)


def read(*parts):
    with codecs.open(os.path.join(here, *parts), 'r') as fp:
        return fp.read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")



def install_jinja2(current_version):
    project_info = json.load(
        urlopen('https://pypi.org/pypi/Jinja2/json')
    )

    version = project_info['info']['version']
    if version == current_version:
        print('%r already installed' % version)
        return
    else:
        print('Upgrading %r to %r' % (current_version, version))

    release_info = project_info['releases'][version]
    for item in release_info:
        if item['filename'].endswith('.tar.gz'):
            url = item['url']
            break

    with tempfile.TemporaryFile() as tmpfile:
        f = urlopen(url)
        shutil.copyfileobj(f, tmpfile)
        tmpfile.seek(0)
        t = tarfile.open(
            mode='r:gz',
            fileobj=tmpfile
        )

        for member in t.getmembers():
            name_parts = member.name.split('/')
            if len(name_parts) < 3:
                continue
            elif name_parts[1] != 'src' or '.egg-info' in member.name:
                continue

            member.name = '/'.join(name_parts[2:])
            t.extract(member, path=os.path.join(root, 'plugins/module_utils'))

    for filename in ('filters.py', 'tests.py'):
        path = os.path.join('plugins/module_utils/jinja2', filename)
        with open(path, 'r+') as f:
            text = f.read()
            text = re.sub(
                'from .runtime import',
                'from jinja2.runtime import',
                text
            )
            text = re.sub(
                'from .exceptions import',
                'from jinja2.exceptions import',
                text
            )
            f.seek(0)
            f.write(text)
            f.truncate()


def main():
    try:
        current_version = find_version(
            root, 'plugins', 'module_utils', 'jinja2', '__init__.py'
        )
    except RuntimeError:
        current_version = None

    install_jinja2(current_version)

    docs_version = '%s.x' % '.'.join(current_version.split('.')[:2])

    e = Environment(loader=FileSystemLoader(root))
    t = e.get_template('README.md.j2')
    out = t.render(version=current_version, docs_version=docs_version)
    with open(os.path.join(root, 'README.md'), 'w+') as f:
        f.write(out)


if __name__ == '__main__':
    main()
