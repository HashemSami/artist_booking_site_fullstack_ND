# ----------------------------------------------------------------------------#
# Imports
# ----------------------------------------------------------------------------#

import dateutil.parser
import babel
from flask import (
    Flask,
    render_template,
    request,
    flash,
    abort,
    redirect,
    url_for,
)

from flask_moment import Moment

# from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import logging
from logging import Formatter, FileHandler
from forms import ArtistForm, VenueForm, ShowForm
from models import db, Venue, Artist, Genre, Show
import datetime
import sys

from feed_init_data import feed_data

# ----------------------------------------------------------------------------#
# App Config.
# ----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object("config")
db.init_app(app)

migrate = Migrate(app, db)

# ----------------------------------------------------------------------------#
# Filters.
# ----------------------------------------------------------------------------#


def format_datetime(value, format="medium"):
    date = dateutil.parser.parse(value)
    if format == "full":
        format = "EEEE MMMM, d, y 'at' h:mma"
    elif format == "medium":
        format = "EE MM, dd, y h:mma"
    return babel.dates.format_datetime(date, format, locale="en")


app.jinja_env.filters["datetime"] = format_datetime


def num_of_shows(shows, past=False):
    if past:
        shows_values = [
            1 for show in shows if show.start_time < datetime.datetime.now()
        ]

        return len(shows_values)

    shows_values = [
        1 for show in shows if show.start_time > datetime.datetime.now()
    ]

    return len(shows_values)


# ----------------------------------------------------------------------------#
# Controllers.
# ----------------------------------------------------------------------------#


@app.route("/")
def index():
    if len(Genre.query.all()) == 0:
        feed_data(db, Venue, Artist, Genre, Show)
    return render_template("pages/home.html")


#  Venues
#  ----------------------------------------------------------------


@app.route("/venues")
def venues():
    data = []
    error = False
    try:

        query_cities = db.session.query(Venue.city.distinct().label("city"))
        for city in [row.city for row in query_cities.all()]:
            city_venues = Venue.query.filter_by(city=city).all()

            venues = []

            for venue in city_venues:

                venues.append(
                    {
                        "id": venue.id,
                        "name": venue.name,
                        "num_upcoming_shows": num_of_shows(venue.artists),
                    }
                )

            data.append(
                {
                    "city": city,
                    "state": city_venues[0].state,
                    "venues": venues,
                }
            )

    except Exception:
        error = True
        db.session.rollback()
        print(sys.exc_info())

    finally:
        db.session.close()
        if error is True:
            abort(400)
        else:
            return render_template("pages/venues.html", areas=data)


@app.route("/venues/search", methods=["POST"])
def search_venues():
    response = {}
    error = False
    try:
        search_term = request.form.get("search_term", "")
        print(search_term)
        venue_search = Venue.query.filter(
            Venue.name.ilike(f"%{search_term}%")
        ).all()

        response = {
            "count": len(venue_search),
            "data": [
                {
                    "id": venue.id,
                    "name": venue.name,
                    "num_upcoming_shows": num_of_shows(venue.artists),
                }
                for venue in venue_search
            ],
        }

    except Exception:
        error = True
        db.session.rollback()
        print(sys.exc_info())

    finally:
        db.session.close()
        if error is True:
            abort(400)
        else:
            return render_template(
                "pages/search_venues.html",
                results=response,
                search_term=request.form.get("search_term", ""),
            )


@app.route("/venues/<int:venue_id>")
def show_venue(venue_id):
    data = {}
    error = False
    try:
        venue = Venue.query.get_or_404(venue_id)

        past_shows = []
        upcoming_shows = []

        for show in venue.artists:
            temp_show = {
                "artist_id": show.artist_id,
                "artist_name": show.artist.name,
                "artist_image_link": show.artist.image_link,
                "start_time": show.start_time.strftime("%m/%d/%Y, %H:%M:%S"),
            }
            if show.start_time <= datetime.datetime.now():
                past_shows.append(temp_show)
            else:
                upcoming_shows.append(temp_show)

        data = {
            "id": venue.id,
            "name": venue.name,
            "genres": [genre.name for genre in venue.genres],
            "address": venue.address,
            "city": venue.city,
            "state": venue.state,
            "phone": venue.phone,
            "website": venue.website,
            "facebook_link": venue.facebook_link,
            "seeking_talent": venue.seeking_talent,
            "seeking_description": venue.seeking_description,
            "image_link": venue.image_link,
            "past_shows": past_shows,
            "upcoming_shows": upcoming_shows,
            "past_shows_count": len(past_shows),
            "upcoming_shows_count": len(upcoming_shows),
        }

    except Exception:
        error = True
        db.session.rollback()
        print(sys.exc_info())

    finally:
        db.session.close()
        if error is True:
            abort(400)
        else:
            return render_template("pages/show_venue.html", venue=data)


