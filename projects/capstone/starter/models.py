import os

from flask_sqlalchemy import SQLAlchemy

# database_filename = "database.db"
# project_dir = os.path.dirname(os.path.abspath(__file__))
# database_path = "sqlite:///{}".format(os.path.join(project_dir, database_filename))
database_path = os.environ['DATABASE_URL']

db = SQLAlchemy()


def setup_db(app):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)


def db_drop_and_create_all():
    db.drop_all()
    db.create_all()


movie_actors = db.Table('movie_actors',
                        db.Column(
                            'movie_id',
                            db.Integer,
                            db.ForeignKey('Movie.id'),
                            primary_key=True),
                        db.Column(
                            'actor_id',
                            db.Integer,
                            db.ForeignKey('Actor.id'),
                            primary_key=True)
                        )


class Movie(db.Model):
    __tablename__ = 'Movie'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    title = db.Column(db.String(120))
    movie_date = db.Column(db.DateTime)
    actors = db.relationship('Actor', secondary=movie_actors,
                             backref=db.backref('Movie', lazy='joined'))

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()


class Actor(db.Model):
    __tablename__ = 'Actor'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(100))
    age = db.Column(db.Integer)
    gender = db.Column(db.String(50))

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()
