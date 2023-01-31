# 練習課題


## Pytestの練習

以下のテストを書いてみましょう(全部書く必要はありません。)

- 2つの数字を足して答えが正しいことを確認する
- 2つの数字を引いて答えが正しいことを確認する
- 2つの文字列が等しいことを確認する
- 2つのリストが等しいことを確認する
- 正の数字が正の数字であることを確認する
- 負の数字が負の数字であることを確認する
- 3で割り切れる数字が3で割り切れることを確認する
- 3で割り切れない数字が3で割り切れないことを確認する

## connpass_clientを使った connpass api テスト


### conftest.py に セットアップとティアダウンを記述

```{attention}
connpass の規約を守るために、 `connpass_client` を使う時は、リクエストは５秒以上間隔を開けて行う工夫をしましょう。たとえばセットアップもしくはティアダウンのタイミングで `time.sleep(5)` 記述するのは良い方法かもしれません。
```

1. `event_id="266898"` をリクエストするフィクスチャ `an_event_data` を書いてください。
1. `event_id='273501,272790,271250,270289,269404,266898,264872'` と `order=2` オプションに入れてリクエストするフィクスチャ `some_events_data` を書いてください。


### 一つのイベントリクエストに対するテスト

an_event_data フィクスチャを使って以下のテストを書いてみましょう

1. an_event_data のレスポンスフィールドは、`['results_start', 'results_returned', 'results_available', 'events']` である
1. `events` の配列データは１つである
1. `events` の配列データで返ってくる一つの辞書データのキーは `['event_id', 'title', 'catch', 'description', 'event_url', 'started_at', 'ended_at', 'limit', 'hash_tag', 'event_type', 'accepted', 'waiting', 'updated_at', 'owner_id', 'owner_nickname', 'owner_display_name', 'place', 'address', 'lat', 'lon', 'series']` と一致する
1. `results_returned`と `events` の配列データ数は一致する
1. `event_id="266898"` を３回リクエストし、常に同じレスポンスであること


### 複数のイベントリクエストに対するテスト

`some_events_data` フィクスチャを使って以下のテストを書いてみましょう。

1. some_events_data のレスポンスフィールドは、`['results_start', 'results_returned', 'results_available', 'events']` である
1. `events` の配列データは7つである
1. `events` の配列データで返ってくるそれぞれの辞書データのキーは `['event_id', 'title', 'catch', 'description', 'event_url', 'started_at', 'ended_at', 'limit', 'hash_tag', 'event_type', 'accepted', 'waiting', 'updated_at', 'owner_id', 'owner_nickname', 'owner_display_name', 'place', 'address', 'lat', 'lon', 'series']` と一致する
1. イベントIDがリクエストした時のID７つと一致すること
1. `results_returned`と `events` の配列データ数は一致する
1. `owner_id` は全て `36417` である
1. `events` の配列データは、開催日時順が降順(新着順)である

### テストの目的からフィクスチャを書く

以下のテストは、フィクスチャを新規に作る必要が有ります。テストにあわせてフィクスチャを作り、テストを作成してください

1. `event_id="266898"` のレスポンスをいったん CSV に書き出し、一行目が以下の一致すること。
    ```
    event_id,title,catch,description,event_url,started_at,ended_at,limit,hash_tag,event_type,accepted,waiting,updated_at,owner_id,owner_nickname,owner_display_name,place,address,lat,lon,series
    ```
    
    ```{note}
     以下は `connpass_client` を使って取得したデータを csv file へ書き出すコード例です。
    ```
    ```python
    from connpass_client import ConnpassClient, Writer
    cli = ConnpassClient()
    series_id = "5944"
    data = cli.get(series_id=series_id)
    Writer(data).to_csv("/tmp/series_id_5944.csv")
    ```
 

1. 任意の `event_id` でリクエストして、常に同じレスポンスが返ってくること
    ```{note}
    以下は任意のパラメータをフィクスチャに渡す関数例です
    ```
    ```python
    @pytest.fixture
    def custom_event_data():
        def _custom_event_data(**params):
            cli = ConnpassClient()
            return cli.get(**params)
        return _custom_event_dat

    def test_something(custom_event_data):
        data = custom_event_data(event_id = "266898")
        assert data["results_returned"] == 1
    ```
