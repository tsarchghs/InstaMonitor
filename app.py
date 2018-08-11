from flask import Flask,request,render_template,url_for,session,redirect
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from InstagramAPI import InstagramAPI
import os
from datetime import datetime

app = Flask(__name__)
db = SQLAlchemy(app)
SESSION_TYPE = 'filesystem'
sess = Session(app)
API_URL = 'https://i.instagram.com/api/v1/'
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + str(os.getcwd()) + "/db.sqlite3"

class userFollowData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username_id = db.Column(db.Integer, unique=True, nullable=False)
    followers = db.Column(db.String(4294000000))
    followings = db.Column(db.String(4294000000))
    created = db.Column(db.DateTime, nullable=False,
        default=datetime.utcnow) 
    def __repr__(self):
        return '<userFollowData %r>' % self.id
db.create_all()

@app.route('/login',methods=["GET","POST"])
def login():
	if "logged_in" in session:
		if session["logged_in"]:
			return redirect(url_for("index"))
	if request.method == "GET":
		return render_template("auth/login.html")
	elif request.method == "POST":
		username = request.form["username"]
		password = request.form["password"]
		api = InstagramAPI(username,password)
		user = api.login()
		if user:
			session["logged_in"] = True
			session["api"] = api
			return redirect(url_for("index"))
		else:
			return render_template("auth/login.html",invalid_credentials=True)

@app.route("/logout")
def logout():
	session["logged_in"] = False
	session["api"] = False
	return redirect(url_for("login"))

@app.route('/index')
def index():
	if not "logged_in" in session:
		return redirect(url_for("login"))
	if "logged_in" in session:
		if not session["logged_in"]:
			return redirect(url_for("login"))
	session["api"].getProfileData()
	user_info = session["api"].LastJson
	return render_template("index.html",user_info=user_info)

if __name__ == "__main__":
    app.secret_key = '<?>'
    app.config['SESSION_TYPE'] = SESSION_TYPE

    sess.init_app(app)
    app.debug = True
    app.run(port=8000)