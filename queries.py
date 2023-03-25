from app import (
    db,
    Venue,
    Artist,
    Genre,
    Show,
    app,
    genres_venues,
    genres_artists,
)
import datetime

app.app_context().push()

print(Genre.query.all())

# CA = City(name="San Francisco", state="CA")
# NY = City(name="New York", state="NY")

# db.session.add_all([CA, NY])

db.session.query(genres_venues).delete()
db.session.query(genres_artists).delete()
Show.query.delete()
Venue.query.delete()
Artist.query.delete()
Genre.query.delete()
# db.session.remove()
# db.drop_all()

db.session.commit()
db.session.close()
