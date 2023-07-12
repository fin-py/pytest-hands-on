# 組み込みフィクスチャ練習問題

## tmp_path

### 復習
- テスト中に一時ディレクトリを利用するためのフィクスチャ
- pathlib.Path オブジェクト
- tmp_path のスコープはテスト関数単位
- 各テスト関数内で使用される tmp_path は異なる一時ディレクトリパスを示す


```python 
def test_tmp_directory1(tmp_path):
    file_path = tmp_path / "test_file.txt"
    file_path.write_text("Hello, World!")

    print(file_path.resolve())  # 出力するには -s オプション

    assert file_path.exists()
    assert file_path.read_text() == "Hello, World!"


def test_tmp_directory2(tmp_path):
    file_path = tmp_path / "test_file.txt"
    file_path.write_text("Hello, World!")

    print(file_path.resolve()) # 出力するには -s オプション

    assert file_path.exists()
    assert file_path.read_text() == "Hello, World!"
```

### 問題
1. `data = ConnpassClient().get(event_id="266898")` を実行し、`data["events"][0]["title"]` で返る結果が `'テスト駆動Python 第2版 読書会#1'` であるテストを書いて下さい
1. tmp_path フィクスチャを使って、一時ファイルに `data["events"][0]["title"]` の結果を書き込み、その内容を `read_text` して得られる文字列が、`'テスト駆動Python 第2版 読書会#1'` であるテストを書いて下さい
1. tmp_path フィクスチャを使って、一時ファイルに、`python -m connpass_client --event-id 266898 --csv <temp_file_path>` の結果を書き込んで下さい。その `<temp_file_path>` を `read_text` して得られる文字列の中に`'テスト駆動Python 第2版 読書会#1'`があることを確認するテストを書いて下さい。
    - [ヒント]: `python -m connpass_client` を実行するには、外部プロセスを実行するための機能を提供する `subprocess.run` を使います。例：
        ```python 
        import subprocess
        subprocess.run(
            ["python", "-m", "connpass_client", "--event-id", "266898", "--csv", <temp_file_path>], 
        )
        ```
    - [ヒント]: Windows の方は、python へのフルパスを渡す必要が有るようです。パスはこの様に取得出来ます。
        ```python 
        import sys

        python_path = sys.executable
        print(python_path)
        ```

## tmp_path_factory

### 復習
- テスト中に一時ディレクトリを利用するためのフィクスチャ
- TempPathFactoryオブジェクト
- tmp_path_factory のスコープはセッションに設定できる
- 同じモジュール内のすべてのテスト関数で同じ tmp_path_factory インスタンスを共有できる

```python 
import pytest

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
```
### 問題
1. tmp_path_factory フィクスチャを使って、一時ファイルに、`python -m connpass_client --event-id 266898 --csv temp_file_path` の結果を `scope="session"`で書き込んで下さい。
1. 1で作ったフィクスチャを使って 文字列 `'テスト駆動Python 第2版 読書会#1'` が含まれているか確認するテストを書いて下さい。

## capsys
- Pythonの標準出力と標準エラー出力をキャプチャし、テスト中にアクセスしてテスト結果を検証することができる

### 復習
```python 
def test_1(capsys):
    print("Hello World!")
    assert capsys.readouterr().out.strip() == "Hello World!"
```
### subprocess.run の使い方
- 外部プロセスを実行するための機能を提供
- 返り値は、標準出力の場合 `stdout` に、標準エラー出力の場合  `stderr` にキャプチャされる

