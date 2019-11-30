#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
python 文件处理的工具集
'''

import os
import hashlib


def file_to_list(filepath):
    """
    读取txt文件的每一列并保存为list
    :param filepath: 
    :return: list
    """
    with open(filepath, 'r') as f:
        result = [line.strip() for line in f if line]# line后面会带有 '\n'，需要加strip()方法
    return result


def get_all_filenames(dirpath):
    """
    获取目录下所有文件名
    """
    all_filenames = list()
    for root, dirs, files in os.walk(dirpath):
        if files:
            for file in files:
                all_filenames.append(os.path.join(root, file))
    return all_filenames


def get_file_md5(fname):
    """
    获得文件的MD5值
    """
    m = hashlib.md5()
    with open(fname, 'rb') as fobj:
        while True:
            data = fobj.read(4096)
            if not data:
                break
            m.update(data)
    return m.hexdigest().upper()


def get_file_sha256(fname):
    """
    获得文件的SHA256值
    """
    m = hashlib.sha256()
    with open(fname, 'rb') as fobj:
        while True:
            data = fobj.read(4096)
            if not data:
                break
            m.update(data)
    return m.hexdigest().upper()


def get_bytesize_from_str(size_str):
    """
    将字符串表示的文件大小转换成以B为单位的数值
    输入示例：3.45KB
    """
    size_str = size_str.upper()
    unit_mapping = {
        'TB': 1024**4, 
        'GB': 1024**3, 
        'MB': 1024**2, 
        'KB': 1024**1, 
        'B': 1, 
    }
    for unit in unit_mapping:
        if unit in size_str:
            val = float(size_str.rsplit(unit, 1)[0].strip())
            val = int(val*unit_mapping[unit])
            break
    return val


def save_strlist_to_file(filepath, strlist):
    """
    将字符串序列写入到文件中
    """
    with open(filepath, 'w') as f:
        for line in strlist:
            f.write(line+'\n')


import pickle
def save_obj_to_file(obj, filepath):
    """
    将Python对象保存到文件中
    """
    if not filepath.endswith('.pkl'):
        filepath += '.pkl'
    with open(filepath, 'wb') as f:
        pickle.dump(obj, f)


def load_obj_from_file(filepath):
    """
    从文件中载入Python对象
    """
    assert os.path.exists(filepath)
    with open(filepath, 'rb') as f:
        obj = pickle.load(f)
    return obj







