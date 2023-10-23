from flask import Flask, render_template, request, url_for, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"
app.config["SECRET_KEY"] = "fpoijaf984qiub98rtbnusp9uwrnb150vmpautj"
db = SQLAlchemy()

login_manager = LoginManager()
login_manager.init_app(app)


class Users(UserMixin, db.Model):
	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(250), unique=True, nullable=False)
	name = db.Column(db.String(250))
	password = db.Column(db.String(250), nullable=False)


db.init_app(app)


with app.app_context():
	db.create_all()


@login_manager.user_loader
def loader_user(user_id):
	return Users.query.get(user_id)

@app.route("/")
def home():
	return render_template("home.html")

@app.route('/register', methods=["GET", "POST"])
def register():
	if request.method == "POST":
		user = Users(email=request.form.get("email"),
			   		name=request.form.get("name"),
					password=generate_password_hash(request.form.get("password"), method='scrypt'))
		db.session.add(user)
		db.session.commit()
		return redirect(url_for("login"))
	return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
	if request.method == "POST":
		user = Users.query.filter_by(
			email=request.form.get("email")).first()
		if not (user and check_password_hash(user.password, request.form.get("password"))) :
			flash("Bad login.  Try again.")
			return redirect(url_for("home"))
		login_user(user)
		return redirect(url_for("studies"))
	return render_template("login.html")

@app.route("/logout")
def logout():
	logout_user()
	return redirect(url_for("home"))

@app.route('/studies')
@login_required
def studies():
    return render_template('studies.html', name=current_user.name)

if __name__ == "__main__":
	app.run()
