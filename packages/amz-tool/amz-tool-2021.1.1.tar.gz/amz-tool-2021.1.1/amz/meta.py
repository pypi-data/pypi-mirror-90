# Handles fetching of meta data
import os
from functools import reduce
from operator import getitem

import yaml


def update_line_in_file(replace_containing, replace_with, filename):
    f = open(filename, 'r')
    lines = f.readlines()
    lines_upd = [f"{replace_with}\n" if replace_containing in l else l for l in lines]
    f.close()
    with open(filename, 'w') as f:
        f.write(''.join(lines_upd))
        f.close()


def get_version():
    PKG_DIR = os.path.dirname(__file__)
    v = open(f'{PKG_DIR}/data/VERSION').readlines()[0]
    return v.ljust(10, ' ')


def get_amz_config(key_chain):

    HOME_DIR = os.environ["HOME"]
    AMZ_CONFIG_FILE = HOME_DIR + '/.amz/config/amz-config.yaml'
    try:
        config = yaml.load(open(AMZ_CONFIG_FILE, 'r'), Loader=yaml.FullLoader)
        return reduce(getitem, key_chain, config)
    except:
        return


def get_yaml_config(filepath, key_chain):

    try:
        config = yaml.load(open(filepath, 'r'), Loader=yaml.FullLoader)
        return reduce(getitem, key_chain, config)
    except:
        return


def highlight_cmd(cmd):
    return f'\033[90m\033[107m {cmd} \033[0m'


def validate_script(filepath):
    # Open and parse yaml file
    yf = yaml.load(open(filepath), Loader=yaml.FullLoader)
    # Check for 4 sections - Meta, Install, Update, Remove
    if list(yf.keys()).sort() != ['meta', 'install', 'update', 'remove'].sort(): return False
    # Meta Section
    ## Reqd Keys
    if 'name' not in list(yf['meta'].keys()): return False
    if 'check' not in list(yf['meta'].keys()): return False
    ## deps keys are known?
    if 'deps' in list(yf['meta'].keys()):
        if not set(yf['meta']['deps'].keys()).issubset(set(['apt', 'py2', 'py3'])): return False
    ## args have default keys?
    if 'args' in list(yf['meta'].keys()):
        if not all('default' in val for val in list(yf['meta']['args'].values())): return False
    # Install/Update/Remove Section
    for sec in ['install', 'update', 'remove']:
        ## Each dict value is a list of str
        if not all(all(isinstance(cmd, str) for cmd in cmds) for cmds in list(yf[sec].values())): return False
    return True
