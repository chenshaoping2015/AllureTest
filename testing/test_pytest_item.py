import pytest

@pytest.fixture
@pytest.mark.P0
def node_info(request):
    # 获取当前测试节点
    node = request.node
    print(f"测试节点名称: {node.name}")
    print(f"测试节点类名: {getattr(node.cls, '__name__', 'None')}")
    print(f"测试节点标签: {node.own_markers}")
    yield

import pytest

@pytest.fixture
def check_test_result(request):
    yield
    # 获取测试调用阶段的报告
    report = request.node.rep_call
    if report.failed:
        print(f"测试失败: {report.longreprtext}")
    else:
        print(f"测试成功，耗时: {report.duration:.2f}s")

def add(a, b):
    return a / b

def test_node_info(node_info):
    print(node_info)

def test_add(check_test_result):
    add(1, 2)

def test_path():
    PathUtils.directory("log")