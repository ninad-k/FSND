import datetime

from flask import Flask
from flask import abort
from flask import jsonify
from flask import request
from flask_cors import CORS

from auth import AuthError, requires_auth
from models import setup_db, Movie, Actor


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    # db_drop_and_create_all()

    @app.route('/movies', methods=['GET'])
    @requires_auth('get:movies')
    def getMovies(jwt):
        movies = Movie.query.all()
        if movies is None:
            abort(404)
        return jsonify({
            "success": True,
            "movies": [{"Title": movie.title, "Date": movie.movie_date, "Actors": movie.actors} for movie in movies]
        }), 200

    @app.route('/actors', methods=['GET'])
    @requires_auth('get:actors')
    def getActors(jwt):
        actors = Actor.query.all()
        if actors is None:
            abort(404)
        return jsonify({
            "success": True,
            "actors": [{"Name": actor.name, "Age": actor.age, "Gender": actor.gender} for actor in actors]
        }), 200

    @app.route('/movies/<int:mid>', methods=['DELETE'])
    @requires_auth('delete:movies')
    def removeMovie(jwt, mid):
        theMovie = Movie.query.filter(Movie.id == mid).one_or_none()
        if theMovie is None:
            abort(404)
        theMovie.delete()
        return jsonify({
            "success": True
        }), 200

    @app.route('/actors/<int:aid>', methods=['DELETE'])
    @requires_auth('delete:actors')
    def removeActor(jwt, aid):
        theActor = Actor.query.filter(Actor.id == aid).one_or_none()
        if theActor is None:
            abort(404)
        theActor.delete()
        return jsonify({
            "success": True
        }), 200

    @app.route('/movies', methods=['POST'])
    @requires_auth('post:movies')
    def postMovie(jwt):
        if ('title' not in request.get_json()) or (
                'movie_date' not in request.get_json()):
            abort(422)
        m_title = request.get_json()['title']
        m_date = request.get_json()['movie_date']
        if (m_title is None) or (m_date is None):
            abort(422)
        newMovie = Movie(
            title=m_title,
            movie_date=datetime.datetime.strptime(
                m_date, '%Y-%m-%dT%H:%M:%S'))
        newMovie.insert()
        return jsonify({
            "success": True,
            "Movie": m_title
        }), 200

    @app.route('/actors', methods=['POST'])
    @requires_auth('post:actors')
    def postActor(jwt):
        if ('name' not in request.get_json()) or (
                'age' not in request.get_json() or ('gender' not in request.get_json())):
            abort(422)
        a_name = request.get_json()['name']
        a_age = request.get_json()['age']
        a_gender = request.get_json()['gender']
        if (a_name is None) or (a_age is None) or (a_gender is None):
            abort(422)
        newActor = Actor(name=a_name, age=a_age, gender=a_gender)
        newActor.insert()
        return jsonify({
            "success": True,
            "Actor": a_name
        }), 200

    @app.route('/movies/<int:mid>', methods=['PATCH'])
    @requires_auth('patch:movies')
    def patchMovie(jwt, mid):
        movie = Movie.query.filter(Movie.id == mid).one_or_none()
        if movie is None:
            abort(404)
        if ('title' in request.get_json()):
            newTitle = request.get_json()['title']
            movie.title = newTitle
        if ('movie_date' in request.get_json()):
            newDate = request.get_json()['movie_date']
            movie.movie_date = datetime.datetime.strptime(
                newDate, '%Y-%m-%dT%H:%M:%S')
        if ('actors' in request.get_json()):
            newActors = request.get_json()['actors']
            for newActor in newActors:
                actor = Actor.query.filter(Actor.name == newActor['name']).one_or_none()
                if actor is None:
                    abort(404)
                if movie.actors is None:
                    movie.actors = []
                movie.actors.append(actor)
        movie.update()
        return jsonify({
            "success": True,
            "Movie": movie.title
        }), 200

    @app.route('/actors/<int:aid>', methods=['PATCH'])
    @requires_auth('patch:actors')
    def patchActor(jwt, aid):
        actor = Actor.query.filter(Actor.id == aid).one_or_none()
        if actor is None:
            abort(404)
        if ('name' in request.get_json()):
            newName = request.get_json()['name']
            actor.name = newName
        if ('age' in request.get_json()):
            newAge = request.get_json()['age']
            actor.age = newAge
        if ('gender' in request.get_json()):
            newGender = request.get_json()['gender']
            actor.gender = newGender
        actor.update()
        return jsonify({
            "Success": True,
            "Actor": actor.name
        }), 200

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'error': 404,
            'message': "Not Found"
        }), 404

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'error': 400,
            'message': "Bad Request"
        }), 400

    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify({
            'error': 401,
            'message': "Unauthorized"
        }), 401

    @app.errorhandler(AuthError)
    def auth_error(error):
        return jsonify({
            "success": False,
            "error": error.status_code,
            "message": error.error
        }), error.status_code

    return app


app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
