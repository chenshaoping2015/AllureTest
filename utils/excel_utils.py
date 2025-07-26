import pandas as pd
import numpy as np
from typing import Tuple, List, Union, Optional
import pytest

from path_utils import PathUtils


class ExcelDataReader:
    """
    Excel 数据读取工具类，用于与 pytest 参数化测试结合使用。
    功能：
    1. 读取 Excel 文件，支持多 Sheet 和标题行配置。
    2. 自动将数据转换为 Python 原生类型，兼容 pytest 参数化。
    3. 返回参数名（列名）和参数值（行数据）的分离结构。
    """

    @staticmethod
    def read_data(
            file_path: str,
            sheet_name: Union[str, int] = 0,
            has_header: bool = True
    ) -> Tuple[Optional[Tuple[str, ...]], List[Tuple]]:
        """
        读取 Excel 数据，返回参数名和参数值的元组。

        :param file_path: Excel 文件路径
        :param sheet_name: 工作表名称或索引，默认为第一个工作表
        :param has_header: 是否有标题行，默认为 True
        :return: (参数名, 参数值列表)
                 参数名为列名的元组（如果有标题行），否则为 None
                 参数值列表为每行数据的元组列表
        """
        # 读取 Excel 数据
        df = pd.read_excel(file_path, sheet_name=sheet_name, header=0 if has_header else None)

        # 提取列名(如通常第一行为整个文档的列名)
        # 列名元组（如果有标题行，如实例中的('用户名', '密码', '性别')），否则为None
        arg = tuple(df.columns) if has_header else None

        # 转换数据为 Python 原生类型并生成参数值列表
        rvalues = []
        for row in df.values:
            converted_row = [ExcelDataReader._convert_to_python_type(value) for value in row]
            rvalues.append(tuple(converted_row))

        return arg, rvalues

    @staticmethod
    def _convert_to_python_type(value: Union[np.generic, None]) -> Union[int, float, str, None]:
        """
        将 numpy/pandas 类型转换为 Python 原生类型。

        :param value: 原始值（可能为 numpy 类型）
        :return: Python 原生类型（int/float/str/None）
        """
        # 处理缺失值,统一将 numpy.nan、pandas.NA 等缺失值转换为 Python 的 None
        if pd.isna(value):
            return None
        # 将numpy 标量类型（如 np.int64）转换为Python原生类型
        # 输入：np.int64(5) → 输出：int(5)
        # 输入：np.float32(3.14) → 输出：float(3.14)
        elif isinstance(value, np.generic):
            return value.item()
        #保留原生类型
        else:
            return value

if __name__ == '__main__':

    # 示例用法
    # 读取带标题的 Excel 数据
    file_path = PathUtils.directory("selenium/selenium_wx/config/关键字文档.xlsx")
    no_heard_path = PathUtils.directory("config/test_data_no_header.xlsx")
    arg, rvalues = ExcelDataReader.read_data(file_path)
    print(rvalues)
    item = [value[2] for value in rvalues]
    print(item)

# @pytest.mark.parametrize(arg, rvalues)
#确保 Excel 文件的列名与测试函数参数名 完全一致（包括大小写和空格）
# def test_addition(a, b, expected):
#     assert a + b == expected


# 读取无标题的 Excel 数据
'''
ExcelDataReader.read_data 返回一个元组 (arg, rvalues)。

当 has_header=False 时，arg 为 None（无列名），rvalues 是参数值列表。

_ 用于接收第一个返回值（即 arg），表示“忽略此值”。

excel_no_header 接收第二个返回值（即 rvalues），即实际需要使用的数据。
'''
# _, excel_no_header = ExcelDataReader.read_data(no_heard_path, has_header=False)
#
#
# @pytest.mark.parametrize("a,b,expected", excel_no_header)
# def test_subtraction(a, b, expected):
#     assert a + b == expected

