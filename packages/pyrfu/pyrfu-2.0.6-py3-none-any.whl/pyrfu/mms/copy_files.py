#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# MIT License
#
# Copyright (c) 2020 Louis Richard
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so.

import os

from .list_files import list_files
from .mms_config import CONFIG


def copy_files(var=None, tint=None, mms_id=1, target_dir="./data/"):
    """Copy files from NAS24 to the target path

    Parameters
    ----------
    var : dict
        Dictionary containing 4 keys
            * var["inst"] : name of the instrument
            * var["tmmode"] : data rate
            * var["lev"] : data level
            * var["dtype"] : data type

    tint : list of str
        Time interval

    mms_id : str or int
        Index of the spacecraft

    target_dir : str
        Target path

    """
    assert var is not None and isinstance(var, dict)
    assert tint is not None and isinstance(tint, list)
    assert isinstance(mms_id, int)
    assert isinstance(target_dir, str)

    mms_path = CONFIG["local_data_dir"] + "/"

    files = list_files(tint, mms_id, var)

    for file in files:
        relative_path = os.path.split(file)[0].replace(mms_path, "")
        path = os.path.join(target_dir, relative_path)

        if not os.path.exists(path):
            os.makedirs(path)
            os.popen('cp {} {}'.format(file, os.path.join(path, os.path.split(file)[1])))
        else:
            os.popen('cp {} {}'.format(file, os.path.join(path, os.path.split(file)[1])))

    return