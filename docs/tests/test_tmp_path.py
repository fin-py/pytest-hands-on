import pytest


# tmp_path 
# テスト中に一時ディレクトリを利用するためのフィクスチャ
# pathlib.Path オブジェクト
# tmp_path のスコープはテスト関数単位
# 各テスト関数内で使用される tmp_path は異なる一時ディレクトリパスを示す

def test_tmp_directory1(tmp_path):
    file_path = tmp_path / "test_file.txt"
    file_path.write_text("Hello, World!")

    print(file_path.exists) # 出力するには -s オプション

    assert file_path.exists()
    assert file_path.read_text() == "Hello, World!"


def test_tmp_directory2(tmp_path):
    file_path = tmp_path / "test_file.txt"
    file_path.write_text("Hello, World!")

    print(file_path.exists) # 出力するには -s オプション

    assert file_path.exists()
    assert file_path.read_text() == "Hello, World!"

# 練習問題