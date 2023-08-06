# -*- coding: utf-8 -*-

import os
import datetime
import glob
import re
import shutil

import binarybrain as bb


def get_date_string():
    ''' Get date strings for save path
        データ保存パス用の日付文字列を生成
    '''
    return datetime.datetime.now().strftime('%Y%m%d_%H%M%S')

def is_date_string(text: str):
    ''' Check if the string is a date
        データ保存パス用の日付文字列かどうか判定
    
        Args:
            text (str): 判定する文字列
        
        Returns:
            Boolean.
    '''
    
    if re.fullmatch('[12][0-9]{3}[01][0-9][0-3][0-9]_[0-2][0-9][0-5][0-9][0-5][0-9]', text):
        return True
    return False
    
def get_latest_path(path: str) -> str:
    ''' Get latest data path
        最新のデータ保存パスを取得
    
        Args:
            path (str): 検索するパス
        
        Returns:
            見つかったパス. 見つからなければ None
    '''
    
    if not os.path.exists(path):
        return None
    
    files = os.listdir(path)
    dirs  = [f for f in files if os.path.isdir(os.path.join(path, f))]
    
    targets = []
    for d in dirs:
        if is_date_string(d):
            targets.append(d)
    
    if not targets:
        return None
    
    targets.sort(reverse=True)
    return os.path.join(path, targets[0])


def remove_old(path: str, keep: int=-1):
    ''' Get latest data path
        最新のデータ保存パスを取得
    
        Args:
            path (str): 検索するパス
            keep (int): 削除せずに残す数
    '''
    
    if keep < 0:
        return
    
    files = os.listdir(path)
    dirs  = [f for f in files if os.path.isdir(os.path.join(path, f))]
    
    targets = []
    for d in dirs:
        if is_date_string(d):
            no_delete_file = os.path.join(path, d, '__no_delete__')
            if not os.path.exists(no_delete_file):
                targets.append(d)
    
    targets.sort(reverse=True)
    del targets[:keep]
    
    for t in targets:
        shutil.rmtree(os.path.join(path, t))


def save_models(path: str, net, *, write_layers=True, force_flatten=False):
    ''' save networks
        ネットを構成するモデルの保存
        
        Args:
            path (str):  保存するパス
            net (Model): 保存するネット
            write_layers (bool) : レイヤー別にも出力するかどうか
    '''
    
    # make dir
    os.makedirs(path, exist_ok=True)
    
    # save
    net_name = net.get_name()
    net_file_name = os.path.join(path, net_name + '.bin')
    with open(net_file_name, 'wb') as f:
        f.write(net.dump_bytes())

    # save flatten models
    if write_layers:
        models    = bb.get_model_list(net, flatten=True, force_flatten=force_flatten)
        fname_list = []  # 命名重複回避用
        for i, model in enumerate(models):
            name = model.get_name()
            if model.is_named():
                if name in fname_list:
                    print('[warrning] duplicate model name : %s', name)
                    fname = '%04d_%s.bin' % (i, name)
                else:
                    fname = '%s.bin' % (name)
            else:
                fname = '%04d_%s.bin' % (i, name)
            fname_list.append(fname)
            
            file_path = os.path.join(path, fname)
            
            with open(file_path, 'wb') as f:
                f.write(model.dump_bytes())


def load_models(path: str, net, *, read_layers: bool=True, force_flatten=False):
    ''' load networks
        ネットを構成するモデルの保存
        
        Args:
            path (str):  読み出すパス
            net (Model): 読み込むネット
            read_layers (bool) : レイヤー別に読み込むか
    '''

    # load
    net_name = net.get_name()
    net_file_name = os.path.join(path, net_name + '.bin')
    if not read_layers and os.path.exists(net_file_name):
        with open(net_file_name, 'rb') as f:
            dat = f.read()
            net.load_bytes(dat)
        return

    # load models
    models    = bb.get_model_list(net, flatten=True, force_flatten=force_flatten)
    fname_list = []
    for i, model in enumerate(models):
        name = model.get_name()
        if model.is_named():
            if name in fname_list:
                print('[warrning] duplicate model name : %s', name)
                fname = '%04d_%s.bin' % (i, name)
            else:
                fname = '%s.bin' % (name)
        else:
            fname = '%04d_%s.bin' % (i, name)
        fname_list.append(fname)
        
        file_path = os.path.join(path, fname)
        if os.path.exists(file_path):
            with open(file_path, 'rb') as f:
                dat = f.read()
                model.load_bytes(dat)
        else:
            print('file not found : %s' % file_path)
            
def save_networks(path: str, net, *, keep_olds: int=3, write_layers: bool=True, force_flatten: bool=False):
    ''' save networks
        ネットを構成するモデルの保存
        
        指定したパスの下にさらに日付でディレクトリを作成して保存
        古いものから削除する機能あり
        
        Args:
            path (str) : 保存するパス
            net (Model) : 保存するネット
            keep_olds (int) : 残しておく古いデータ数
    '''
    
    # make dir
    os.makedirs(path, exist_ok=True)
    
    # save with date
    date_str = get_date_string()
    data_path = os.path.join(path, date_str)
    
    save_models(data_path, net, write_layers=write_layers, force_flatten=force_flatten)
    
    if keep_olds >= 0:
        remove_old(path, keep=keep_olds)

def load_networks(path: str, net, *, read_layers: bool=True, force_flatten=False):
    ''' load network
        ネットを構成するモデルの読み込み
        
        最新のデータを探して読み込み
        
        Args:
            path (str) : 読み込むパス
            net (Model) : 読み込むネット
    '''
    
    data_path = get_latest_path(path)
    if data_path is None:
        print('not loaded : file not found')
        return
    
    load_models(data_path, net, read_layers=read_layers, force_flatten=force_flatten)
    print('load : %s' % data_path)
