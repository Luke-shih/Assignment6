import pymysql
from flask import Flask, request, render_template, session, url_for, redirect, session
from mysql.connector import Error
import mysql.connector
import bcrypt

app=Flask(__name__, static_folder="public", static_url_path="/")
app.secret_key = "assignmentweek6"

@app.route("/")
def homepage(): # 一進入"/"時先切換到 homepage 首頁
    return render_template("homepage.html") 

@app.route("/signup", methods = ['GET', 'POST'])
def signup():
    has_regiter = 0 # 用來記錄當前帳號是否已存在，0：不存在 1：已存在
    
    name = request.form.get('name')         # 取得輸入 form 中的 name 資料
    username = request.form.get('username') # 取得輸入 form 中的 username 資料
    password = request.form.get('password') # 取得輸入 form 中的 password 資料

    db =  pymysql.connect(host="127.0.0.1", user="root", password="1234", database="website") # 連接資料庫
    cursor = db.cursor()


    while name == "" or username == "" or password =="": # 如果沒輸入資料就案註冊，跳轉 error
        return redirect(url_for('error', message = request.args.get("message", "請輸入姓名及帳號密碼")))

    sql = "SELECT username FROM `website`.`user` WHERE username = %s ;"
    
    cursor.execute(sql, username)
    has_regiter = cursor.fetchall()

    if len(has_regiter) == 0:
        session['name'] = name
        session['username'] = username
        session['password'] = password

        global nickname # 設一個 global nickname 讓會員頁面抓
        nickname = name

        cursor.close()
        db.close()
        return redirect(url_for("member"))
    else:
        return redirect(url_for('error', message = request.args.get("message", "帳號已經被註冊過")))

@app.route('/signin', methods=["POST", "GET"])
def signin():
    username = request.form.get('username')
    password = request.form.get('password')

    db =  pymysql.connect(host="127.0.0.1", user="root", password="1234", database="website")
    cursor = db.cursor()

    sql = "SELECT * FROM `website`.`user` WHERE `username` =  %s and password = %s;"      
    val = (username, password)
    cursor.execute(sql, val)
    users = cursor.fetchall()
    if username == "" or password =="": # 如果沒輸入資料就案註冊，跳轉 error
        return redirect(url_for('error', message = request.args.get("message", "帳號或密碼錯誤")))
    elif len(users) > 0:
        sql = "SELECT * FROM `website`.`user` WHERE `username` = %s and password = %s;"
        val = (username, password)
        cursor.execute(sql, val)

        session['username'] = username # 將 username 加入 session 中
        session['password'] = password # 將 password 加入 session 中 

        result = cursor.fetchone()
        global nickname
        nickname = result[1] # [1]代表 name 位置
        db.close()
        return redirect(url_for('member'))
    else:
        return redirect(url_for('error', message = request.args.get("message", "帳號或密碼錯誤")))
@app.route("/member")
def member():

    if "username" in session and "password" in session:
        result = request.args.get("name", nickname)
        return render_template("member.html", data = result)
    else:
        return redirect(url_for('error', message = request.args.get("message", "帳號或密碼錯誤")))
   
@app.route("/error/") 
def error():
    message = request.args.get("message", None)
    return render_template("error.html",data = message)

@app.route("/logout")
def logout():
    session.pop("name", None)    # 將 name 清空
    session.pop("username", None)    # 將 username 清空
    session.pop("password", None)   # 將 password 清空

    return redirect(url_for("homepage"))    # 回傳到首頁

if __name__ == '__main__':
    app.run(port=3000)
