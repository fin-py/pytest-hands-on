# 練習課題

（2023/01/30更新：とりあえず思いつく問題をドンドン書いていって、あとで重複とかを削る）

各章に沿って練習問題を作りました。

[はじめてのpytest](./hello-world.ipynb) を一度実行して、`test_sample.py` を確認した後、練習問題を入ることをおすすめします。

## 注意

<font color="red"><strong>connpass の規約を守るために、 `connpass_client` を使う時は、リクエストは５秒以上間隔を開けて行う工夫をしてください。</strong></font>

## 第01章 はじめてのpytest
1. 1 は (range 10) に入っていることを確認するテスト
1. x = 10 y = 20 の時、 x < y であることを確認するテスト
1. 文字列 "finpy" は 文字列 "finpy-connpass" に入っていることを確認するテスト
1. リスト [4,5,6] は リスト [7,8,9] であることが失敗するテスト

## 第02章 テスト関数を書く
#### 検索結果が単一の場合のテスト
1. [APIリファレンス ](https://connpass.com/about/api/) によると、APIのレスポンスは、`['results_start', 'results_returned', 'results_available', 'events']` の4つのキーワードを持つ辞書です。 `event_id = "266898"` の返り値のキーワードが4つであることを確認するテストを書いて下さい。
1. そのキーワードが `['results_start', 'results_returned', 'results_available', 'events']` であることを確認するテストを書いて下さい。
1. `'events'`に紐づくデータの型は `配列(複数要素)`です。よって型は `<class 'list'>` です。これを確認するテストを書いて下さい。
1. `event_id = "266898"` のイベントは1つしか無いので、`'events'` で得られる配列の要素数も1つです。これを確認するテストを書いて下さい。
1. `'events'`で得られた各配列は辞書型のデータです。これを確認するテストを書いて下さい。

#### 検索結果が複数の場合のテスト
1. `series_id=5944` のグループはイベントページを10個作成しています。レスポンスの `'results_returned'` が10であることを確認するテストを書いて下さい。
1. また、`'events'`の返り値の配列数も10であることを確認するテストを書いて下さい。
1. よって、`'results_returned'`の返り値は`'events'`の返り値の配列数と同値であることを確認するテストを書いて下さい。


## 第03章 pytestのフィクスチャ
1. `@pytest.fixture` を使って、`266898` を返すフィクスチャを定義してください
1. 定義したフィクスチャを使用してアサーションを行うテストを書いてください
1. 以下のオプションをクライアントに渡してデータを取得するセットアップフィクスチャ `my_data` をスコープレベルをモジュールで書いてください
    ```bash
     event_id="273501,272790,271250,270289,269404,266898,264872" # コンマ区切りのID文字列を渡すと複数イベントを取得可
     order=2 # 開催日時順を降順（新しい順）
    ```
1.  `my_data` を使って以下のテストを書いてください
    1. `'events'`は７つであること
    1. イベントIDが上記７つのIDのと一致すること
    1. `owner_id` は全て `36417` であること
    1. 開催日時順が降順で返ってきていること


## 第04章 組み込みフィクスチャ

1. 以下は、PythonでCSVファイルをSQLiteデータベースに変換する例のコードです。(ChatGPT に書いてもらいました。)
    ```python 
    import csv
    import sqlite3

    # CSVファイルのパス
    csv_file = 'example.csv'
    # SQLiteデータベースのパス
    sqlite_file = 'example.db'

    # CSVファイルの読み込み
    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        header = next(reader)
        rows = [row for row in reader]

    # SQLiteデータベースへの接続
    conn = sqlite3.connect(sqlite_file)
    cursor = conn.cursor()

    # テーブルの作成
    table_name = 'example_table'
    cursor.execute(f'DROP TABLE IF EXISTS {table_name}')
    cursor.execute(f'CREATE TABLE {table_name} ({", ".join(header)})')

    # CSVデータの挿入
    for row in rows:
        cursor.execute(f'INSERT INTO {table_name} VALUES ({",".join(["?" for i in range(len(header))])})', row)

    # 変更の保存とデータベースの接続の終了
    conn.commit()
    conn.close()

    ```
    以下は `connpass_client` を使って取得したデータを csv file へ書き出すコード例です。

    ```python
    from connpass_client import ConnpassClient, Writer
    cli = ConnpassClient()
    series_id = "5944"
    data = cli.get(series_id=series_id)
    Writer(data).to_csv("/tmp/series_id_5944.csv")
    ```
    この２つのコード例を参考に、client で取得したデータを一時ディレクトリにCSVとして保存した後、SQLITEへ挿入しするセットアップを書いてみましょう。一時ディレクトリは組み込みフィクスチャーである `tmp_path_factory` を使いましょう。テストが終わったら、一時ディレクトリ毎削除するティアダウンも書きましょう。このフィクスチャは conftest.py に記述してください。
1. 以下は、Python で SQLite データベースをクエリする簡単な例です。(ChatGPT に書いてもらいました。)
    ```python
    import sqlite3

    conn = sqlite3.connect("example.db")
    cursor = conn.cursor()

    # SELECT statement
    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()
    for row in rows:
        print(row)

    conn.close()

    ```
    このコード例を参考にして作成したDBを使ったテストを書いてみましょう。


## 第05章 パラメータ化



