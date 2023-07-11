import os
import subprocess

import pytest

from connpass_client import ConnpassClient

# tmp_path 
# テスト中に一時ディレクトリを利用するためのフィクスチャ
# pathlib.Path オブジェクト
# tmp_path のスコープはテスト関数単位
# 各テスト関数内で使用される tmp_path は異なる一時ディレクトリパスを示す

def test_tmp_directory1(tmp_path):
    file_path = tmp_path / "test_file.txt"
    file_path.write_text("Hello, World!")

    print(file_path.resolve()) # 出力するには -s オプション

    assert file_path.exists()
    assert file_path.read_text() == "Hello, World!"


def test_tmp_directory2(tmp_path):
    file_path = tmp_path / "test_file.txt"
    file_path.write_text("Hello, World!")

    print(file_path.resolve()) # 出力するには -s オプション

    assert file_path.exists()
    assert file_path.read_text() == "Hello, World!"

# 問題
# 1. data = ConnpassClient().get(event_id="266898") を実行し、 data["events"][0]["title"] で返る結果が 'テスト駆動Python 第2版 読書会#1' であるテストを書いて下さい

def test_dataevent():
    data = ConnpassClient().get(event_id="266898")
    assert data["events"][0]["title"] == 'テスト駆動Python 第2版 読書会#1'


# 1. tmp_path フィクスチャを使って、一時ファイルに data["events"][0]["title"] の結果を書き込み、その内容を read_text して得られる文字列が、'テスト駆動Python 第2版 読書会#1' であるテストを書いて下さい

def test_tmp_directory_file(tmp_path):
    file_path = tmp_path / "266898.json"
    data = ConnpassClient().get(event_id="266898")

    file_path.write_text(data["events"][0]["title"])

    assert file_path.exists()
    assert file_path.read_text() == 'テスト駆動Python 第2版 読書会#1'

# 1. tmp_path フィクスチャを使って、一時ファイルに、python -m connpass_client --event-id 266898 --csv <temp_file_path> の結果を書き込んで下さい。その <temp_file_path> を read_text して得られる文字列の中に'テスト駆動Python 第2版 読書会#1'があることを確認するテストを書いて下さい。

def test_tmp_directory_file2(tmp_path):
    temp_file_path = tmp_path / "266898.csv"
    print(temp_file_path.resolve())

    subprocess.run(
        ["python", "-m", "connpass_client", "--event-id", "266898", "--csv", temp_file_path],
    )

    assert temp_file_path.exists()
    assert 'テスト駆動Python 第2版 読書会#1' in temp_file_path.read_text()


