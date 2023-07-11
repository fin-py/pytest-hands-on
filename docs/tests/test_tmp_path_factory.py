import pytest


# tmp_path_factory 
# テスト中に一時ディレクトリを利用するためのフィクスチャ
# TempPathFactoryオブジェクト
# tmp_path_factory のスコープはセッションにできる
# 同じモジュール内のすべてのテスト関数で同じ tmp_path_factory インスタンスが共有される


def test_temp_directory(tmp_path_factory): # デフォルトは関数スコープ
    temp_dir = tmp_path_factory.mktemp("my_temp_dir")
    file_path = temp_dir / "test_file.txt"
    file_path.write_text("Hello, World!")
    
    print(file_path.exists)

    assert file_path.exists()
    assert file_path.read_text() == "Hello, World!"

@pytest.fixture(scope="session")
def temp_filepath(tmp_path_factory):
    temp_dir = tmp_path_factory.mktemp("my_temp_dir")
    file_path = temp_dir / "test_file.txt"
    file_path.write_text("Hello, World!")
    return file_path


def test_hello(temp_filepath):
    print(temp_filepath)
    assert temp_filepath.read_text() == "Hello, World!"
    
# 練習問題


