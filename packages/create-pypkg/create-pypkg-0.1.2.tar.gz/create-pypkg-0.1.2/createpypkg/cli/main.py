#!/usr/bin/env python
"""
Python Package Scaffold Builder

Usage:
    create-pypkg -h|--help
    create-pypkg --version
    create-pypkg [--debug|--info] [--module=<name>] <path>

Options:
    -h, --help          Print help and exit
    --version           Print version and exit
    --debug, --info     Execute a command with debug|info messages
    --module=<name>     Specify a module name

Arguments:
    <path>              Path to a directory for a new repository directory
"""

import logging
import os
import re
from pathlib import Path
from pprint import pformat

from docopt import docopt

from .. import __version__
from .util import (fetch_description_from_readme, fetch_git_config, print_log,
                   render_template, set_log_config)


def main():
    args = docopt(__doc__, version=f'create-pypkg {__version__}')
    set_log_config(debug=args['--debug'], info=args['--info'])
    logger = logging.getLogger(__name__)
    logger.debug(f'args:{os.linesep}{args}')
    _create_python_package_scaffold(args=args)


def _create_python_package_scaffold(args, include_package_data=True,
                                    create_dockerfile=True):
    logger = logging.getLogger(__name__)
    repo_dir = Path(args['<path>']).resolve()
    pkg_name = args['--module'] or repo_dir.name
    pkg_dir = repo_dir.joinpath(re.sub(r'[\.\-]', '', pkg_name))
    assert repo_dir.is_dir(), f'No such directory:\t{repo_dir}'
    if pkg_dir.is_dir():
        pass
    else:
        print_log(f'Make a directory:\t{pkg_dir}')
        pkg_dir.mkdir()
    readme_md = repo_dir.joinpath('README.md')
    if readme_md.is_file():
        description = fetch_description_from_readme(md_path=readme_md)
    else:
        description = 'An example package'
        render_template(
            data={'package_name': pkg_name, 'description': description},
            output_path=readme_md
        )
    data = {
        'package_name': pkg_name, 'module_name': pkg_dir.name,
        'include_package_data': str(include_package_data),
        'version': 'v0.0.1', 'description': description,
        **fetch_git_config(repo_dir_path=repo_dir)
    }
    logger.debug(f'data:{os.linesep}' + pformat(data))
    gitignore = repo_dir.joinpath('.gitignore')
    if not gitignore.is_file():
        render_template(output_path=gitignore, template='Python.gitignore')
    dest_files = [
        'setup.py',
        *[(pkg_dir.name + '/' + n) for n in ['__init__.py', 'cli.py']],
        'MANIFEST.in', 'Dockerfile', 'docker-compose.yml'
    ]
    for f in dest_files:
        render_template(output_path=repo_dir.joinpath(f), data=data)
    dockerignore = repo_dir.joinpath('.dockerignore')
    if not dockerignore.is_file():
        print_log(f'Create a symlink:\t{dockerignore}')
        os.symlink('.gitignore', str(dockerignore))
