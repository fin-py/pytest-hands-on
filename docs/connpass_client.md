# connpass_client の使い方

[環境構築](docs/environment.md) を参考にconnpass_clientをインストールしてください。


## イベントを取得する

クライアントオブジェクトの .get() メソッドにオプションを渡せば、イベント情報を得ることができます。オプションについては[APIリファレンス - connpass](https://connpass.com/about/api/)を参照してください。

### 例１：`event_id = "266898"` の情報を得る

```python 
from connpass_client import ConnpassClient
from pprint import pprint

cli = ConnpassClient()
data = cli.get(event_id="266898")
pprint(data["events"])
```

結果数は `'results_available'` で得ることができ、その詳細データを `'events'` で得ることができます。


```bash
{'results_available': 1,
 'results_returned': 1,
 'results_start': 1
 'events': [{'accepted': 15,
             'address': '',
             'catch': 'CHAPTER 2 テスト関数を書く',
             'description': '<h1>概要</h1>\n' ...... ,
             'ended_at': '2022-11-30T20:30:00+09:00',
             'event_id': 266898,
             'event_type': 'participation',
             'event_url': 'https://fin-py.connpass.com/event/266898/',
             'hash_tag': '',
             'lat': None,
             'limit': None,
             'lon': None,
             'owner_display_name': 'driller',
             'owner_id': 36417,
             'owner_nickname': 'driller',
             'place': 'オンライン(Brave Talk)',
             'series': {'id': 3056,
                        'title': 'fin-py',
                        'url': 'https://fin-py.connpass.com/'},
             'started_at': '2022-11-30T19:30:00+09:00',
             'title': 'テスト駆動Python 第2版 読書会#1',
             'updated_at': '2022-11-30T16:30:02+09:00',
             'waiting': 0}],
}

```

### 例２：`owner_nickname="driller", keyword_or="もくもく"` の情報を得る

```python
from connpass_client import ConnpassClient
from pprint import pprint

cli = ConnpassClient()
data = cli.get(owner_nickname="driller", keyword_or="もくもく")
pprint(data)
```


```bash
{'results_available': 78,
 'results_returned': 10,
 'results_start': 1
 'events': [{'accepted': 8,
             'address': '',
             'catch': 'finの人もpyの人も、ガチ勢もゆる勢も',
             'description': "......",
             'started_at': '2023-02-04T10:00:00+09:00',
             'title': '【オンライン開催】fin-pyもくもく会 #65',
             ..... },
            {'accepted': 7,
             'address': '',
             'catch': 'finの人もpyの人も、ガチ勢もゆる勢も',
             'description':  "......",
             'ended_at': '2023-01-07T13:00:00+09:00',
             'event_id': 269405,
             'started_at': '2023-01-07T10:00:00+09:00',
             'title': '【オンライン開催】fin-pyもくもく会 #64',
             ..... },
            {'accepted': 8,
             'address': '',
             'catch': 'finの人もpyの人も、ガチ勢もゆる勢も',
             'description':  "......",
             'event_id': 266421,
             'event_type': 'participation',
             'started_at': '2022-12-10T10:00:00+09:00',
             'title': '【オンライン開催】fin-pyもくもく会 #63',
             .....},
             
             .....
             ],
}
 ```