#!/usr/bin/env python

import logging
import os
import re
import shutil
from configparser import ConfigParser
from pathlib import Path
from pprint import pformat

from jinja2 import Environment, FileSystemLoader


def set_log_config(debug=None, info=None):
    if debug:
        lv = logging.DEBUG
    elif info:
        lv = logging.INFO
    else:
        lv = logging.WARNING
    logging.basicConfig(
        format='%(asctime)s %(levelname)-8s %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S', level=lv
    )


def fetch_description_from_readme(md_path):
    short_description = ''
    with open(md_path, 'r') as f:
        for i, r in enumerate(f):
            if i > 0 and r.strip() and not r.startswith(('#', '=', '-')):
                short_description = r.strip()
                break
    return short_description


def fetch_git_config(repo_dir_path):
    logger = logging.getLogger(__name__)
    local_gitconfig = Path(str(repo_dir_path)).joinpath('.git/config')
    local_cf = (
        _read_config_file(path=local_gitconfig)
        if local_gitconfig.is_file() else dict()
    )
    logger.debug(f'local_cf:\t{os.linesep}' + pformat(local_cf))
    global_gitconfig = Path.home().joinpath('.gitconfig')
    global_cf = (
        _read_config_file(path=global_gitconfig)
        if global_gitconfig.is_file() else dict()
    )
    logger.debug(f'global_cf:\t{os.linesep}' + pformat(global_cf))
    if local_cf.get('user'):
        author = str(local_cf['user'].get('name'))
        author_email = str(local_cf['user'].get('email'))
    elif global_cf.get('user'):
        author = str(global_cf['user'].get('name'))
        author_email = str(global_cf['user'].get('email'))
    else:
        author = ''
        author_email = ''
    if local_cf.get('remote "origin"'):
        git_url = local_cf['remote "origin"'].get('url') or ''
        if git_url.startswith(('https://', 'http://')):
            url = git_url
        elif git_url.startswith('git@github.com:'):
            url = 'https://github.com/{}'.format(git_url.split(':')[1])
        else:
            url = ''
        user_name = re.split(r'[:/]', url)[-2] if url and '/' in url else ''
    else:
        url = ''
        user_name = ''
    return {
        'author': author, 'author_email': author_email, 'url': url,
        'user_name': user_name
    }


def _read_config_file(path, keys=None):
    c = ConfigParser()
    c.read(path)
    return {k: dict(v) for k, v in c.items() if keys is None or k in keys}


def render_template(output_path, data=None, template=None):
    logger = logging.getLogger(__name__)
    target = Path(str(output_path))
    if target.is_file():
        logger.info(f'Skip rendering a file:\t{target}')
    else:
        print_log(f'Render a file:   \t{target}')
        if data is not None:
            with open(target, 'w') as f:
                f.write(
                    Environment(
                        loader=FileSystemLoader(
                            str(Path(__file__).parent.joinpath('../template')),
                            encoding='utf8'
                        )
                    ).get_template(
                        template or f'{target.name}.j2'
                    ).render(data) + os.linesep
                )
        else:
            shutil.copyfile(
                str(
                    Path(__file__).parent.joinpath('../static').joinpath(
                        template or target.name
                    )
                ),
                str(target)
            )


def print_log(message):
    logger = logging.getLogger(__name__)
    logger.info(message)
    print(f'>>\t{message}', flush=True)