#  Create Venue
#  ----------------------------------------------------------------


@app.route("/venues/create", methods=["GET"])
def create_venue_form():
    form = VenueForm()
    return render_template("forms/new_venue.html", form=form)


@app.route("/venues/create", methods=["POST"])
def create_venue_submission():
    form = VenueForm(request.form, meta={"csrf": False})
    error = False
    if form.validate():
        try:

            new_venue = Venue(
                name=form.name.data,
                address=form.address.data,
                city=form.city.data,
                state=form.state.data,
                phone=form.phone.data,
                website=form.website_link.data,
                facebook_link=form.facebook_link.data,
                seeking_talent=form.seeking_talent.data,
                seeking_description=form.seeking_description.data,
                image_link=form.image_link.data,
            )
            for genre in form.genres.data:
                new_venue.genres.append(Genre(name=genre))

            db.session.add(new_venue)
            db.session.commit()
            # on successful db insert, flash success
            flash(
                "Venue " + request.form["name"] + " was successfully listed!"
            )

        except Exception:
            error = True
            db.session.rollback()
            print(sys.exc_info())

        finally:
            db.session.close()
            if error is True:
                flash(
                    "An error occurred. Venue "
                    + form.name.data
                    + " could not be listed."
                )

            return render_template("pages/home.html")

    # If there is any invalid field
    else:
        message = []
        for field, errors in form.errors.items():
            for error in errors:
                message.append(f"{field}: {error}")
        flash("Please fix the following errors: " + ", ".join(message))
        form = VenueForm()
        return render_template("forms/new_venue.html", form=form)


@app.route("/venues/<venue_id>/delete", methods=["GET"])
def delete_venue(venue_id):

    error = False
    try:
        venue = Venue.query.get(venue_id)
        # data = db.session.query(Venue).filter(Venue.id == venue_id)
        for show in venue.artists:
            db.session.delete(show)

        db.session.delete(venue)
        db.session.commit()
        flash("Venue  was successfully deleted!")

    except Exception:
        error = True
        db.session.rollback()
        print(sys.exc_info())

    finally:
        db.session.close()
        if error is True:
            flash("An error occurred. Venue could not be deleted.")

        return redirect(url_for("index"))


#  Artists
#  ----------------------------------------------------------------
@app.route("/artists")
def artists():
    data = {}
    error = False
    try:
        artists_list = db.session.query(Artist.id, Artist.name).all()

        data = [
            {
                "id": artist.id,
                "name": artist.name,
            }
            for artist in artists_list
        ]

    except Exception:
        error = True
        db.session.rollback()
        print(sys.exc_info())

    finally:
        db.session.close()
        if error is True:
            abort(400)
        else:
            return render_template("pages/artists.html", artists=data)


@app.route("/artists/search", methods=["POST"])
def search_artists():
    response = {}
    error = False
    try:
        search_term = request.form.get("search_term", "")
        print(search_term)
        artist_search = Artist.query.filter(
            Artist.name.ilike(f"%{search_term}%")
        ).all()

        response = {
            "count": len(artist_search),
            "data": [
                {
                    "id": artist.id,
                    "name": artist.name,
                    "num_upcoming_shows": num_of_shows(artist.venues),
                }
                for artist in artist_search
            ],
        }

    except Exception:
        error = True
        db.session.rollback()
        print(sys.exc_info())

    finally:
        db.session.close()
        if error is True:
            abort(400)
        else:
            return render_template(
                "pages/search_artists.html",
                results=response,
                search_term=request.form.get("search_term", ""),
            )


@app.route("/artists/<int:artist_id>")
def show_artist(artist_id):
    data = {}
    error = False
    try:
        artist = Artist.query.get_or_404(artist_id)
        past_shows = []
        upcoming_shows = []

        for show in artist.venues:
            temp_show = {
                "venue_id": show.venue_id,
                "venue_name": show.venue.name,
                "venue_image_link": show.venue.image_link,
                "start_time": show.start_time.strftime("%m/%d/%Y, %H:%M:%S"),
            }
            if show.start_time <= datetime.datetime.now():
                past_shows.append(temp_show)
            else:
                upcoming_shows.append(temp_show)

        data = {
            "id": artist.id,
            "name": artist.name,
            "genres": [genre.name for genre in artist.genres],
            "city": artist.city,
            "state": artist.state,
            "phone": artist.phone,
            "website": artist.website,
            "facebook_link": artist.facebook_link,
            "seeking_venue": artist.seeking_venue,
            "seeking_description": artist.seeking_description,
            "image_link": artist.image_link,
            "past_shows": past_shows,
            "upcoming_shows": upcoming_shows,
            "past_shows_count": len(past_shows),
            "upcoming_shows_count": len(upcoming_shows),
        }
    except Exception:
        error = True
        db.session.rollback()
        print(sys.exc_info())

    finally:
        db.session.close()
        if error is True:
            abort(400)
        else:
            return render_template("pages/show_artist.html", artist=data)


