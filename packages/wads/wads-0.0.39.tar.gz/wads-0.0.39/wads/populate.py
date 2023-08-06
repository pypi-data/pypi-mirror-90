import os
import shutil
import json
from collections import ChainMap

# from functools import partial
from typing import List, Optional
from wads import pkg_path_names, root_dir, wads_configs, wads_configs_file
from wads import pkg_join as wads_join
from wads.util import mk_conditional_logger
from wads.pack import write_configs
from wads.licensing import license_body

# from wads.pack_util import write_configs

path_sep = os.path.sep

populate_dflts = wads_configs.get(
    'populate_dflts',
    {
        'description': "There's a bit of an air of mystery around this project...",
        'root_url': None,
        'author': None,
        'license': 'mit',
        'description_file': 'README.md',
        'long_description': 'file:README.md',
        'long_description_content_type': 'text/markdown',
        'keywords': None,
        'install_requires': None,
        'verbose': True,
    },
)


def gen_readme_text(
    name, text="There's a bit of an air of mystery around this project..."
):
    return f'''
# {name}
{text}
'''


# TODO: Add a `defaults_from` in **configs that allows one to have several named defaults in wads_configs_file
def populate_pkg_dir(
    pkg_dir,
    description: str = populate_dflts['description'],
    root_url: Optional[str] = populate_dflts['root_url'],
    author: Optional[str] = populate_dflts['author'],
    license: str = populate_dflts['license'],
    description_file: str = populate_dflts['description_file'],
    keywords: Optional[List] = populate_dflts['keywords'],
    install_requires: Optional[List] = populate_dflts['install_requires'],
    long_description=populate_dflts['long_description'],
    long_description_content_type=populate_dflts[
        'long_description_content_type'
    ],
    include_pip_install_instruction_in_readme=True,
    verbose: bool = populate_dflts['verbose'],
    overwrite: List = (),
    defaults_from: Optional[str] = None,
    skip_docsrc_gen=False,
    **configs,
):
    """Populate project directory root with useful packaging files, if they're missing.

    >>> from wads.populate import populate_pkg_dir
    >>> import os  # doctest: +SKIP
    >>> name = 'wads'  # doctest: +SKIP
    >>> pkg_dir = f'/D/Dropbox/dev/p3/proj/i/{name}'  # doctest: +SKIP
    >>> populate_pkg_dir(pkg_dir,  # doctest: +SKIP
    ...                  description='Tools for packaging',
    ...                  root_url=f'https://github.com/i2mint',
    ...                  author='OtoSense')

    :param pkg_dir:
    :param description:
    :param root_url:
    :param author:
    :param license:
    :param description_file:
    :param keywords:
    :param install_requires:
    :param long_description:
    :param long_description_content_type:
    :param verbose:
    :param default_from: Name of field to look up in wads_configs to get defaults from,
        or 'user_input' to get it from user input.
    :param configs:
    :return:

    """

    args_defaults = dict()
    if defaults_from is not None:
        if defaults_from == 'user_input':  # TODO: Implement!
            args_defaults = dict()  # ... and then fill with user input
            raise NotImplementedError(
                'Not immplemented yet'
            )  # TODO: Implement
        else:
            try:
                wads_configs = json.load(open(wads_configs_file))
                args_defaults = wads_configs[defaults_from]
            except KeyError:
                raise KeyError(
                    f"{wads_configs_file} json didn't have a {defaults_from} field"
                )

    if isinstance(overwrite, str):
        overwrite = {overwrite}
    else:
        overwrite = set(overwrite)

    _clog = mk_conditional_logger(condition=verbose, func=print)
    pkg_dir = os.path.abspath(os.path.expanduser(pkg_dir))
    assert os.path.isdir(pkg_dir), f'{pkg_dir} is not a directory'
    if pkg_dir.endswith(path_sep):
        pkg_dir = pkg_dir[
            :-1
        ]  # remove the slash suffix (or basename will be empty)
    name = os.path.basename(pkg_dir)
    pjoin = lambda *p: os.path.join(pkg_dir, *p)

    if name not in os.listdir(pkg_dir):
        f = pjoin(name)
        _clog(f'... making directory {pkg_dir}')
        os.mkdir(f)
    if '__init__.py' not in os.listdir(pjoin(name)):
        f = pjoin(name, '__init__.py')
        _clog(f'... making an empty {f}')
        with open(f, 'w') as fp:
            fp.write('')

    # Note: Overkill since we just made those things...
    if name not in os.listdir(pkg_dir) or '__init__.py' not in os.listdir(
        pjoin(name)
    ):
        raise RuntimeError(
            "You should have a {name}/{name}/__init__.py structure. You don't."
        )

    if os.path.isfile(pjoin('setup.cfg')):
        with open(pjoin('setup.cfg'), 'r'):
            pass

    kwargs = dict(
        description=description,
        root_url=root_url,
        author=author,
        license=license,
        description_file=description_file,
        long_description=long_description,
        long_description_content_type=long_description_content_type,
        keywords=keywords,
        install_requires=install_requires,
    )
    kwargs = {k: v for k, v in kwargs.items() if v is not None}
    # configs = dict(name=name, **configs, **kwargs, **args_defaults)
    # configs = dict(name=name, **args_defaults, **configs, **kwargs)
    configs = dict(ChainMap(dict(name=name), kwargs, configs, args_defaults))

    kwargs['description-file'] = kwargs.pop('description_file', '')

    assert (
        configs.get('name', name) == name
    ), f"There's a name conflict. pkg_dir tells me the name is {name}, but configs tell me its {configs.get('name')}"
    configs['display_name'] = configs.get('display_name', configs['name'])

    def copy_from_resource(resource_name):
        _clog(f'... copying {resource_name} from {root_dir} to {pkg_dir}')
        shutil.copy(wads_join(resource_name), pjoin(resource_name))

    def should_update(resource_name):
        return (resource_name in overwrite) or (
            not os.path.isfile(pjoin(resource_name))
        )

    for resource_name in pkg_path_names:
        if should_update(resource_name):
            copy_from_resource(resource_name)

    def save_txt_to_pkg(resource_name, content):
        target_path = pjoin(resource_name)
        assert not os.path.isfile(target_path), f'{target_path} exists already'
        _clog(f'... making a {resource_name}')
        with open(pjoin(resource_name), 'wt') as fp:
            fp.write(content)

    if should_update('setup.cfg'):
        _clog("... making a 'setup.cfg'")
        if 'pkg-dir' in configs:
            del configs['pkg-dir']
        write_configs(pjoin(''), configs)

    if should_update('LICENSE'):
        _license_body = license_body(configs['license'])
        save_txt_to_pkg('LICENSE', _license_body)

    if should_update('README.md'):
        readme_text = gen_readme_text(name, configs.get('description'))
        if include_pip_install_instruction_in_readme:
            readme_text += f'\n\nTo install:\t```pip install {name}```\n'
        save_txt_to_pkg('README.md', readme_text)

    if not skip_docsrc_gen:
        # TODO: Figure out epythet and wads relationship -- right now, there's a reflexive dependency
        from epythet.docs_gen.setup_docsrc import make_docsrc

        make_docsrc(pkg_dir, verbose)

    return name


def update_pack_and_setup_py(
    target_pkg_dir, copy_files=('setup.py', 'wads/data/MANIFEST.in')
):
    """Just copy over setup.py and pack.py (moving the original to be prefixed by '_'"""
    copy_files = set(copy_files)
    if target_pkg_dir.endswith(path_sep):
        target_pkg_dir = target_pkg_dir[
            :-1
        ]  # remove the slash suffix (or basename will be empty)
    name = os.path.basename(target_pkg_dir)
    contents = os.listdir(target_pkg_dir)
    assert {'setup.py', name}.issubset(
        contents
    ), f"{target_pkg_dir} needs to have all three: {', '.join({'setup.py', name})}"

    pjoin = lambda *p: os.path.join(target_pkg_dir, *p)

    for resource_name in copy_files:
        print(
            f'... copying {resource_name} from {wads_join("")} to {target_pkg_dir}'
        )
        shutil.move(src=pjoin(resource_name), dst=pjoin('_' + resource_name))
        shutil.copy(src=wads_join(resource_name), dst=pjoin(resource_name))


def main():
    import argh  # TODO: replace by argparse, or require argh in wads?

    argh.dispatch_command(populate_pkg_dir)


if __name__ == '__main__':
    main()
