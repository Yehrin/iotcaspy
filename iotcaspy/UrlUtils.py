#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
python URL处理的工具集
'''

from urllib.parse import urlparse


def get_domain_from_url(url):
    resp = urlparse(url)
    return resp.scheme + '://' + resp.netloc


