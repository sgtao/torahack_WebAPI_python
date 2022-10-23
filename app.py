# app.py
# - 下のURI のサービス応答を実現する
# | メソッド | URI | 詳細 |
# |:------|:-----:|------:|
# | GET   | /api/v1/users   | ユーザリストの取得 |
# | GET   | /api/v1/users/123   | ユーザ情報の取得 |
# | GET   | /api/v1/search?q=hoge   | ユーザ検索結果の取得 |
# | POST  | /api/v1/users   | 新規ユーザの作成 |
# | PUT   | /api/v1/users/123   | ユーザ情報の更新 |
# | DELETE | /api/v1/users/123   | ユーザの削除 |
# 
import os
import os.path
import json
import sqlite3
from flask import Flask, request, Response
from flask import send_from_directory, jsonify
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
    # SQL処理：
    read_data = pd.read_sql(sql, conn)
    cur.close()
    # print(read_data)
    dict_data = read_data.to_dict(orient="index")
    items = []
    for item in dict_data.values():
        items.append(item)
    result = json.dumps(items)
    #
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
    conn.close()
    #
    # print(result)
    # print(len(result))
    #
    if (len(result)>0):
        return result[0], 200
    else:
        response = {
            "code": 404,
            # "type": "Not Found",
            "message": "Not Found!",
        }
        print(response)
        return jsonify({'message':response['message']}), response['code']
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
# for POST/PUT/DELETE Request
def run_database(conn, sql):
    cur = conn.cursor()
    try:
        cur.execute(sql)
        conn.commit()
        print("Query success")
    except Exception as e:
        print("Query failed at sql:" + sql)
        raise(e)
    finally:
        cur.close()
    return
#
# add a new user
@app.route('/api/v1/users',methods=["POST"])
def post_user():
    req_json = json.loads(request.get_data())
    # print(req_json)
    # Error Check (name is exist?)
    if req_json['name'] is None or req_json['name'] == "":
        response = {
            "code": 400,
            # "type": "Bad Request",
            "message": "UserName is not Set!",
        }
        print(response)
        return jsonify({ 'message': response['message']}), response['code']
    #
    # data set for SQL command
    name = req_json['name']
    # profile = req_json['profile'] if req_json['profile']  is not "" else ""
    if req_json['profile']  != "":
        profile = req_json['profile']
    else:
        profile = ""
    # dateOfBirth = req_json['date_of_birth'] if req_json['date_of_birth'] is not "" else ""
    if req_json['date_of_birth'] != "":
        dateOfBirth =  req_json['date_of_birth']
    else:
        dateOfBirth = ""
    #
    conn = get_connect()
    sql = 'INSERT INTO users (name, profile, date_of_birth) VALUES ('
    sql += '"' + name + '", "' + profile+ '", "' + dateOfBirth + '")'
    # print(sql)
    try:
        run_database(conn, sql)
        response = {
            "code": 201,
            "message": "新規ユーザーを作成しました。",
        }
    except Exception as e:
        print('error:' + str(e))
        response = {
            "code": 500,
            "message": str(e),
        }
    finally:
        conn.close()
    #
    return jsonify({ 'message': response['message']}), response['code']
#
# update a existing user
@app.route("/api/v1/user/<int:user_id>",methods=["PUT"])
def put_user(user_id):
    req_json = json.loads(request.get_data())
    # print(req_json)
    # Error Check (name is exist?)
    if req_json['name'] is None or req_json['name'] == "":
        response = {
            "code": 400,
            # "type": "Bad Request",
            "message": "UserName is not Set!",
        }
        print(response)
        return jsonify({'message': response['message']}), response['code']
    #
    # Error Check: 指定ユーザがいるか？を確認
    check_user_id = get_user_info(user_id)
    # print(check_user_id[1])
    if (check_user_id[1] == 404):
        response = {
            "code": 404,
            # "type": "NOT FOUND",
            "message": "指定されたユーザーが見つかりません。",
        }
        print(response)
        return jsonify({'message': response['message']}), response['code']
    #
    # data set for SQL command
    name = req_json['name']
    # profile = req_json['profile'] if req_json['profile']  is not "" else ""
    if req_json['profile']  != "":
        profile = req_json['profile']
    else:
        profile = ""
    # dateOfBirth = req_json['date_of_birth'] if req_json['date_of_birth'] is not "" else ""
    if req_json['date_of_birth'] != "":
        dateOfBirth =  req_json['date_of_birth']
    else:
        dateOfBirth = ""
    #
    conn = get_connect()
    sql  = 'UPDATE users SET name="' + name + '", '
    sql += ' profile="' + profile + '", date_of_birth="' + dateOfBirth 
    sql += '" WHERE id=' + str(user_id)
    # print(sql)
    try:
        run_database(conn, sql)
        response = {
            "code": 201,
            "message": "ユーザー情報を更新しました。",
        }
    except Exception as e:
        print('error:' + str(e))
        response = {
            "code": 500,
            "message": str(e),
        }
    finally:
        conn.close()
    #
    return jsonify({ 'message': response['message']}), response['code']
#
#
# delete a existing user
@app.route("/api/v1/user/<int:user_id>",methods=["DELETE"])
def delete_user(user_id):
    # req_json = json.loads(request.get_data())
    # print(req_json)
    #
    # Error Check: 指定ユーザがいるか？を確認
    check_user_id = get_user_info(user_id)
    # print(check_user_id[1])
    if (check_user_id[1] == 404):
        response = {
            "code": 404,
            "message": "指定されたユーザーが見つかりません。",
        }
        print(response)
        return jsonify({'message': response['message']}), response['code']
    #
    conn = get_connect()
    sql  = 'DELETE FROM users WHERE id=' + str(user_id)
    # print(sql)
    run_database(conn, sql)
    #
    conn.close()
    return jsonify({ 'message': "ユーザー情報を更新しました。"}), 201
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
    return send_from_directory(
        public_dir(),
        'favicon.ico',
        mimetype='image/vnd.microsoft.icon'
    )
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