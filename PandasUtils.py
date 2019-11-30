#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd

'''
Pandas 工具类
'''


def df_change_type(df, origin_type, target_type):
    """
    将DataFrame中类型为origin_type的列全部转化为target_type。大数据量的情况下非常耗时，不建议使用。

    :param df: 不带NaN的DataFrame
    :param origin_type: list类型的dtype
    :param target_type: 目标dtype
    :return: DataFrame
    """
    target_columns = list()
    for column in df.columns:
        if df[column].dtype in origin_type:
            target_columns.append(column)
    if target_columns is not None:
        df[target_columns] = df[target_columns].astype(target_type)
    return df







