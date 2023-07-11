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
    - [ヒント1] Pythonファイル内で、コマンドライン引数を渡す時は、`-` は `_` にして下さい。（余談ですが、jupyter notebook のセルでは `-` です）
    - [ヒント2] `python -m connpass_client` を実行するには、外部プロセスを実行するための機能を提供する `subprocess.run` を使います。例：
        ```python 
        import subprocess
        subprocess.run(
            ["python", "-m", "connpass_client", "--event_id", "266898"], # --event-id ではなくて --event_id
        )
        ```
    - [ヒント3] csv への書き込みは、[fin-py/connpass-client つかいかた](https://github.com/fin-py/connpass-client/tree/typer#%E3%81%A4%E3%81%8B%E3%81%84%E3%81%8B%E3%81%9F)を参照して下さい。

## tmp_path_factory

### 復習
- テスト中に一時ディレクトリを利用するためのフィクスチャ
- TempPathFactoryオブジェクト
- tmp_path_factory のスコープはセッションに設定できる
- 同じモジュール内のすべてのテスト関数で同じ tmp_path_factory インスタンスを共有できる

```python 
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
```python 
import subprocess

def test_version_v1():
    output = subprocess.run(
        ["python", "-m", "connpass_client", "--version"],
        capture_output=True, 
        text=True
    )
    output = output.stdout.rstrip()
    assert output == connpass_client.__version__
```
### CliRunnerの使い方
- Typerは、Pythonのコマンドラインアプリケーションの構築を支援するフレームワーク
- CliRunnerはそのテストサポートを提供
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
1. `event_id="266898"` で取得できる辞書の `results_returned` キーに入っているデータは`1`であることをprint関数で出力してテストして下さい
1. `connpass_client` には `post` メソッドが無いので、呼び出そうとすると `AttributeError` が発生します。教科書の `2.6 想定される例外をテストする` を参考に期待するエラーが発生するテストを書いて下さい。
1. `connpass_client` に存在しない `event-id` (例 8888888888) を渡すと、以下の辞書が返ることをテストして下さい。
    ```python 
    {'events': [],\n 'results_available': 0,\n 'results_returned': 0,\n 'results_start': 1}
    ```
1. connpass_clientに存在しないオプションを渡すと Usageが返ります。例:
    ```bash
    > python -m connpass_client --taro
    Usage: python -m connpass_client [OPTIONS]
    Try 'python -m connpass_client --help' for help.

    Error: No such option: --taro Did you mean --start?
    ```
    期待した通り Usage が返ることをテストしてください
    

## monkeypatch 
### 復習
- アプリケーションコードや環境を変更
- 外部の依存関係やグローバルな状態をモックしたり、テスト用のダミーデータを提供したりする

### 練習
1. 環境変数をモック
    1. 環境変数を得る関数を書く
        ```python 
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

1. モジュール関数のモック
    1. tests ディレクトリに `foo.py` を新規作成してコード記述
        ```python 
        # モジュールの関数
        def get_data():
            return "Real data"

        # テスト対象の関数
        def process_data():
            data = get_data()
            return data.upper()
        ```
    1. process_data関数をモックしてテストを書く
        ```python 
        import tests.foo as foo

        def test_process_data(monkeypatch):
            # モジュールの関数をモック
            def mock_get_data():
                return "Mocked data"

            # モジュールの関数をモックに置き換え(TODO: foo.get_data ではできない。理由はどりらんせんせいに）
            monkeypatch.setattr("tests.foo.get_data", mock_get_data) 

            result = foo.process_data()
            assert result == "MOCKED DATA"

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
1. ConnpassClientの get メソッドが呼ばれたら先程のJsonファイルをREADするようにモックして、テストを書いてください。JSONファイルのReadは以下のように書くことができます。
    ```python 
    import json
    with open("json file へのパス", "r") as f:
        data = json.load(f)
    return data    
    ```
