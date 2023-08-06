# # main.py
#
# import argparse
#
# def main():
#
#     parser = argparse.ArgumentParser(prog='SsyiWorking', usage='This is a demo, please follow SsyiWorking on wechat')
#
#     parser.add_argument("name", default='SsyiWorking', help="This is a demo framework", action="store")
#
#     args = parser.parse_args()
#
#     if args.name:
#
#         print("Hello, My name is Ssyi, Please search and follow below account from wechat:\n")
#
#         print(args.name)
#
# if __name__ == "__main__":
#
#     main()



# main.py

import argparse

import codecs

import inspect

import json

import os

import shlex

import sys

import glob

import importlib.util

import yaml

# 解析命令行参数

def parse_options(user_options=None):

    parser = argparse.ArgumentParser(prog='Ssyi',

                                     usage='Demo Automation Framework, Search wechat account iTesting for more information')

    parser.add_argument("-env", default='dev', type=str, choices=['dev', 'qa', 'staging', 'prod'], help="Env parameter")

    if not user_options:

        args = sys.argv[1:]

    else:

        args = shlex.split(user_options)

    options, un_known = parser.parse_known_args(args)

    if options.env:

        print("\n想了解更多测试框架内容吗？请关注公众号iTesting")

        print('Currently the env are set to: %s' % options.env)

    return options

# 从指定文件夹下获取模块及其所在的路径

def find_modules_from_folder(folder):

    absolute_f = os.path.abspath(folder)

    md = glob.glob(os.path.join(absolute_f, "*.py"))

    return [(os.path.basename(f)[:-3], f) for f in md if os.path.isfile(f) and not f.endswith('__init__.py')]

# 动态导入模块

def import_modules_dynamically(mod, file_path):

    spec = importlib.util.spec_from_file_location(mod, file_path)

    md = importlib.util.module_from_spec(spec)

    spec.loader.exec_module(md)

    return md

# 获取测试类所在的文件夹和测试类对应的数据类所在的文件夹

def get_tests_and_data_folder_via_env(env):

    # 注意，下面的test_root和test_data_root这两个方法。从main函数执行，和从命令行输入iTesting运行，获取到的值不同

    # 当前此代码获取方式是通过命令行运行，即使用pip install iTesting后，在命令行中使用iTesting来执行

    test_root = os.path.join(os.getcwd(), 'SsyiWorking' + os.sep + 'script')

    test_data_root = os.path.join(os.getcwd(), 'SsyiWorking' + os.sep + 'ssyi_data' + os.sep + env)

    # current_folder, current_file = os.path.split(os.path.realpath(__file__))

    # test_data_root = os.path.join(current_folder, 'test_data' + os.sep + env)

    # test_root = os.path.join(current_folder, 'tests')

    return test_root, test_data_root

# 解析数据文件的方法

def load_data_from_json_yaml(yaml_file):

    _is_yaml_file = yaml_file.endswith((".yml", ".yaml"))

    with codecs.open(yaml_file, 'r', 'utf-8') as f:

        # Load the data from YAML or JSON

        if _is_yaml_file:

            data = yaml.safe_load(f)

        else:

            data = json.load(f)

    return data

# 测试框架的执行函数

def run(test_folder, test_data_folder):

    module_pair_list = find_modules_from_folder(test_folder)

    for m in module_pair_list:

        mod = import_modules_dynamically(m[0], m[1])

        test_data_file = os.path.join(test_data_folder, mod.__name__ + '.yaml')

        for cls_name, cls in inspect.getmembers(mod, inspect.isclass):

            if cls_name.startswith('Ssyi'):

                for item in inspect.getmembers(cls, lambda fc: inspect.isfunction(fc)):

                    func_name, func = item

                    if func_name.startswith('ssyi'):

                        test_data = load_data_from_json_yaml(test_data_file)

                        print("\n想了解更多测试框架内容吗？请关注公众号iTesting")

                        print(test_data["username"])

                        print(test_data["password"])

                        func(cls_name, test_data["username"], test_data["password"], True)

# main函数，也是测试框架入口

def main(user_options=None):

    args = parse_options(user_options)

    test_root, test_data_root = get_tests_and_data_folder_via_env(args.env)

    run(test_root, test_data_root)

if __name__ == "__main__":

    main('-env dev')