#  Update
#  ----------------------------------------------------------------
@app.route("/artists/<int:artist_id>/edit", methods=["GET"])
def edit_artist(artist_id):
    artist = {}
    error = False
    form = ArtistForm()
    try:
        artist = Artist.query.get(artist_id)

        form.name.data = artist.name
        form.genres.data = [genre.name for genre in artist.genres]
        form.state.data = artist.state
        form.city.data = artist.city
        form.phone.data = artist.phone
        form.website_link.data = artist.website
        form.facebook_link.data = artist.facebook_link
        form.seeking_venue.data = artist.seeking_venue
        form.seeking_description.data = artist.seeking_description
        form.image_link.data = artist.image_link

    except Exception:
        error = True
        db.session.rollback()
        print(sys.exc_info())

    finally:
        db.session.close()
        if error is True:
            abort(400)
        else:
            return render_template(
                "forms/edit_artist.html", form=form, artist=artist
            )


@app.route("/artists/<int:artist_id>/edit", methods=["POST"])
def edit_artist_submission(artist_id):
    form = ArtistForm(request.form)
    error = False
    if form.validate():
        try:
            artist = Artist.query.get(artist_id)

            artist.name = form.name.data
            artist.state = form.state.data
            artist.city = form.city.data
            artist.phone = form.phone.data
            artist.website = form.website_link.data
            artist.facebook_link = form.facebook_link.data
            artist.seeking_venue = form.seeking_venue.data
            artist.seeking_description = form.seeking_description.data
            artist.image_link = form.image_link.data

            new_genres = []
            for genre in form.genres.data:
                genre_name = Genre.query.filter_by(name=genre).first()
                new_genres.append(genre_name)

            artist.genres[:] = new_genres
            db.session.commit()
            # on successful db insert, flash success
            flash(
                "Artist " + request.form["name"] + " was successfully updated!"
            )

        except Exception:
            error = True
            db.session.rollback()
            print(sys.exc_info())

        finally:
            db.session.close()
            if error is True:
                flash(
                    "An error occurred. Artist "
                    + form.name.data
                    + " could not be updated."
                )

            return redirect(url_for("show_artist", artist_id=artist_id))

    # If there is any invalid field
    else:
        message = []
        for field, errors in form.errors.items():
            for error in errors:
                message.append(f"{field}: {error}")
        flash("Please fix the following errors: " + ", ".join(message))
        form = ArtistForm()
        return redirect(url_for("edit_artist", artist_id=artist_id))


@app.route("/venues/<int:venue_id>/edit", methods=["GET"])
def edit_venue(venue_id):

    venue = {}
    error = False
    form = VenueForm()
    try:
        venue = Venue.query.get(venue_id)

        form.name.data = venue.name
        form.genres.data = [genre.name for genre in venue.genres]
        form.address.data = venue.address
        form.city.data = venue.city
        form.state.data = venue.state
        form.phone.data = venue.phone
        form.website_link.data = venue.website
        form.facebook_link.data = venue.facebook_link
        form.seeking_talent.data = venue.seeking_talent
        form.seeking_description.data = venue.seeking_description
        form.image_link.data = venue.image_link
    except Exception:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
        if error is True:
            abort(400)
        else:
            return render_template(
                "forms/edit_venue.html", form=form, venue=venue
            )


@app.route("/venues/<int:venue_id>/edit", methods=["POST"])
def edit_venue_submission(venue_id):
    form = VenueForm(request.form)
    error = False
    if form.validate():
        try:
            venue = Venue.query.get(venue_id)
            venue.name = form.name.data
            venue.address = form.address.data
            venue.city = form.city.data
            venue.state = form.state.data
            venue.phone = form.phone.data
            venue.website = form.website_link.data
            venue.facebook_link = form.facebook_link.data
            venue.seeking_talent = form.seeking_talent.data
            venue.seeking_description = form.seeking_description.data
            venue.image_link = form.image_link.data

            new_genres = []
            for genre in form.genres.data:
                genre_name = Genre.query.filter_by(name=genre).first()
                new_genres.append(genre_name)

            venue.genres[:] = new_genres
            db.session.commit()
            # on successful db insert, flash success
            flash(
                "Venue " + request.form["name"] + " was successfully updated!"
            )

        except Exception:
            error = True
            db.session.rollback()
            print(sys.exc_info())

        finally:
            db.session.close()
            if error is True:
                flash(
                    "An error occurred. Venue "
                    + form.name.data
                    + " could not be updated."
                )

            return redirect(url_for("show_venue", venue_id=venue_id))

    # If there is any invalid field
    else:
        message = []
        for field, errors in form.errors.items():
            for error in errors:
                message.append(f"{field}: {error}")
        flash("Please fix the following errors: " + ", ".join(message))
        form = VenueForm()
        return redirect(url_for("edit_venue", venue_id=venue_id))


