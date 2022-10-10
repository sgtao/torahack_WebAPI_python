# app.py
# - 下のURI のサービス応答を実現する
# | メソッド | URI | 詳細 |
# |:------|:-----:|------:|
# | GET   | /api/v1/users   | ユーザリストの取得 |
# | GET   | /api/v1/users/123   | ユーザ情報の取得 |
# 
import os
import os.path
import json
import sqlite3
from flask import Flask, request, Response, send_from_directory
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
# temporal web service
# refer web-dev-qa-db-ja.com
def public_dir():  # pragma: no cover
    exec_dir = os.path.abspath(os.path.dirname(__file__))
    # print(exec_dir)
    return os.path.join(exec_dir, 'public/')
#
def get_public_file(filename):  # pragma: no cover
    try:
        src = os.path.join(public_dir(), filename)
        # This should not be so non-obvious
        # - use read alternatively render_template, send_from
        return open(src).read()
    except IOError as exc:
        return str(exc)
#
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