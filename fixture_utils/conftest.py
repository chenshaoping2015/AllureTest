# conftest.py 文件中的函数是不需要导入的
# 位置：项目根目录
# 查找路径：
# 1. 先从当前模块找->再从当前目录->再往上级节点查找
import pytest
import sys
import os
import yaml

# from pythoncode.calculator import Calculator

# 获取项目根目录（即包含 pythoncode 目录的目录）
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)
pythoncode_path = os.path.join(project_root, "pythoncode")

def pytest_collection_modifyitems(items):
    """
    测试用例收集完成时，将收集到的item的name和nodeid的中文显示
    :return:
    """
    for item in items:
        item.name = item.name.encode("utf-8").decode("unicode_escape")
        item._nodeid = item.nodeid.encode("utf-8").decode("unicode_escape")

def get_datas(level):
    try:
        # safe_load: 把yaml 格式 转成python对象
        # safe_dump: 把python对象 转成yaml格式
        with open("fixture_utils/datas.yml", encoding="utf-8") as f:
            result = yaml.safe_load(f)
            add_datas = result.get("add").get(level).get('datas')
            add_ids = result.get("add").get(level).get('ids')
        # P0 级别的datas [[1, 1, 2], [-0.01, 0.02, 0.01], [10, 0.02, 10.02]]
        # P0 级别的ids ['2个整数', '2个浮点数', '整数+浮点数']
        return [add_datas, add_ids]
    except Exception as e:
        pytest.fail(f"加载测试数据失败: {str(e)}")


def pytest_generate_tests(metafunc):
    # pytest_generate_tests 钩子：适合需要全局控制参数化的场景
    # 检查测试函数是否有 data_level 标记
    marker = metafunc.definition.get_closest_marker("data_level")
    if marker:
        level = marker.args[0]  # 获取标记的参数（如 @pytest.mark.data_level("P1")）
        """动态生成参数化测试"""
        if "a" in metafunc.fixturenames and "b" in metafunc.fixturenames and "expect" in metafunc.fixturenames:
            # 直接调用数据加载函数，而非 Fixture
            datas, ids = get_datas(level)
            # 参数化测试
            metafunc.parametrize("a, b, expect", datas, ids=ids)


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # 获取测试结果
    outcome = yield
    report = outcome.get_result()
    # 按测试阶段（setup/call/teardown）绑定报告
    setattr(item, f"rep_{report.when}", report)  # 动态属性名

def pytest_runtest_call(item):
    """在测试函数执行时被调用"""
    print(f"开始执行测试函数: {item.name}")

# @pytest.fixture(scope="session", autouse=True)
# def manage_logs(request):
#     """Set log file name same as test name"""
#     now = time.strftime("%Y-%m-%d %H_%M_%S")
#     log_name = 'output/log/' + now + '.logs'
#     # request是 pytest中内置的fixture
#     request.config.pluginmanager.get_plugin("logging-plugin") \
#         .set_log_path(log_name)

# @pytest.fixture(scope="class")
# def get_calc():
#     calc = Calculator()
#     yield calc
#     print("结束测试")