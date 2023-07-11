import subprocess

import pytest
from typer.testing import CliRunner

import connpass_client

# capsys
# 標準出力のテスト

def test_1(capsys):
    print("Hello World!")
    assert capsys.readouterr().out.strip() == "Hello World!"


# subprocess を使ってPythonプログラムから別のプログラムやコマンドを実行
# その結果をテストする
def test_version_v1():
    output = subprocess.run(
        ["python", "-m", "connpass_client", "--version"],
        capture_output=True, 
        text=True
    )
    assert output.stdout.rstrip() == connpass_client.__version__

# CliRunner でコマンドを実行し、その結果をテストする
def test_version_v2():
    runner = CliRunner()
    result = runner.invoke(connpass_client.app, ["--version"])
    output = result.stdout.rstrip()
    assert output == connpass_client.__version__


# 練習問題
#  event_id="266898"で取得できるデータの "results_returned" キーに入っているデータは1であることをprintして
# 出力をキャプチャして、それが１であることをテストして下さい

def test_capsys_1(capsys):
    data = connpass_client.ConnpassClient().get(event_id="266898")
    print(data["results_returned"])
    assert capsys.readouterr().out.strip() == "1"

#  connpass_client には post メソッドが無いので、呼び出そうとすると AttributeError が発生します。
# 教科書の 2.6 想定される例外をテストする を参考に期待するエラーが発生するテストを書いて下さい。
def test_capsys_2():
    with pytest.raises(AttributeError):
        connpass_client.ConnpassClient.post()

# 存在しない event-id (例 8888888888) を渡すと、
# {'events': [],\n 'results_available': 0,\n 'results_returned': 0,\n 'results_start': 1} が返るテストを書いて下さい

def test_capsys_3():
    runner = CliRunner()
    result = runner.invoke(connpass_client.app, [ "--event-id", "8888888888"])
    output = result.stdout.rstrip()
    assert output == """{'events': [],\n 'results_available': 0,\n 'results_returned': 0,\n 'results_start': 1}"""
    


#  python -m connpass_client --taro をコマンドラインから実行すると、
# 以下のエラーメッセージが出力されることを subprocess.run を使ってテストを書いて下さい
# """Usage: python -m connpass_client [OPTIONS]\nTry 'python -m connpass_client --help' for help.\n\nError: No such option: --taro Did you mean --start?"""

def test_capsys_4():

    output = subprocess.run(
        ["python", "-m", "connpass_client", "--taro"],
        capture_output=True, 
        text=True
    )
    assert output.stderr.strip() == """Usage: python -m connpass_client [OPTIONS]
Try 'python -m connpass_client --help' for help.

Error: No such option: --taro Did you mean --start?"""