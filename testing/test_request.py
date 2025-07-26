import pytest


@pytest.fixture(params=[[12,13,25],[14,15,29]],ids = [1,2])
def get_param(request):
    #一定要使用request参数，The current parameter is available in ``request.param``.
    return request.param

def test_get_pa(get_param):
    print(get_param)

