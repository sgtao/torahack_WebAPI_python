# torahack_WebAPI_python
- Youtube【とらゼミ】チャンネルのWebAPI講座をPythonで実装してみる
  *  refer Youtube１ : [「Re:ゼロから始めるWeb API入門【基礎編】」](https://www.youtube.com/playlist?list=PLX8Rsrpnn3IVsi0NIDP3yRlFCS0uOZdqv)
  *  refer Youtube２ : [「Re:ゼロから始めるWeb API入門【実践編】」](https://www.youtube.com/playlist?list=PLX8Rsrpnn3IVsi0NIDP3yRlFCS0uOZdqv)
  - refer GitHub : https://github.com/deatiger/basic-rest-api

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
`INSERT INTO users (name, profile) VALUES ("Subaru", "エミリアたんマジ天使！");`
`INSERT INTO users (name, profile) VALUES ("Emilia", "もう、スバルのオタンコナス！");`
`INSERT INTO users (name, profile) VALUES ("Ram", "いいえお客様、きっと生まれて来たのが間違いだわ");`
`INSERT INTO users (name, profile) VALUES ("Rem", "はい、スバルくんのレムです。");`
`INSERT INTO users (name, profile) VALUES ("Roswaal", "君は私になーぁにを望むのかな？");`

#### Fetch all data from users table
`SELECT * FROM users;`

