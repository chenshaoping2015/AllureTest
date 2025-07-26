import pytest

#-------------------------------------示例1-----------------------------------------------------
@pytest.fixture
def setup_and_teardown():
    # 测试用例执行前的准备工作
    print("准备数据阶段")
    try:
        yield
    finally:
        # 测试用例执行后的清理工作
        print("无论失败与否，都会清理数据")

def test_example(setup_and_teardown):
    # 模拟测试用例执行过程中抛出异常
    raise ValueError("Something went wrong")

#-----------------------------------示例2--------------------------------------------------------
@pytest.fixture
# 若需根据测试是否失败执行不同清理操作，需通过 request 对象获取测试结果
def conditional_teardown(request):
    # 测试用例执行前的准备工作
    print("准备工作正式开始----------------------------")

    # 保存测试结果的引用
    result = {"excinfo": None}
    # 定义清理函数
    def finalizer():
        if result["excinfo"] is not None:
            print(f"用例失败后的清理工作（错误原因: {result['excinfo']}）--------------------")
        else:
            print("用例成功后的清理工作---------------------------")
    # 注册清理函数
    request.addfinalizer(finalizer)
    # 返回结果容器（供后续填充）
    return result

def test_success(conditional_teardown):
    print("Running test_success")

def test_failure(conditional_teardown):
    try:
        assert False
    except AssertionError as e:
        # 捕获异常并保存到 result
        conditional_teardown["excinfo"] = str(e)
        raise
#-----------------------------------示例3--------------------------------------------------------

@pytest.fixture
def conditional_teardown(request):
    # Setup 逻辑
    print("准备工作正式开始----------------------------")
    yield
    # Teardown 逻辑
    print("清理工作开始---------------------------")

    # 获取测试结果
    report = request.node.rep_call
    if report.failed:
        print(f"用例失败后的清理工作（错误原因: {report.longreprtext}）--------------------")
    else:
        print("用例成功后的清理工作---------------------------")


def test_success(conditional_teardown):
    print("Running test_success")


def test_failure(conditional_teardown):
    assert False