```python 
import subprocess
import connpass_client

def test_version_v1():
    output = subprocess.run(
        ["python", "-m", "connpass_client", "--version"],
        capture_output=True, # 標準出力と標準エラー出力 をキャプチャ
        text=True # 標準出力と標準エラー出力をデコードされた文字列として返す
    )
    output = output.stdout.rstrip()
    assert output == connpass_client.__version__
```
### CliRunnerの使い方
- [Typer](https://typer.tiangolo.com/) は、Pythonのコマンドラインアプリケーションの構築を支援するフレームワーク
- [CliRunner](https://typer.tiangolo.com/tutorial/testing/#test-the-app) はそのテストサポートを提供
- `invoke()` メソッドを使用して、テスト対象のコマンドを呼び出すことができる。引数やオプションを指定し、コマンドの実行結果を取得。

```python 
from typer.testing import CliRunner

def test_version_v2():
    runner = CliRunner()
    result = runner.invoke(connpass_client.app, ["--version"])
    output = result.stdout.rstrip()
    assert output == connpass_client.__version__
```

### 問題
1. `ConnpassClient().get(event_id="266898")` で取得できる辞書の `results_returned` キーに入っているデータは`"1"`であることをprint関数で出力してテストして下さい
1. `connpass_client` には `post` メソッドが無いので、呼び出そうとすると `AttributeError` が発生します。教科書の `2.6 想定される例外をテストする` を参考に期待するエラーが発生するテストを書いて下さい。
1. 存在しない `--event-id` (例 8888888888) を`connpass_client` に渡すと、以下の辞書が返ることをテストして下さい。コマンドの実行には `CliRunner()` を使って下さい。
    ```python 
    """{'events': [],\n 'results_available': 0,\n 'results_returned': 0,\n 'results_start': 1}"""
    ```
1. `connpass_client` に存在しないオプションを渡すとUsageが返ります。テストコマンドを使って期待した通り Usage が返ることをテストしてください。コマンドの実行には `subprocess.run()` を使って下さい。また、今回は標準エラー出力になるので、`stderr` にキャプチャされることに注意してください。
    テストコマンド:
    ```bash
    $ python -m connpass_client --taro
    ```
    ```bash
    Usage: python -m connpass_client [OPTIONS]
    Try 'python -m connpass_client --help' for help.

    Error: No such option: --taro Did you mean --start?
    ```

## monkeypatch 
### 復習
- アプリケーションコードや環境を変更
- 外部の依存関係やグローバルな状態をモックしたり、テスト用のダミーデータを提供したりする

### 練習
1. 環境変数をモック
    1. 環境変数を得る関数を書く
        ```python 
        import os
        def get_lang_value():
            return os.environ.get("LANG")  # 'ja_JP.UTF-8'        
        ```
    1. 環境変数をモックしてテストを書く
        ```python 
        def test_get_lang_value(monkeypatch):
            # 環境変数をモック
            monkeypatch.setenv("LANG", "Mocked Lang Value")

            result = get_lang_value()
            assert result == "Mocked Lang Value"        
        ```

1. 引数があるメソッドをモック
    1. テスト対象のクラス
        ```python 
        class MyClass:
            def my_method(self, arg1, arg2):
                return arg1 + arg2
        ```
    1. テスト
        ```python 
        def test_my_method(monkeypatch):
            # オブジェクトを作成
            obj = MyClass()

            # モック用の関数を定義
            def mock_method(arg1, arg2):
                return arg1 * arg2

            # モック用の関数を設定
            monkeypatch.setattr(obj, "my_method", mock_method)

            # モックが呼び出される
            result = obj.my_method(3, 4)

            # モックの結果を検証
            assert result == 12
        ```
### 問題

1. 適当なJSONファイルを作成し、以下のデータを挿入してください
    ```json
    {
        "results_start": 1,
        "results_returned": 1,
        "results_available": 1,
        "events": [
            {
                "event_id": 266898
            }
        ]
    }     
    ```
1. `ConnpassClient` の `get` が呼ばれたら先程のJsonファイルをloadするようにモックしてください。次に、`ConnpassClient().get(event_id="266898")` が実行されたらサーバに問い合わせに行かずに、モック関数が実行され、返り値が上記の辞書データと一致するか確認するテストを書いてください。JSONファイルのloadは以下のように書くことができます。
    ```python 
    import json
    with open("json file へのパス", "r") as f:
        data = json.load(f)
    return data    
    ```
