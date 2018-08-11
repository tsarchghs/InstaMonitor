from flask import Flask,request,render_template,url_for,session
from flask_session import Session
from InstagramAPI import InstagramAPI
import os

app = Flask(__name__)
SESSION_TYPE = 'filesystem'
sess = Session(app)

@app.route('/login',methods=["GET","POST"])
def login():
	if request.method == "GET":
		return render_template("auth/login.html")
	elif request.method == "POST":
		username = request.form["username"]
		password = request.form["password"]
		api = InstagramAPI(username,password)
		user = api.login()
		if user:
			session["logged_in"] = True
			return url_for("index")
		else:
			return render_template("auth/login.html",invalid_credentials=True)
		return 0

@app.route('/index')
def index():
	pass

if __name__ == "__main__":
    app.secret_key = '<?>'
    app.config['SESSION_TYPE'] = SESSION_TYPE

    sess.init_app(app)
    app.debug = True
    app.run(port=8000)