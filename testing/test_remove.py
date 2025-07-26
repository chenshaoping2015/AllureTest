import pytest

@pytest.fixture
def temp_file():
    # Setup：创建临时文件
    file = open("./temp.txt", "w+")
    file.write("Hello, pytest!")
    yield file
    # Teardown：关闭并删除文件
    file.close()
    import os
    os.remove("temp.txt")

def test_file_content(temp_file):
    temp_file.seek(0) # 将指针移回文件开头
    content = temp_file.read()
    assert "pytest" in content