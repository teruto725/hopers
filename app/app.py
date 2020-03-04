#Flaskとrender_template（HTMLを表示させるための関数）をインポート
from flask import Flask,render_template,request,redirect
from app.models.models import Member
from app.models.models import News
from app.models.database import db_session
from datetime import datetime

#Flaskオブジェクトの生成
app = Flask(__name__)

#「/」へアクセスがあった場合に、"Hello World"の文字列を返す
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
    return render_template("news.html",all_news=all_news)

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/admin", methods = ["get"])
def admin():
    return render_template("admin.html")

@app.route("/admin",methods=["post"])
def login():
    password = request.form["password"]
    if password == "0302":
        return redirect("/edit")
    else:
        return render_template("admin.html",alert="Not correct pass")

@app.route("/edit")
def edit():
    all_member = Member.query.all()
    all_news = News.query.all()
    return render_template("edit.html", all_member=all_member, all_news=all_news)

@app.route("/member_add",methods =["post"])
def member_add():
    name = request.form["name"]
    twitter = request.form["twitter"]
    content = Member(name,twitter)
    db_session.add(content)
    db_session.commit()
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

    