#!/usr/bin/python
# -*- coding: utf-8 -*-
# encoding: utf-8
# coding=utf-8
'''
@author: karel.blavka@gmail.com
'''
import os
import sys
import logging
from io import IOBase
import yaml
from schema import Schema, And, Or, Use, Optional, SchemaError

DEFAULT = {
    'mqtt': {
        'host': '127.0.0.1',
        'port': 1883,
        'prefix': 'xcomfort'
    },
}


class ConfigError(Exception):
    pass


def port_range(port):
    return 0 <= port <= 65535


schema = Schema({
    'shc': {
        'host': And(str, len),
        'username': And(str, len),
        'password': And(str, len),
    },
    Optional('mqtt'): {
        Optional('host'): And(str, len),
        Optional('port'): And(int, port_range),
        Optional('prefix'): And(str, len),
        Optional('username'): And(str, len),
        Optional('password'): And(str, len),
        Optional('cafile'): os.path.exists,
        Optional('certfile'): os.path.exists,
        Optional('keyfile'): os.path.exists,
    },
})


def load_config(config_file):
    if isinstance(config_file, IOBase):
        config = yaml.safe_load(config_file)
        try:
            config = schema.validate(config)
        except SchemaError as e:
            raise ConfigError(str(e))

    elif config_file is None:
        config = {}

    _apply_default(config, DEFAULT)

    return config


def _apply_default(config, default):
    for key in default:
        if key not in config:
            config[key] = default[key]
            continue

        if isinstance(default[key], dict):
            _apply_default(config[key], default[key])
