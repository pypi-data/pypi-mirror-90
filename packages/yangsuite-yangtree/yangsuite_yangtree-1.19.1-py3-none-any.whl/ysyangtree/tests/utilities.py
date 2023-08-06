"""Utility helper functions for tests."""

import json
import shutil
import os.path
from yangsuite.paths import set_base_path

canned_input_dir = os.path.join(os.path.dirname(__file__), 'canned_input')
canned_output_dir = os.path.join(os.path.dirname(__file__), 'canned_output')


def canned_input_str(filename, dir=''):
    """Get the text contents of the specified canned_input file."""
    with open(os.path.join(canned_input_dir, dir, filename), 'r') as fd:
        return fd.read()


def canned_input_data(filename, dir=''):
    """Get the specified canned_input file as a JSON object."""
    return json.loads(canned_input_str(filename, dir))


def canned_output_str(filename, dir=''):
    """Get the text contents of the specified canned_output file."""
    with open(os.path.join(canned_output_dir, dir, filename), 'r') as fd:
        return fd.read()


def canned_output_data(filename, dir=''):
    """Get the specified canned_output file as a JSON object."""
    return json.loads(canned_output_str(filename, dir))


def clone_test_data(new_location):
    if os.path.exists(new_location):
        shutil.rmtree(new_location)
    shutil.copytree(os.path.join(os.path.dirname(__file__), 'data'),
                    new_location)
    set_base_path(new_location)


def get_modules(replay):
    if 'task' in replay:
        return replay['task']['segments'][0]['yang']['modules']
    else:
        return replay['segments'][0]['yang']['modules']


def get_configs(replay):
    modules = get_modules(replay)
    return modules['test-option']['configs']
