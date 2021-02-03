# ----------------------------------------------------------------------------#
# Imports
# ----------------------------------------------------------------------------#

import logging
import sys
from logging import Formatter, FileHandler

import babel
import dateutil.parser
from flask import Flask, render_template, request, flash, redirect, url_for
from flask_migrate import Migrate
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy

from forms import *

# from flask_wtf import FlaskForm
# ----------------------------------------------------------------------------#
# App Config.
# ----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)


# TODO: connect to a local postgresql database # DONE

# ----------------------------------------------------------------------------#
# Models.
# ----------------------------------------------------------------------------#

class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    genres = db.Column(db.ARRAY(db.String()))
    address = db.Column(db.String(120))
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean)
    seeking_description = db.Column(db.String(500))
    shows = db.relationship('Show', backref="Venue", lazy='dynamic')

    # TODO: implement any missing fields, as a database migration using Flask-Migrate
    # simplify to reusable calls for the API ease
    def simple(self):
        return {
            'id': self.id,
            'name': self.name,
        }

    def details(self):
        return {
            'id': self.id,
            'name': self.name,
            'genres': self.genres,
            'address': self.address,
            'city': self.city,
            'state': self.state,
            'phone': self.phone,
            'website': self.website,
            'facebook_link': self.facebook_link,
            'seeking_talent': self.seeking_talent,
            'seeking_description': self.seeking_description,
            'image_link': self.image_link,
        }


class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    genres = db.Column(db.ARRAY(db.String))
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    website = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean)
    seeking_description = db.Column(db.String(500))
    shows = db.relationship('Show', backref="Artist", lazy='dynamic')

    # TODO: implement any missing fields, as a database migration using Flask-Migrate
    # simplify to reusable calls for the API ease
    def simple(self):
        return {
            'id': self.id,
            'name': self.name,
        }

    def details(self):
        return {
            'id': self.id,
            'name': self.name,
            'genres': self.genres,
            'city': self.city,
            'state': self.state,
            'phone': self.phone,
            'website': self.website,
            'facebook_link': self.facebook_link,
            'seeking_venue': self.seeking_venue,
            'seeking_description': self.seeking_description,
            'image_link': self.image_link,
        }


# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.


