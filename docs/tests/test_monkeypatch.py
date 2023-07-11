# monkeypatch
# アプリケーションコードや環境を変更
# 外部の依存関係やグローバルな状態をモックしたり、テスト用のダミーデータを提供したりする

import json
import os

import tests.foo as foo
from connpass_client import ConnpassClient


def get_lang_value():
    return os.environ.get("LANG")  # 'ja_JP.UTF-8'


def test_get_lang_value(monkeypatch):
    # 環境変数をモック
    monkeypatch.setenv("LANG", "Mocked Lang Value")

    result = get_lang_value()
    assert result == "Mocked Lang Value"


def get_data():
    return "Real data"


def process_data():
    data = get_data()
    return data.upper()


def test_process_data(monkeypatch):
    # モジュールの関数をモック
    def mock_get_data():
        return "Mocked data"

    # モジュールの関数をモックに置き換え
    monkeypatch.setattr("tests.foo.get_data", mock_get_data)

    result = foo.process_data()
    assert result == "MOCKED DATA"

# テスト対象のクラス
class MyClass:
    def my_method(self, arg1, arg2):
        return arg1 + arg2

# テスト
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

def test_client_data(monkeypatch):
    mock_response = {
        "results_start": 1,
        "results_returned": 1,
        "results_available": 1,
        "events": [{"event_id": 266898}],
    }

    obj = ConnpassClient()

    # モックの ConnpassClient().get() メソッド
    def mock_get(**kwargs):
        with open("./tests/mock_266898.json", "r") as f:
            data = json.load(f)
        return data

    monkeypatch.setattr(obj, "get", mock_get)
    result = obj.get(event_id="266898")
    assert result == mock_response

