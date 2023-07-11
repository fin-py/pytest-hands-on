import subprocess

import pytest

from connpass_client import ConnpassClient

# tmp_path_factory 
# テスト中に一時ディレクトリを利用するためのフィクスチャ
# TempPathFactoryオブジェクト
# tmp_path_factory のスコープはセッションに設定できる
# 同じモジュール内のすべてのテスト関数で同じ tmp_path_factory インスタンスを共有できる


def test_temp_directory(tmp_path_factory): # デフォルトは関数スコープ
    temp_dir = tmp_path_factory.mktemp("my_temp_dir")
    file_path = temp_dir / "test_file.txt"
    file_path.write_text("Hello, World!")
    
    print(file_path.resolve()) 

    assert file_path.exists()
    assert file_path.read_text() == "Hello, World!"

@pytest.fixture(scope="session")
def temp_filepath(tmp_path_factory):
    temp_dir = tmp_path_factory.mktemp("my_temp_dir")
    file_path = temp_dir / "test_file.txt"
    file_path.write_text("Hello, World!")
    return file_path


def test_hello(temp_filepath):
    print(temp_filepath.resolve())
    assert temp_filepath.read_text() == "Hello, World!"
    
# 問題

# 1. tmp_path_factory フィクスチャを使って、一時ファイルに、python -m connpass_client --event-id 266898 --csv temp_file_path  の結果を書き込んで下さい。その時、fixture の scope を session にしてください。

@pytest.fixture(scope="session")
def tmp_file(tmp_path_factory):
    temp_dir = tmp_path_factory.mktemp("connpass-client")
    file_path = temp_dir / "266898.csv"

    subprocess.run(
        ["python", "-m", "connpass_client", "--event-id", "266898", "--csv", file_path],
    )
    print(file_path.resolve())
    return file_path

# 1. 1で作ったフィクスチャを使って 文字列 'テスト駆動Python 第2版 読書会#1' が含まれているか確認するテストを書いて下さい。

def test_read_temp_file(tmp_file):
    print(tmp_file.resolve())
    assert 'テスト駆動Python 第2版 読書会#1' in tmp_file.read_text() 


