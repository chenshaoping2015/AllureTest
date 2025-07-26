
import pytest

from pythoncode.calculator import Calculator
from utils.log_utils import Logging
import allure

# 大的功能点
@allure.feature("计算器功能")
class TestCalculator:
    logging = Logging().get_logger()
    calc = Calculator()
    # 冒烟测试用例
    @pytest.mark.run(order=3)
    @pytest.mark.data_level("P0")
    @allure.story("相加功能--冒烟测试")
    def test_add1(self, a, b, expect):
        self.logging.info(f"参数：{a}，{b}，期望结果：{expect}")
        # 测试相加方法
        with allure.step("正向场景相加操作"):
            result = self.calc.add(a, b)
        self.logging.info(f"结果：{result}")
        # 实际结果 对比 预期结果
        with allure.step("结果验证"):
            assert result == expect

    # 有效边界值
    @pytest.mark.run(order=1)
    @pytest.mark.data_level("P1_1")
    @allure.story("相加功能--负数测试")
    def test_add2(self, a, b, expect):
        self.logging.info(f"参数：{a}，{b}，期望结果：{expect}")
        result = self.calc.add(a, b)
        self.logging.info(f"结果：{result}")
        allure.attach.file("./image/logo.jpg", name="截图", attachment_type=allure.attachment_type.JPG, extension=".jpg")
        assert result == expect

    # 异常情况处理
    @pytest.mark.run(order=2)
    @pytest.mark.P1_2
    @allure.story("相加功能--中文测试")
    def test_add3(self, get_calc, p1_2_params):
        a, b, errortype =p1_2_params
        self.logging.info(f"参数：{a}，{b}，期望结果：{errortype}")
        # pytest 封装的一种处理异常的方式
        with pytest.raises(eval(errortype)) as e:
            result = get_calc.add(a, b)
            self.logging.info(f"结果：{result}")

        print(e.typename)

    @pytest.mark.run(order=-1)
    @pytest.mark.P2
    @allure.story("相加功能--空字符测试")
    def test_add4(self, get_calc, p2_params):
        a, b, errortype = p2_params
        self.logging.info(f"参数：{a}，{b}，期望结果：{errortype}")
        # pytest 封装的一种处理异常的方式
        with pytest.raises(eval(errortype)) as e:
            result = get_calc.add(a, b)
            self.logging.info(f"结果：{result}")