#  Create Artist
#  ----------------------------------------------------------------


@app.route("/artists/create", methods=["GET"])
def create_artist_form():
    form = ArtistForm()
    return render_template("forms/new_artist.html", form=form)


@app.route("/artists/create", methods=["POST"])
def create_artist_submission():
    form = ArtistForm(request.form)
    error = False
    if form.validate():
        try:
            new_artist = Artist(
                name=form.name.data,
                city=form.city.data,
                state=form.state.data,
                phone=form.phone.data,
                website=form.website_link.data,
                facebook_link=form.facebook_link.data,
                seeking_venue=form.seeking_venue.data,
                seeking_description=form.seeking_description.data,
                image_link=form.image_link.data,
            )

            for genre in form.genres.data:
                new_artist.genres.append(Genre(name=genre))

            db.session.add(new_artist)
            db.session.commit()

            # on successful db insert, flash success
            flash(
                "Artist " + request.form["name"] + " was successfully listed!"
            )

        except Exception:
            error = True
            db.session.rollback()
            print(sys.exc_info())

        finally:
            db.session.close()
            if error is True:
                flash(
                    "An error occurred. Artist "
                    + form.name.data
                    + " could not be listed."
                )

            return render_template("pages/home.html")

    # If there is any invalid field
    else:
        message = []
        for field, errors in form.errors.items():
            for error in errors:
                message.append(f"{field}: {error}")
        flash("Please fix the following errors: " + ", ".join(message))
        form = ArtistForm()
        return render_template("forms/new_artist.html", form=form)


#  Shows
#  ----------------------------------------------------------------


@app.route("/shows")
def shows():
    data = {}
    error = False
    try:
        shows_list = Show.query.all()

        data = [
            {
                "venue_id": show.venue_id,
                "venue_name": show.venue.name,
                "artist_id": show.artist_id,
                "artist_name": show.artist.name,
                "artist_image_link": show.artist.image_link,
                "start_time": show.start_time.strftime("%m/%d/%Y, %H:%M:%S"),
            }
            for show in shows_list
        ]

    except Exception:
        error = True
        db.session.rollback()
        print(sys.exc_info())

    finally:
        db.session.close()
        if error is True:
            abort(400)
        else:
            return render_template("pages/shows.html", shows=data)


@app.route("/shows/create")
def create_shows():
    # renders form. do not touch.
    form = ShowForm()
    return render_template("forms/new_show.html", form=form)


@app.route("/shows/create", methods=["POST"])
def create_show_submission():
    form = ShowForm(request.form)
    error = False
    if form.validate():
        try:
            new_show = Show(
                artist_id=form.artist_id.data,
                venue_id=form.venue_id.data,
                start_time=form.start_time.data,
            )

            db.session.add(new_show)
            db.session.commit()

            # on successful db insert, flash success
            flash("Show was successfully listed!")

        except Exception:
            error = True
            db.session.rollback()
            print(sys.exc_info())

        finally:
            db.session.close()
            if error is True:
                flash("An error occurred. Show could not be listed.")

            return render_template("pages/home.html")

    # If there is any invalid field
    else:
        message = []
        for field, errors in form.errors.items():
            for error in errors:
                message.append(f"{field}: {error}")
        flash("Please fix the following errors: " + ", ".join(message))
        form = ShowForm()
        return render_template("forms/new_show.html", form=form)


@app.errorhandler(404)
def not_found_error(error):
    return render_template("errors/404.html"), 404


@app.errorhandler(500)
def server_error(error):
    return render_template("errors/500.html"), 500


if not app.debug:
    file_handler = FileHandler("error.log")
    file_handler.setFormatter(
        Formatter(
            "%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]"
        )
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info("errors")

# ----------------------------------------------------------------------------#
# Launch.
# ----------------------------------------------------------------------------#

# Default port:
if __name__ == "__main__":
    app.run()

# Or specify port manually:
"""
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
"""
