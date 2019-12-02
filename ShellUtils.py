#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import subprocess


def run_bash(cmd, return_result=False):
    """
    运行shell命令
    """
    p = subprocess.Popen(cmd, shell=True, 
                            stdout=subprocess.PIPE, 
                            stderr=subprocess.PIPE)
    error = p.stderr.read().decode('utf-8')
    if error:
        raise Exception(error)
    if return_result:
        result = p.stdout.read().decode('utf-8')
        return result

