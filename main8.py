from flask import Flask, render_template, request, url_for, redirect, flash, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user

db = SQLAlchemy()
app = Flask(__name__)

app.config['SECRET_KEY'] = 'any-secret-key-you-choose'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return db.session.query(User).get(int(user_id))

##CREATE TABLE IN DB
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    #Every render_template has a logged_in variable set.
    return render_template("index8.html", logged_in=current_user.is_authenticated)

@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == 'POST':
        data = request.form
        email = data['email']

        if db.session.query(User).filter_by(email=email).first():
            #User already exist
            flash("You've already signed up with that email, log in instead!")
            return redirect(url_for('login'))

        hash_and_salted_password = generate_password_hash(
            data.get('password'),
            method='pbkdf2:sha256',
            salt_length=8
        )
        user = User()
        user.email = data['email']
        user.name = data['name']
        user.password = hash_and_salted_password

        db.session.add(user)
        db.session.commit()

        #Log in and authenticate user after adding details to database
        login_user(user)

        return redirect(url_for('secrets'))
    return render_template("register.html", logged_in=current_user.is_authenticated)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.form
        email = data['email']
        password = data['password']

        #Find user by email entered
        user = db.session.query(User).filter_by(email=email).first()
        #Email doesn't exist or password incorrect
        if not user:
            flash("That email does not exist, try again!")
            return redirect(url_for('login'))
        #Check stored password hash against entered password hashed
        elif not check_password_hash(user.password, password):
            flash("Password incorrect, try again!")
            return redirect(url_for('login'))
        #Email exists and password correct
        else:
            login_user(user)
            return redirect(url_for('secrets'))
    return render_template("login8.html", logged_in=current_user.is_authenticated)


@app.route('/secrets')
@login_required
def secrets():
    print(current_user.name)
    return render_template("secrets.html", name=current_user.name, logged_in=True)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/download')
@login_required
def download():
    return send_from_directory(directory='static', path="files/cheat_sheet.pdf")

if __name__ == "__main__":
    app.run(debug=True)
