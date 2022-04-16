# -*- coding: utf-8 -*-

import os
import sys

import shutil
import PySimpleGUI as sg

def makeResouceFiles():
    """リソースフォルダを作成"""
    if os.path.exists("./resources") != True:
        os.mkdir("./resources")
    if os.path.exists("./resources/options.yml") != True:
        print(resourcePath("resources/options.yml"))
        shutil.copyfile(resourcePath("resources/options.yml"), "./resources/options.yml")

def resourcePath(filename): 
    """内部リソースを取得

    Args:
        filename (string): リソースのファイルpath

    Returns:
        file
    """
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, filename)
    return os.path.join(filename)