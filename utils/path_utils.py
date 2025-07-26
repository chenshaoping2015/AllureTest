# -*- coding:utf-8 -*-
# @Time  :2022/11/27 23:50
# @Author: stevenchen
"""
公共方法：
1.输入的filepath为目录时：
    若目录存在，返回目录路径
    若目录不存在，自动创建目录并返回创建后的目录路径
2.输入的filepath为文件时：
    若文件存在，返回文件路径
    若文件不存在，提示用户去创建文件并返回目录文件
"""

import os


class PathUtils:
    # 设置路径(通用）
    @classmethod
    def directory(cls, filepath):
        """os.path.split(‘PATH’),PATH指一个文件的全路径作为参数：将文件名和路径分割开,将索引为0的视为目录（路径），将索引为1的视为文件名，以最后一个/做为分隔符"""
        # 获取项目根路径
        # original_path = os.path.split(os.path.dirname(__file__))[0] (弃用，更麻烦)
        original_path = os.path.dirname(os.path.dirname(__file__))
        # 在根目录下拼接一个新的路径
        full_path = os.path.join(original_path, filepath)
        # 规范化指定的路径,在Windows操作系统中，路径中的任何正斜杠(‘ / ‘)都会转换为反斜杠(‘ \ ‘)
        full_path = os.path.normpath(full_path)

        try:
            # 如果路径不包含文件名（即用户意图创建目录）
            # if not os.path.basename(full_path):
            #     dir_part = full_path
            # else:
            #     dir_part = os.path.dirname(full_path)

            # 确保目录存在
            if not os.path.exists(full_path):
                os.makedirs(full_path, exist_ok=True)
                print(f"创建了目录: {full_path}")
        except Exception as e:
            print(f"创建目录失败: 错误: {e}")
            raise

        return full_path

# if __name__ == '__main__':
#     print(PathUtils.directory("log"))
    # a = os.path.dirname(os.path.dirname(__file__))
    # print(type(a))
    # b = os.path.split(os.path.dirname(__file__))[0]
    # print(type(b))