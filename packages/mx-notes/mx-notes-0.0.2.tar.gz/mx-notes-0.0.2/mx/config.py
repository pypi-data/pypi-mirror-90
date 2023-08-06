import json
import os
from pathlib import Path
import sys

CONFIG_FILE = '.mxconfig'
GLOBAL_CONFIG_PATH = Path.home() / CONFIG_FILE
DEFAULT_CONFIG = {
    'SECRET_KEY': 'c24539f26c60a8509747f30c3d4a761c',
    'BINDINGS': [],
}


def _from_file(filename):

    def err_and_exit(msg):
        sys.stderr.write(filename + ': ' + msg + '\n')
        sys.exit(1)

    data = {}

    try:
        with open(filename) as f:
            data = json.load(f)
            if not isinstance(data, dict):
                err_and_exit('Expecting config to be dict, got {:s}'.format(type(data).__name__))
    except IOError:
        pass
    except ValueError as e:
        err_and_exit(str(e))

    return data


def load_config(path):

    config = DEFAULT_CONFIG.copy()
    config.update(_from_file(GLOBAL_CONFIG_PATH))
    config.update(_from_file(os.path.join(path, CONFIG_FILE)))

    return config
