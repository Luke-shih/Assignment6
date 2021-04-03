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
    
    name = request.form.get('name')
    username = request.form.get('username')
    password = request.form.get('password')

    db =  pymysql.connect(host="127.0.0.1", user="root", password="1234", database="website")
    cursor = db.cursor()

    sql1 = "select * from user"
    cursor.execute(sql1)
    all_users = cursor.fetchall() # 查詢到所有的數據存儲到all_users中
    i = 0
    
    while i < len(all_users):
        if username in all_users[i]:
            has_regiter = 1 # 表示該帳號已經存在
        i+= 1
    if has_regiter == 0: # 表示資料表中找不到相同的
        sql2 = "INSERT INTO `website`.`user` ( `name`, `username`, `password`) VALUES (%s, %s, %s);"

        val = (name, username, password)
        cursor = db.cursor()
        cursor.execute(sql2, val)
        db.commit()

        session['name'] = name
        session['username'] = username
        session['password'] = password

        global nickname
        nickname = name

        cursor.close()
        db.close()
        return redirect(url_for("member"))
    else:
        cursor.close()
        db.close()
        return redirect(url_for("error"))

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
    if len(users) > 0:
        sql = "SELECT * FROM `website`.`user` WHERE `username` = %s and password = %s;"
        val = (username, password)
        cursor.execute(sql, val)

        session['username'] = username
        session['password'] = password

        result = cursor.fetchone()
        global nickname
        nickname = result[1]
        db.close()
        return redirect(url_for('member'))
    else:
        return redirect(url_for("error"))

@app.route("/member")
def member():

    if "username" in session and "password" in session:
        result = request.args.get("name", nickname)
        return render_template("member.html", data = result)
    else:
        return redirect(url_for("error"))
   
@app.route("/error") # 當帳號密碼有一個不等於 test 時執行
def error():

    message = request.args.get("message", None)
    return render_template("error.html", data = message)

@app.route("/logout")
def logout():
    session.pop("name", None)    # 將 name 清空
    session.pop("username", None)    # 將 username 清空
    session.pop("password", None)   # 將 password 清空

    return redirect(url_for("homepage"))    # 回傳到首頁

# 使用__name__ == '__main__'是Python的慣用法，確保直接執行此腳本時才
# 啟動服務器，若其他程序調用該腳本可能父級程序會啟動不同的服務器
if __name__ == '__main__':
    app.run(port=3000)
