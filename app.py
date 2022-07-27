import os
from dotenv import find_dotenv, load_dotenv
from flask import Flask, render_template, request
import flask
from tmdb import get_movie_details
from wiki import get_wiki_link
import random
from flask_sqlalchemy import SQLAlchemy
from flask_login import (
    LoginManager,
    login_required,
    login_user,
    UserMixin,
    current_user,
    logout_user,
)

load_dotenv(find_dotenv())
url = os.getenv("DATABASE_URL")
if url.startswith("postgres://"):
    url = url.replace("postgres://", "postgresql://", 1)

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.config["SQLALCHEMY_DATABASE_URI"] = url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = os.getenv("SECRET_KEY")
db = SQLAlchemy(app)


class Movie_logins(db.Model, UserMixin):
    __tablename__ = "Movie_logins"
    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f"<Movie_logins {self.userid}>"

    def get_userid(self):
        return self.userid


class Movie_ratings(db.Model):
    __tablename__ = "Movie_ratings"
    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.String(20), nullable=False)
    movieid = db.Column(db.Integer, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f"<Movie_ratings {self.movieid}>"


db.create_all()


@login_manager.user_loader
def load_user(user_id):
    return Movie_logins.query.get(int(user_id))


@login_manager.unauthorized_handler
def unauthorized():
    return flask.redirect(flask.url_for("login"))


@app.route("/index", methods=["GET", "POST"])
@login_required
def hello_world():

    movies_ids = ["155", "272", "49026", "293660"]
    movie_data = get_movie_details(random.choice(movies_ids))
    movie_wiki_link = get_wiki_link(movie_data["titles"])

    if request.method == "POST":
        data = request.form
        new_movie_rating = Movie_ratings(
            userid=current_user.get_userid(),
            movieid=data["movieid"],
            rating=data["rating"],
            comment=data["comment"],
        )
        db.session.add(new_movie_rating)
        db.session.commit()

    movie_comm_ratings = Movie_ratings.query.all()
    num_movies = len(movie_comm_ratings)

    return render_template(
        "index.html",
        movieid=movie_data["movieid"],
        title=movie_data["titles"],
        tagline=movie_data["taglines"],
        genres=movie_data["genres"],
        images=movie_data["movie_image"] + "/w500" + movie_data["images"],
        movie_wiki_link=movie_wiki_link,
        movie_comm_ratings=movie_comm_ratings,
        num_movies=num_movies,
    )


@app.route("/signup1")
def index():
    return render_template("signup.html")


@app.route("/signup1", methods=["GET", "POST"])
def signup1():

    data = flask.request.form.get("userid")
    user = Movie_logins.query.filter_by(userid=data).first()
    if user:
        pass
    else:
        user = Movie_logins(userid=data)
        db.session.add(user)
        db.session.commit()
    return flask.redirect(flask.url_for("login"))


@app.route("/")
def log():
    return render_template("login.html")


@app.route("/", methods=["POST"])
def login():
    if request.method == "POST":
        data = flask.request.form.get("userid")
        user = Movie_logins.query.filter_by(userid=data).first()
        if user:
            login_user(user)
            return flask.redirect(flask.url_for("hello_world"))
        else:

            return flask.redirect(flask.url_for("signup1"))


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return flask.redirect(flask.url_for("login"))


app.run(host=os.getenv("IP", "0.0.0.0"), port=int(os.getenv("PORT", 8080)), debug=True)
