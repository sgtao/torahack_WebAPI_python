# torahack_WebAPI_python
- Youtube【とらゼミ】チャンネルのWebAPI講座をPythonで実装してみる
  *  refer Youtube１ : [「Re:ゼロから始めるWeb API入門【基礎編】」](https://www.youtube.com/playlist?list=PLX8Rsrpnn3IVsi0NIDP3yRlFCS0uOZdqv)
  *  refer Youtube２ : [「Re:ゼロから始めるWeb API入門【実践編】」](https://www.youtube.com/watch?v=9GGRICOjA4c&list=PLX8Rsrpnn3IVW5P1H1s_AOP0EEyMyiRDA)
  * refer GitHub : https://github.com/deatiger/basic-rest-api
  * refer web-dev-qa-db-ja : 『[Flaskで静的ファイルを提供する方法](https://www.web-dev-qa-db-ja.com/ja/python/flask%E3%81%A7%E9%9D%99%E7%9A%84%E3%83%95%E3%82%A1%E3%82%A4%E3%83%AB%E3%82%92%E6%8F%90%E4%BE%9B%E3%81%99%E3%82%8B%E6%96%B9%E6%B3%95/1044299462/)』

## 設計物

### APIサーバの構築

- 下のURI のサービス応答を実現する

| メソッド | URI | 詳細 |
|:------|:-----:|------:|
| GET   | /api/v1/users   | ユーザリストの取得 |
| GET   | /api/v1/users/123   | ユーザ情報の取得 |
| POST  | /api/v1/users   | 新規ユーザの作成 |
| PUT   | /api/v1/users/123   | ユーザ情報の更新 |
| DELETE | /api/v1/users/123   | ユーザの削除 |
| GET   | /api/v1/search?q=hoge   | ユーザ検索結果の取得 |

- エラー発生時の応答

| ステータスコード | テキストフレーズ | 意味・特徴 |
|:------|:-----:|------:|
| 200   | OK | リクエストの成功を示す |
| 201   | Created | リソース作成・更新の成功を示す |
| 400   | Bad Request | リクエストの構文やパラメータの誤りを示す |
| 404   | Not Found | リソースが存在しない／URLの解釈失敗などを示す |
| 500   | Internal Server Error | サーバ側でのエラー発生を示す |


#### (参考）ステータスコード大分類

| ステータスコード | 意味 | 詳細 |
|:------|:-----:|------:|
| 1xx   | 処理中 | 処理の継続を示す。<br>クライアントがリクエストを継続するか再送信する |
| 2xx   | 成功   | リクエストの成功を示す |
| 3xx   | リダイレクト | 他リソースへの移行を示す。<br>`Location`ヘッダから新たなリソースへ接続する |
| 4xx   | クライアントエラー | クライアントのリクエストが原因のエラーを示す |
| 5xx   | サーバーエラー | サーバ側のエラー発生を示す |




### DBの準備

- DBに`Users`テーブルを作成する

| フィールド名 | データ型 | NULL許容(必須) | 備考 |
|:------|:-----:|:-----:|------:|
| id | INTEGER | NOT NULL | PRIMARY KEY |
| name | TEXT | NOT NULL |   |
| profile | TEXT |   |   |
| date_of_birth | TEXT |   |   |
| created_at | TEXT | NOT NULL  | datetimeで日付を自動取得  |
| updated_at | TEXT | NOT NULL  | datetimeで日付を自動取得  |


### 初期DBの準備

- torahackさんの[提供コンテンツの手順](https://github.com/deatiger/basic-rest-api/blob/develop/README.md)を利用させていただく


#### Create users table
```sql
/**
 * コマンドラインで実行：
 * sqlite3 db/database.sqlite3
 * 終了するときは、".exit" を入力
 */
CREATE TABLE users (
  id INTEGER NOT NULL PRIMARY KEY,
  name TEXT NOT NULL,
  profile TEXT,
  created_at TEXT NOT NULL DEFAULT (DATETIME('now', 'localtime')),
  updated_at TEXT NOT NULL DEFAULT (DATETIME('now', 'localtime')),
  date_of_birth TEXT
);
```

#### Create sample data
```sql
INSERT INTO users (name, profile) VALUES ("Subaru", "エミリアたんマジ天使！");
INSERT INTO users (name, profile) VALUES ("Emilia", "もう、スバルのオタンコナス！");
INSERT INTO users (name, profile) VALUES ("Ram", "いいえお客様、きっと生まれて来たのが間違いだわ");
INSERT INTO users (name, profile) VALUES ("Rem", "はい、スバルくんのレムです。");
INSERT INTO users (name, profile) VALUES ("Roswaal", "君は私になーぁにを望むのかな？");
```

#### Fetch all data from users table
```sql
.schema
SELECT * FROM users;
.exit
```

## クライアント（Webサイト）
- 講座では同一オリジン内でウェブサービスを立ち上げており、同じ方法に従う
  * **Blueprint**や**WSGI**は利用せず、`app.py`単体で立ち上げる
```python
@app.route('/')
def index():
    content = get_public_file('index.html')
    return Response(content, mimetype="text/html")
#
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(public_dir(),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')
#
@app.route('/<path:path>')
def get_resource(path):  # pragma: no cover
    mimetypes = {
        ".css": "text/css",
        ".html": "text/html",
        ".js": "application/javascript",
    }
    complete_path = os.path.join(public_dir(), path)
    ext = os.path.splitext(path)[1]
    # print('request file extention is ', ext)
    mimetype = mimetypes.get(ext, "text/html")
    content = get_public_file(complete_path)
    return Response(content, mimetype=mimetype)
#
```

## LICENSE
The source code is licensed MIT.
