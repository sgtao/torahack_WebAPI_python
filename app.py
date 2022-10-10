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
from flask import Flask, request
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
    return conn
#
def get_jsondata_from_sql(conn, sql):
    cur = conn.cursor()
    data = conn.execute(sql)
    result = data.fetchall()
    read_data = pd.read_sql(sql, conn)
    dict_data = read_data.to_dict(orient="index")
    items = []
    for item in dict_data.values():
        items.append(item)
    result = json.dumps(items)
    #
    cur.close()
    return json.loads(result)
#
# get users list
@app.route("/api/v1/users")
def get_users_list():
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
def get_user_info(user_id):
    # データベースを開く
    conn = get_connect()
    sql = 'SELECT * FROM users WHERE id = ' + str(user_id)
    result = get_jsondata_from_sql(conn, sql)
    # print(result)
    #
    conn.close()
    return result[0]
#
# search user
@app.route("/api/v1/search", methods=["GET"])
def search_user():
    keyword = request.args.get("q")
    # print("search with " + keyword)
    # データベースを開く
    conn = get_connect()
    sql = 'SELECT * FROM users WHERE name LIKE "%' + str(keyword) + '%"'
    result = get_jsondata_from_sql(conn, sql)
    # print(result)
    #
    conn.close()
    return result
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
    main()
#
# EOF