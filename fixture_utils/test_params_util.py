# 测试模块
import pytest
from pythoncode.calculator import Calculator


class TestCalculator:

    def setup_class(self):
        print("实例化calculator对象")
        self.calc = Calculator()

    def setup(self):
        print("开始计算")

    def teardown(self):
        print("结束计算")

    def teardown_class(self):
        print("结束测试")

    # 冒烟测试用例
    @pytest.mark.run(order=3)
    @pytest.mark.data_level("P0")
    # 参数，就是我们要传递的数据序列（可以列表，可以元组），每个序列里存放一组数据
    def test_add0(self, a, b, expect):
        # 测试相加方法
        result = self.calc.add(a, b)
        print(result)
        # 实际结果 对比 预期结果
        assert result == expect

    # 有效边界值
    @pytest.mark.run(order=1)
    @pytest.mark.data_level("P1_1")
    def test_add1(self, a, b, expect):
        result = self.calc.add(a, b)
        assert result == expect

    # 异常情况处理
    @pytest.mark.run(order=2)
    @pytest.mark.data_level("P1_2")
    def test_add2(self, a, b, errortype):
        # pytest 封装的一种处理异常的方式
        with pytest.raises(eval(errortype)) as e:
            result = self.calc.add(a, b)

        print(e.typename)

    @pytest.mark.run(order=-1)
    @pytest.mark.data_level("P2")
    def test_add3(self, a, b, errortype):
        # pytest 封装的一种处理异常的方式
        with pytest.raises(eval(errortype)) as e:
            result = self.calc.add(a, b)

        print(e.typename)
        try:
            result = self.calc.add("中",9.3)
        except TypeError as e :
            print("异常信息：")
            print(e)

    def test_add4(self):
        with pytest.raises(eval("TypeError")) as e:
            result = self.calc.add("中", 0)

        print(e.typename)

