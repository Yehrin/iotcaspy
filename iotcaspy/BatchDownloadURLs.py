#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from concurrent import futures
import os
import datetime
import argparse
from functools import partial
from retry import retry
from ShellUtils import run_bash


def multiproc_handle(func, paralist, max_workers=4):
    """
    多进程处理，返回一个迭代器
    """
    executor = futures.ProcessPoolExecutor(max_workers=max_workers)
    results = executor.map(func, paralist)
    return results


def download_single_file(filepath, save_dir='./'):
    """
    下载单个文件
    返回：state, path
    """
    save_filepath = os.path.join(save_dir, filepath.rsplit('/', 1)[-1])
    if os.path.exists(save_filepath):
        return True, save_filepath
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    cmd = 'aria2c -x4 -d %s %s' % (save_dir, filepath)
    try:
        run_bash(cmd)
    except:
        pass
    # 判断文件是否生成
    if os.path.exists(save_filepath):
        return True, save_filepath
    else:
        return False, filepath


def multiproc_download(urls_filepath, save_dir='./', max_workers=4):
    """
    读取给定的URLs文件，并多进程下载
    返回的是一个生成器Generator
    """
    if not os.path.exists(urls_filepath):
        raise Exception('URL文件不存在！')
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    with open(urls_filepath, 'r') as f:
        download_urls = [url.strip() for url in f.readlines()]
    download_states = multiproc_handle(partial(download_single_file, save_dir=save_dir), download_urls, max_workers=max_workers)
    return download_states


def display_download_state(states, failed_filepath=None):
    """
    显示下载状态并返回下载失败的URL
    """
    failed_urls = []
    successful_cnt = failed_cnt = 0
    for state, path in states:
        if state:
            # 下载成功
            successful_cnt += 1
            pass
        else:
            failed_cnt += 1
            failed_urls.append(path)
        date = datetime.datetime.now()
        date_str = date.strftime('%Y-%m-%d %H:%M:%S')
        print('\r截止%s，总共下载%d个文件，其中：成功 %d，失败 %d。' % (date_str, failed_cnt+successful_cnt, successful_cnt, failed_cnt), end="")
    print('')
    if len(failed_urls) and failed_filepath:
        with open(failed_filepath, 'w') as f:
            for url in failed_urls:
                f.write(url+'\n')
    
    return failed_urls


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='批量下载URL文件中的文件')
    # 添加定位参数
    parser.add_argument('urls_dir', type=str,
                        help="URL文件路径")
    parser.add_argument('-save_dir', type=str, default='./', 
                        help="保存的目录或文件名")
    args = parser.parse_args()
    
    target_urls_filepath = args.urls_dir
    target_save_dir = args.save_dir
    download_states = multiproc_download(target_urls_filepath, target_save_dir, max_workers=20)
    display_download_state(download_states, os.path.join(target_save_dir, 'downloaded_failed_urls.txt'))