class Show(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    artist_id = db.Column(db.Integer, db.ForeignKey(
        'Artist.id'), nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'),
                         nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)

    def details(self):
        return {
            'venue_id': self.venue_id,
            'venue_name': self.Venue.name,
            'artist_id': self.artist_id,
            'artist_name': self.Artist.name,
            'artist_image_link': self.Artist.image_link,
            'start_time': self.start_time
        }

    def show_artist(self):
        return {
            'artist_id': self.artist_id,
            'artist_name': self.Artist.name,
            'artist_image_link': self.Artist.image_link,
            'start_time': self.start_time
        }

    def show_venue(self):
        return {
            'venue_id': self.venue_id,
            'venue_name': self.Venue.name,
            'venue_image_link': self.Venue.image_link,
            'start_time': self.start_time
        }


# ----------------------------------------------------------------------------#
# Filters.
# ----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
    date = dateutil.parser.parse(str(value))
    if format == 'full':
        format = "EEEE MMMM, d, y 'at' h:mma"
    elif format == 'medium':
        format = "EE MM, dd, y h:mma"
    return babel.dates.format_datetime(date, format)


app.jinja_env.filters['datetime'] = format_datetime


# ----------------------------------------------------------------------------#
# Controllers.
# ----------------------------------------------------------------------------#

@app.route('/')
def index():
    return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
    # TODO: replace with real venues data.
    #       num_shows should be aggregated based on number of upcoming shows per venue.

    # determine the time, grab the venues, setup empty string and array
    # current_time = datetime.now().strftime('%Y-%m-%d %H:%S:%M')
    # venues = db.session.query(Venue.city,Venue.state).group_by('city','state').all()
    # venue_state_and_city = ''
    # venue_data = []
    #
    # # loop through venues to check for upcoming shows, city, states and venue information
    # for venue in venues:
    #
    #     # filter upcoming shows to check if show has already passed
    #     current_shows = venue.shows.filter(Show.start_time > current_time).all()
    #     # if the venue and state are
    #     if venue_state_and_city == venue.city + venue.state:
    #         venue_data[len(venue_data) - 1]["venues"].append({
    #             "id": venue.id,
    #             "name": venue.name,
    #             "num_upcoming_shows": len(current_shows)  # a count of the number of shows
    #         })
    #         # organize data by city and state (area) if not already done
    #     else:
    #         venue_state_and_city == venue.city + venue.state
    #         venue_data.append({
    #             "city": venue.city,
    #             "state": venue.state,
    #             "venues": [{
    #                 "id": venue.id,
    #                 "name": venue.name,
    #                 "num_upcoming_shows": len(current_shows)
    #             }]
    #         })
    #
    # return render_template('pages/venues.html', areas=venue_data)

    data = []
    ven = db.session.query(Venue.city, Venue.state).group_by('city', 'state').all()
    for city in ven:
        venueInfo = db.session.query(Venue.id, Venue.name).filter_by(city=city[0], state=city[1])
        infos = []
        for info in venueInfo:
            num = getNumUpcomingShows(info[0])
            infos.append({'id': info[0], "name": info[1], "num_upcoming_shows": num})
        col = {"city": city[0], "state": city[1], "venues": infos}
        data.append(col)

    return render_template('pages/venues.html', areas=data);


@app.route('/venues/search', methods=['POST'])
def search_venues():
    # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
    # seach for Hop should return "The Musical Hop".
    # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"

    # search_term = request.form.get('search_term')
    venue_query = Venue.query.filter(Venue.name.ilike('%' + request.form['search_term'] + '%'))
    # compare the search term query to the simple venue json
    venue_list = list(map(Venue.simple, venue_query))

    response = {
        "count": len(venue_list),
        "data": venue_list
    }
    return render_template('pages/search_venues.html',
                           results=response,
                           search_term=request.form.get('search_term', ''))


@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
    # shows the venue page with the given venue_id
    # TODO: replace with real venue  data from the venues table, using venue_id

    venue_query = Venue.query.get(venue_id)
    #
    if venue_query:
        venue_details = Venue.details(venue_query)
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        new_shows_query = Show.query.options(db.joinedload(Show.Venue)).filter(Show.venue_id == venue_id).filter(
            Show.start_time > current_time).all()
        new_show = list(map(Show.show_artist, new_shows_query))

        venue_details["upcoming_shows"] = new_show
        venue_details["upcoming_shows_count"] = len(new_show)

        past_shows_query = Show.query.options(db.joinedload(Show.Venue)).filter(Show.venue_id == venue_id).filter(
            Show.start_time <= current_time).all()
        past_shows = list(map(Show.show_artist, past_shows_query))

        venue_details["past_shows"] = past_shows
        venue_details["past_shows_count"] = len(past_shows)

        return render_template('pages/show_venue.html', venue=venue_details)
    return render_template('errors/404.html')


#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
    form = VenueForm()
    return render_template('forms/new_venue.html', form=form)


@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
    # TODO: insert form data as a new Venue record in the db, instead
    # TODO: modify data to be the data object returned from db insertion

    error = False
    # form = VenueForm(request.form)
    # if form.validate():
    try:
        seeking_talent = False
        seeking_description = ''
        if 'seeking_talent' in request.form:
            seeking_talent = request.form['seeking_talent'] == 'y'
        if 'seeking_description' in request.form:
            seeking_description = request.form['seeking_description']
        new_venue = Venue(
            name=request.form['name'],
            genres=request.form.getlist('genres'),
            address=request.form['address'],
            city=request.form['city'],
            state=request.form['state'],
            phone=request.form['phone'],
            website=request.form['website'],
            facebook_link=request.form['facebook_link'],
            image_link=request.form['image_link'],
            seeking_talent=seeking_talent,
            seeking_description=seeking_description,
        )
        # insert new venue records into the db
        db.session.add(new_venue)
        db.session.commit()
    except:
        # TODO: on unsuccessful db insert, flash an error instead.
        # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
        # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
        error = True
        db.session.rollback()
        print(sys.exc_info())
        flash('An error occurred. Venue ' + request.form['name'] + ' could not be listed.')

    finally:
        db.session.close()
        # on successful db insert, flash success
        if error == False:
            flash('Venue ' + request.form['name'] + ' was successfully listed!')

    return render_template('pages/home.html')


@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
    # TODO: Complete this endpoint for taking a venue_id, and using
    # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
    try:
        Venue.query.filter_by(id=venue_id).delete()
        db.session.commit()
    except:
        db.session.rollback()
    finally:
        db.session.close()
    # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
    # clicking that button delete it from the db then redirect the user to the homepage
    return None


#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
    # TODO: replace with real data returned from querying the database
    # query all artists in the database
    artist_query = Artist.query.all()
    # data = list(map(Artist.short, artist_query))
    return render_template('pages/artists.html', artists=artist_query)


@app.route('/artists/search', methods=['POST'])
def search_artists():
    # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
    # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
    # search for "band" should return "The Wild Sax Band".
    artist_query = Artist.query.filter(Artist.name.ilike('%' + request.form['search_term'] + '%'))
    artist_list = list(map(Artist.simple, artist_query))
    response = {
        "count": len(artist_list),
        "data": artist_list
    }
    return render_template('pages/search_artists.html', results=response,
                           search_term=request.form.get('search_term', ''))


@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
    # shows the venue page with the given venue_id
    # TODO: replace with real venue data from the venues table, using venue_id

    artist_query = Artist.query.get(artist_id)
    if artist_query:
        artist_details = Artist.details(artist_query)
        # get the current time
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        new_shows_query = Show.query.options(db.joinedload(Show.Artist)).filter(Show.artist_id == artist_id).filter(
            Show.start_time > current_time).all()
        new_shows_list = list(map(Show.show_venue, new_shows_query))
        artist_details["upcoming_shows"] = new_shows_list
        artist_details["upcoming_shows_count"] = len(new_shows_list)
        past_shows_query = Show.query.options(db.joinedload(Show.Artist)).filter(Show.artist_id == artist_id).filter(
            Show.start_time <= current_time).all()
        past_shows_list = list(map(Show.show_venue, past_shows_query))
        artist_details["past_shows"] = past_shows_list
        artist_details["past_shows_count"] = len(past_shows_list)
        return render_template('pages/show_artist.html', artist=artist_details)
    return render_template('errors/404.html')


#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
    form = ArtistForm(request.form)
    artist_data = Artist.query.get(artist_id)
    if artist_data:
        artist_details = Artist.details(artist_data)
        form.name.data = artist_details["name"]
        form.genres.data = artist_details["genres"]
        form.city.data = artist_details["city"]
        form.state.data = artist_details["state"]
        form.phone.data = artist_details["phone"]
        form.website.data = artist_details["website"]
        form.facebook_link.data = artist_details["facebook_link"]
        form.seeking_venue.data = artist_details["seeking_venue"]
        form.seeking_description.data = artist_details["seeking_description"]
        form.image_link.data = artist_details["image_link"]
        return render_template('forms/edit_artist.html', form=form, artist=artist_details)
    return render_template('errors/404.html')


@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
    # TODO: take values from the form submitted, and update existing
    # artist record with ID <artist_id> using the new attributes
    form = ArtistForm(request.form)
    artist_data = Artist.query.get(artist_id)
    if artist_data:
        if form.validate():
            seeking_venue = False
            seeking_description = ''
            if 'seeking_venue' in request.form:
                seeking_venue = request.form['seeking_venue'] == 1
            if 'seeking_description' in request.form:
                seeking_description = request.form['seeking_description']
            setattr(artist_data, 'name', request.form['name'])
            setattr(artist_data, 'genres', request.form.getlist('genres'))
            setattr(artist_data, 'city', request.form['city'])
            setattr(artist_data, 'state', request.form['state'])
            setattr(artist_data, 'phone', request.form['phone'])
            setattr(artist_data, 'website', request.form['website'])
            setattr(artist_data, 'facebook_link', request.form['facebook_link'])
            setattr(artist_data, 'image_link', request.form['image_link'])
            setattr(artist_data, 'seeking_description', seeking_description)
            setattr(artist_data, 'seeking_venue', seeking_venue)
            Artist.update(artist_data)
            return redirect(url_for('show_artist', artist_id=artist_id))
        else:
            print(form.errors)
    return render_template('errors/404.html'), 404


@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
    form = VenueForm()
    venue_query = Venue.query.get(venue_id)
    if venue_query:
        venue_details = Venue.details(venue_query)
        form.name.data = venue_details["name"]
        form.genres.data = venue_details["genres"]
        form.address.data = venue_details["address"]
        form.city.data = venue_details["city"]
        form.state.data = venue_details["state"]
        form.phone.data = venue_details["phone"]
        form.website.data = venue_details["website"]
        form.facebook_link.data = venue_details["facebook_link"]
        form.seeking_talent.data = venue_details["seeking_talent"]
        form.seeking_description.data = venue_details["seeking_description"]
        form.image_link.data = venue_details["image_link"]
        return render_template('forms/edit_venue.html', form=form, Venue=venue_details)
    return render_template('errors/404.html')


@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
    # TODO: take values from the form submitted, and update existing
    # venue record with ID <venue_id> using the new attributes
    form = VenueForm(request.form)
    venue_data = Venue.query.get(venue_id)
    if venue_data:
        if form.validate():
            seeking_talent = False
            seeking_description = ''
            if 'seeking_talent' in request.form:
                seeking_talent = request.form['seeking_talent'] == 1
            if 'seeking_description' in request.form:
                seeking_description = request.form['seeking_description']
            setattr(venue_data, 'name', request.form['name'])
            setattr(venue_data, 'genres', request.form.getlist('genres'))
            setattr(venue_data, 'address', request.form['address'])
            setattr(venue_data, 'city', request.form['city'])
            setattr(venue_data, 'state', request.form['state'])
            setattr(venue_data, 'phone', request.form['phone'])
            setattr(venue_data, 'website', request.form['website'])
            setattr(venue_data, 'facebook_link', request.form['facebook_link'])
            setattr(venue_data, 'image_link', request.form['image_link'])
            setattr(venue_data, 'seeking_description', seeking_description)
            setattr(venue_data, 'seeking_talent', seeking_talent)
            Venue.update(venue_data)
            return redirect(url_for('show_venue', venue_id=venue_id))
        else:
            print(form.errors)
    return render_template('errors/404.html'), 404


#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
    form = ArtistForm()
    return render_template('forms/new_artist.html', form=form)


@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
    # called upon submitting the new artist listing form
    # TODO: insert form data as a new Venue record in the db, instead
    # TODO: modify data to be the data object returned from db insertion
    error = False
    try:
        seeking_venue = False
        seeking_description = ''
        if 'seeking_venue' in request.form:
            seeking_venue = request.form['seeking_venue'] == 1
        if 'seeking_description' in request.form:
            seeking_description = request.form['seeking_description']
        new_artist = Artist(
            name=request.form['name'],
            genres=request.form.getlist('genres'),
            city=request.form['city'],
            state=request.form['state'],
            phone=request.form['phone'],
            website=request.form['website'],
            image_link=request.form['image_link'],
            facebook_link=request.form['facebook_link'],
            seeking_venue=seeking_venue,
            seeking_description=seeking_description,
        )
        db.session.add(new_artist)
        db.session.commit()
    except Exception as e:
        # TODO: on unsuccessful db insert, flash an error instead.
        # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
        # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
        error = True
        db.session.rollback()
        print(sys.exc_info())
        print(e)
        flash('An error occurred. Artist ' + request.form['name'] + ' could not be listed.')

    finally:
        db.session.close()
        # on successful db insert, flash success
        if error == False:
            flash('Artist ' + request.form['name'] + ' was successfully listed!')

    return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
    # displays list of shows at /shows
    # TODO: replace with real venues data.
    #       num_shows should be aggregated based on number of upcoming shows per venue.
    # a query of all shows from db using join
    show_query = Show.query.options(db.joinedload(Show.Venue), db.joinedload(Show.Artist)).all()
    data = list(map(Show.details, show_query))
    return render_template('pages/shows.html', shows=data)


@app.route('/shows/create')
def create_shows():
    # renders form. do not touch.
    form = ShowForm()
    return render_template('forms/new_show.html', form=form)


@app.route('/shows/create', methods=['POST'])
def create_show_submission():
    # called to create new shows in the db, upon submitting new show listing form
    # TODO: insert form data as a new Show record in the db, instead
    try:
        new_show = Show(
            venue_id=request.form['venue_id'],
            artist_id=request.form['artist_id'],
            start_time=request.form['start_time'],
        )
        db.session.add(new_show)
        db.session.commit()
    except:
        # TODO: on unsuccessful db insert, flash an error instead.
        # e.g., flash('An error occurred. Show could not be listed.')
        # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
        error = True
        db.session.rollback()
        print(sys.exc_info())
        flash('An error occured. Show could not be listed.')

    finally:
        db.session.close()

        # on successful db insert, flash success
        flash('Show was successfully listed!')

    return render_template('pages/home.html')


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


def getNumUpcomingShows(id, idType='ven', get_data=0):
    if idType == 'ven':
        shows = db.session.query(Show.start_time, Show.artist_id).filter_by(venue_id=id).all()
    elif idType == 'art':
        shows = db.session.query(Show.start_time, Show.venue_id).filter_by(artist_id=id).all()
    num = 0
    cur = datetime.today()
    info = []
    for show in shows:

        if (show[0].date() > cur.date()) or (show[0].date() == cur.date() and show[0].time() > cur.time()):
            num = num + 1
            if idType == 'ven':
                art = db.session.query(Artist.name, Artist.image_link).filter_by(id=show[1]).all()
                info.append({
                    "artist_id": show[1],
                    "artist_name": art[0][0],
                    "artist_image_link": art[0][1],
                    "start_time": str(show[0])
                })
            elif idType == 'art':
                ven = db.session.query(Venue.name, Venue.image_link).filter_by(id=show[1]).all()
                info.append({
                    "venue_id": show[1],
                    "venue_name": ven[0][0],
                    "venue_image_link": ven[0][1],
                    "start_time": str(show[0])
                })
    if get_data == 1:
        return num, info
    return num


def getNumPastShows(id, idType='ven', get_data=0):
    if idType == 'ven':
        shows = db.session.query(Show.start_time, Show.artist_id).filter_by(venue_id=id).all()
    elif idType == 'art':
        shows = db.session.query(Show.start_time, Show.venue_id).filter_by(artist_id=id).all()
    num = 0
    cur = datetime.today()
    info = []
    for show in shows:
        if (show[0].date() < cur.date()) or (show[0].date() == cur.date() and show[0].time() < cur.time()):
            num = num + 1
            if idType == 'ven':
                art = db.session.query(Artist.name, Artist.image_link).filter_by(id=show[1]).all()
                info.append({
                    "artist_id": show[1],
                    "artist_name": art[0][0],
                    "artist_image_link": art[0][1],
                    "start_time": str(show[0])
                })
            elif idType == 'art':
                ven = db.session.query(Venue.name, Venue.image_link).filter_by(id=show[1]).all()
                info.append({
                    "venue_id": show[1],
                    "venue_name": ven[0][0],
                    "venue_image_link": ven[0][1],
                    "start_time": str(show[0])
                })
    if get_data == 1:
        return num, info
    return num


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

# ----------------------------------------------------------------------------#
# Launch.
# ----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
