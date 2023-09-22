from flask import Flask,render_template,request,redirect,url_for,session
import sqlite3 as sql
from pytube import extract

app = Flask(__name__)

app.secret_key = "jef123"

def isloggedin():
    return "email" in session

@app.route('/signup', methods = ["GET","POST"])
def signup():
    if request.method == "POST":
        con = sql.connect("user.db")
        cur = con.cursor()
        cur.execute("insert into login (username,dob,email,password) values(?,?,?,?)",
                    (request.form.get("username"),request.form.get("dob"),
                     request.form.get("email"),request.form.get("password")))
        con.commit()
        

        return redirect (url_for('login'))
    return render_template ("signup.html")

@app.route('/', methods = ["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        con = sql.connect("user.db")
        cur = con.cursor()
        cur.execute("select * from login where email=? and password=?",
                    (email,password))
        fet = cur.fetchall()
        for i in fet:
            # email1 = i[2]
            # pass1 = i[3]
            if email in i and password == i[3]:
                session["email"] = email
                return redirect(url_for('youtube'))
            else:
                return "Incorrect email of password"

    return render_template ("login.html")

@app.route('/youtube')
def youtube():
    con = sql.connect("user.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM UPLOAD")
    fet = cur.fetchall()
    return render_template ("youtube.html", box = fet)



@app.route('/upload', methods = ["GET","POST"])
def upload():
    if request.method == "POST":
        videourl = request.form.get("video")
        videoid = extract.video_id(videourl)

        thumbnail = request.form.get("thumb")
        title = request.form.get("title")
        con = sql.connect("user.db")
        cur = con.cursor()
        cur.execute("insert into upload (videourl,thumburl,title) values(?,?,?)",
                    (videoid,thumbnail,title))
        con.commit()
        return redirect (url_for('youtube'))
    return render_template ("upload.html")

@app.route('/video/<var>')
def video(var):
    return render_template ("video.html",VAR = var)


@app.route('/windies')
def windies():
    return render_template ("windies.html")


@app.route('/shorts')
def shorts():
    return render_template ("shorts.html")

@app.route('/logout')
def logout():
    session.pop("email")
    return redirect (url_for('login'))



if __name__ == "__main__":
    app.run(debug=True)