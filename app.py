# app.py
# - 下のURI のサービス応答を実現する
# | メソッド | URI | 詳細 |
# |:------|:-----:|------:|
# | GET   | /api/v1/users   | ユーザリストの取得 |
# | GET   | /api/v1/users/123   | ユーザ情報の取得 |
# 
import os
import json
import sqlite3
from flask import Flask,render_template,request,g
import pandas as pd
#
app = Flask(__name__)
dbname = 'db/database.sqlite3'
item_keys = {'id', 'name', 'profile', 'created_at', 'updated_at', 'date_of_birth'}
#
def get_connect(conn = ""):
    if conn == "":
        # データベースをオープンしてFlaskのグローバル変数に保存
        return sqlite3.connect(dbname)
    # conn.row_factory = dict_factory
    return conn
#
def dict_factory(cursor, row):
   d = {}
   for idx, col in enumerate(cursor.description):
       d[col[0]] = row[idx]
   return d
#
def get_jsondata_from_sql(conn, sql):
    cur = conn.cursor()
    data = conn.execute(sql)
    result = data.fetchall()
    # read_data = pd.read_sql(sql, conn).transpose()
    read_data = pd.read_sql(sql, conn)
    # print(read_data)
    dict_data = read_data.to_dict(orient="index")
    items = []
    for item in dict_data.values():
        # print(item)
        items.append(item)
    # result = json.dumps(items, indent=4, ensure_ascii=False)
    result = json.dumps(items)
    # print(result)
    #
    cur.close()
    return json.loads(result)
#
# get users list
@app.route("/api/v1/users")
def userslist():
    # データベースを開く
    conn = get_connect()
    sql = 'SELECT * FROM users'
    result = get_jsondata_from_sql(conn, sql)
    # print(result)
    #
    conn.close()
    return result
#
# get a user
@app.route("/api/v1/user/<int:user_id>", methods=["GET"])
def userinfo(user_id):
    # データベースを開く
    conn = get_connect()
    sql = 'SELECT * FROM users WHERE id = ' + str(user_id)
    result = get_jsondata_from_sql(conn, sql)
    # print(result)
    #
    conn.close()
    return result[0]
#
# run after setup
def main():
    """main
    """
    host = os.getenv('HOST', '0.0.0.0')
    port = int(os.getenv('PORT', '5000'))
    app.run(host=host, port=port)
#
if __name__ == '__main__':
    # # test DB --start--
    # conn = get_connect()
    # # cur = conn.cursor()
    # # terminalで実行したSQL文と同じようにexecute()に書く
    # # cur.execute('SELECT * FROM users')
    # # data = cur.fetchone()
    # # result = dict(zip(item_keys, data))
    # # data = pd.read_sql('SELECT * FROM users', conn)
    # # data = pd.read_sql('SELECT * FROM users WHERE id = 1', conn)
    # # result = data.transpose().to_dict()
    # # print(json.dumps(result, ensure_ascii=False))
    # sql = 'SELECT * FROM users WHERE id = 1'
    # print(get_jsondata_from_sql(conn, sql))
    # # print(result)
    # # cur.close()
    # conn.close()
    # # test DB -- end --
    main()
#
# EOF