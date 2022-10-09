# app.py
# - 下のURI のサービス応答を実現する
# | メソッド | URI | 詳細 |
# |:------|:-----:|------:|
# | GET   | /api/v1/users   | ユーザリストの取得 |
# 
import os
import sqlite3
from flask import Flask,render_template,request,g
#
app = Flask(__name__)
dbname = 'db/database.sqlite3'
#
def get_connect(conn = ""):
    if conn == "":
        # データベースをオープンしてFlaskのグローバル変数に保存
        return sqlite3.connect(dbname)
    conn.row_factory = row_to_dict
    return conn
#
def row_to_dict(cursor: sqlite3.Cursor, row: sqlite3.Row) -> dict:
    data = {}
    for idx, col in enumerate(cursor.description):
        data[col[0]] = row[idx]
    return data
#
# get users list
@app.route("/api/v1/users")
def userslist():
    # データベースを開く
    conn = get_connect()
    cur = conn.cursor()
    sql = 'SELECT * FROM users'
    data = conn.execute(sql)
    result = data.fetchall()
    # print(result)
    #
    cur.close()
    conn.close()
    return result
#
# get a user
@app.route("/api/v1/user/<int:user_id>", methods=["GET"])
def userinfo(user_id):
    # データベースを開く
    conn = get_connect()
    cur = conn.cursor()
    sql = 'SELECT * FROM users WHERE id = ' + str(user_id)
    data = conn.execute(sql)
    result = data.fetchall()
    # print(result)
    #
    cur.close()
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
    # conn = get_connect()
    # cur = conn.cursor()
    # # terminalで実行したSQL文と同じようにexecute()に書く
    # cur.execute('SELECT * FROM users')
    # print(cur.fetchall())
    # #
    # cur.close()
    # conn.close()
    main()
#
# EOF