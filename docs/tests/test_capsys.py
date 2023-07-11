import subprocess
import connpass_client

from typer.testing import CliRunner
import pytest 
# capsys
# 標準出力のテスト

def test_1(capsys):
    print("Hello World!")
    assert capsys.readouterr().out.strip() == "Hello World!"


# subprocess を使ってPythonプログラムから別のプログラムやコマンドを実行
# その結果でテストを行う

def test_version_v1():
    output = subprocess.run(
        ["python", "-m", "connpass_client", "--version"],
        capture_output=True, 
        text=True
    )
    output = output.stdout.rstrip()
    assert output == connpass_client.__version__
# capsys fails for subprocess calls · Issue #3319 · pytest-dev/pytest - https://github.com/pytest-dev/pytest/issues/3319


def test_version_v2():
    runner = CliRunner()
    result = runner.invoke(connpass_client.app, ["--version"])
    output = result.stdout.rstrip()
    assert output == connpass_client.__version__


# 練習問題
# 1 event_id="266898"で取得できるデータの "results_returned" キーに入っているデータは1であることをprintして
# 出力をキャプチャして、それが１であることをテストして下さい

def test_results_returned(capsys):
    data = connpass_client.ConnpassClient().get(event_id="266898")
    print(data["results_returned"])
    assert capsys.readouterr().out.strip() == "1"

# 2 connpass_client.ConnpassClient.post() は AttributeError が発生する
# テストを書いて下さい（2.6 想定される例外をテストする）

def test_notexist_method():
    with pytest.raises(AttributeError):
        connpass_client.ConnpassClient.post()

# 3 python -m connpass_client --taro をコマンドラインから実行すると、
# 以下のエラーメッセージが出力されることを subprocess.run を使ってテストを書いて下さい
# """Usage: python -m connpass_client [OPTIONS]\nTry 'python -m connpass_client --help' for help.\n\nError: No such option: --taro Did you mean --start?"""

def test_notexist_option():
    output = subprocess.run(
        ["python", "-m", "connpass_client", "--taro"],
        capture_output=True, 
        text=True
    )
    # print(output)
    assert output.stderr.strip() == """Usage: python -m connpass_client [OPTIONS]\nTry 'python -m connpass_client --help' for help.\n\nError: No such option: --taro Did you mean --start?"""


