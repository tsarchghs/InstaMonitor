from flask import Flask,request,render_template,url_for,session,redirect
from flask_session import Session
from InstagramAPI import InstagramAPI
import os

app = Flask(__name__)
SESSION_TYPE = 'filesystem'
sess = Session(app)
API_URL = 'https://i.instagram.com/api/v1/'

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
			session["username_id"] = api.username_id
			session["username"] = username
			session["password"] = password
			return redirect(url_for("index"))
		else:
			return render_template("auth/login.html",invalid_credentials=True)

@app.route("/logout")
def logout():
	session["logged_in"] = False
	session["username_id"] = False
	session["username"] = False
	session["password"] = False
	return redirect(url_for("login"))

@app.route('/index')
def index():
	if not "logged_in" in session:
		return redirect(url_for("login"))
	if "logged_in" in session:
		if not session["logged_in"]:
			return redirect(url_for("login"))
	api = InstagramAPI(session["username"],session["password"])
	api.login()
	api.getProfileData()
	user_info = api.LastJson
	return render_template("index.html",user_info=user_info)

if __name__ == "__main__":
    app.secret_key = '<?>'
    app.config['SESSION_TYPE'] = SESSION_TYPE

    sess.init_app(app)
    app.debug = True
    app.run(port=8000)