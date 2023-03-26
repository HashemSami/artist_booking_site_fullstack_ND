from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class Show(db.Model):
    __tablename__ = "shows"

    # id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    venue_id = db.Column(
        db.Integer, db.ForeignKey("venues.id"), primary_key=True
    )
    artist_id = db.Column(
        db.Integer, db.ForeignKey("artists.id"), primary_key=True
    )
    start_time = db.Column(db.DateTime, primary_key=True)

    venue = db.relationship("Venue", back_populates="artists")
    artist = db.relationship("Artist", back_populates="venues")


genres_venues = db.Table(
    "genres_venues",
    db.Column(
        "venue_id", db.Integer, db.ForeignKey("venues.id"), primary_key=True
    ),
    db.Column(
        "genre_id", db.Integer, db.ForeignKey("genres.id"), primary_key=True
    ),
)

genres_artists = db.Table(
    "genres_artists",
    db.Column(
        "artist_id", db.Integer, db.ForeignKey("artists.id"), primary_key=True
    ),
    db.Column(
        "genre_id", db.Integer, db.ForeignKey("genres.id"), primary_key=True
    ),
)


class Genre(db.Model):
    __tablename__ = "genres"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))


class Venue(db.Model):
    __tablename__ = "venues"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    city = db.Column(db.String(120))
    state = db.Column(db.String(120))

    address = db.Column(db.String(120))
    genres = db.relationship(
        "Genre", secondary=genres_venues, backref="venue_genres"
    )

    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website = db.Column(db.String)

    seeking_talent = db.Column(db.Boolean)
    seeking_description = db.Column(db.String)

    artists = db.relationship(
        "Show", back_populates="venue", lazy="joined", cascade="all, delete"
    )


class Artist(db.Model):
    __tablename__ = "artists"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    genres = db.relationship(
        "Genre", secondary=genres_artists, backref="artist_genres"
    )

    phone = db.Column(db.String(120))
    website = db.Column(db.String)
    facebook_link = db.Column(db.String(120))
    image_link = db.Column(db.String(500))

    seeking_venue = db.Column(db.Boolean)
    seeking_description = db.Column(db.String)

    venues = db.relationship(
        "Show", back_populates="artist", lazy="joined", cascade="all, delete"
    )
