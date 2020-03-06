#Flaskとrender_template（HTMLを表示させるための関数）をインポート
from flask import Flask,render_template,request,redirect,url_for,send_from_directory,session
from app.models.models import Member
from app.models.models import News
from app.models.database import db_session
from datetime import datetime
from werkzeug import secure_filename
from app import key 
import os
#Flaskオブジェクトの生成
app = Flask(__name__)
app.secret_key = key.getSessionKey()

### 基本ページ
@app.route("/top")
def top():
    return render_template("top.html")

@app.route("/member")
def member():
    all_member = Member.query.all()
    return render_template("member.html",all_member=all_member)

@app.route("/news")
def news():
    all_news = News.query.all()
    all_news = sorted(all_news, key=lambda u: u.date,reverse=True)
    return render_template("news.html",all_news=all_news)

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/twitter")
def twitter():
    return render_template("twitter.html")

### 管理者ログイン

@app.route("/admin", methods = ["get"])
def admin():
    return render_template("admin.html")

@app.route("/admin",methods=["post"])
def login():
    password = request.form["password"]
    if password == key.getAdminKey():
        session["admin"] = "admin"
        return redirect("/edit")
    else:
        return render_template("admin.html",alert="Not correct pass")

@app.route("/logout")
def logout():
    session.pop("admin", None)
    return redirect("/admin")


### 管理者系処理

@app.route("/edit")
def edit():
    if "admin" in session:
        all_member = Member.query.all()
        all_news = News.query.all()
        return render_template("edit.html", all_member=all_member, all_news=all_news)
    else :
        return redirect("/admin")
## ファイルアップロード
UPLOAD_FOLDER = './app/static/member_images'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/member_add",methods =["post"])
def member_add():
    name = request.form["name"]
    img_file = request.files['member_image']
    twitter = request.form["twitter"]
    content = Member(name,twitter)
    db_session.add(content)
    db_session.commit()
    member = Member.query.filter_by(name=name).first()
    filename = str(member.id)+".png"
    img_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    return redirect("/edit")


@app.route("/member_del", methods =["post"])
def member_del():
    id_list = request.form.getlist("del")
    for id in id_list:
        content = Member.query.filter_by(id=id).first()
        db_session.delete(content)
    db_session.commit()
    return redirect("/edit")

@app.route("/news_add", methods =["post"])
def news_add():
    date = request.form["date"]
    text = request.form["text"]
    content = News(date,text)
    db_session.add(content)
    db_session.commit()
    return redirect("/edit")


@app.route("/news_del", methods =["post"])
def news_del():
    id_list = request.form.getlist("del")
    for id in id_list:
        content = News.query.filter_by(id=id).first()
        db_session.delete(content)
    db_session.commit()
    return redirect("/edit")


#おまじない
if __name__ == "__main__":
    app.run(debug=True)

    