# from app import db, Venue, Artist, Genre, Show, app


# app.app_context().push()


def feed_data(db, Venue, Artist, Genre, Show):

    Alternative = Genre(name="Alternative")
    Blues = Genre(name="Blues")
    Classical = Genre(name="Classical")
    Country = Genre(name="Country")
    Electronic = Genre(name="Electronic")
    Folk = Genre(name="Folk")
    Funk = Genre(name="Funk")
    HipHop = Genre(name="Hip-Hop")
    HeavyMetal = Genre(name="Heavy Metal")
    Instrumental = Genre(name="Instrumental")
    Jazz = Genre(name="Jazz")
    MusicalTheatre = Genre(name="Musical Theatre")
    Pop = Genre(name="Pop")
    Punk = Genre(name="Punk")
    RB = Genre(name="R&B")
    Reggae = Genre(name="Reggae")
    RocknRoll = Genre(name="Rock n Roll")
    Soul = Genre(name="Soul")
    Other = Genre(name="Other")

    db.session.add_all(
        [
            Alternative,
            Blues,
            Classical,
            Country,
            Electronic,
            Folk,
            Funk,
            HipHop,
            HeavyMetal,
            Instrumental,
            Jazz,
            MusicalTheatre,
            Pop,
            Punk,
            RB,
            Reggae,
            RocknRoll,
            Soul,
            Other,
        ]
    )

    venue1 = Venue(
        name="The Musical Hop",
        address="1015 Folsom Street",
        city="San Francisco",
        state="CA",
        phone="123-123-1234",
        website="https://www.themusicalhop.com",
        facebook_link="https://www.facebook.com/TheMusicalHop",
        seeking_talent=True,
        seeking_description="We are on the lookout for a local artist to play every two weeks. Please Call us.",
        image_link="https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60",
    )
    venue1.genres.append(Jazz)
    venue1.genres.append(Reggae)
    venue1.genres.append(Classical)
    venue1.genres.append(Folk)

    venue2 = Venue(
        name="The Dueling Pianos Bar",
        address="335 Delancy Street",
        city="New York",
        state="NY",
        phone="914-003-1132",
        website="https://www.theduelingpianos.com",
        facebook_link="https://www.facebook.com/theduelingpianos",
        seeking_talent=False,
        image_link="https://images.unsplash.com/photo-1497032205916-ac775f0649ae?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=750&q=80",
    )
    venue2.genres.append(Classical)
    venue2.genres.append(RB)
    venue2.genres.append(HipHop)

    venue3 = Venue(
        name="Park Square Live Music & Coffee",
        address="34 Whiskey Moore Ave",
        city="San Francisco",
        state="CA",
        phone="415-000-1234",
        website="https://www.parksquarelivemusicandcoffee.com",
        facebook_link="https://www.facebook.com/ParkSquareLiveMusicAndCoffee",
        seeking_talent=False,
        image_link="https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
    )
    venue3.genres.append(RocknRoll)
    venue3.genres.append(Jazz)
    venue3.genres.append(Classical)
    venue3.genres.append(Folk)

    artist1 = Artist(
        name="Guns N Petals",
        city="San Francisco",
        state="CA",
        phone="326-123-5000",
        website="https://www.gunsnpetalsband.com",
        facebook_link="https://www.facebook.com/GunsNPetals",
        seeking_venue=True,
        seeking_description="Looking for shows to perform at in the San Francisco Bay Area!",
        image_link="https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
    )
    artist1.genres.append(RocknRoll)

    artist2 = Artist(
        name="Matt Quevedo",
        city="New York",
        state="NY",
        phone="300-400-5000",
        facebook_link="https://www.facebook.com/mattquevedo923251523",
        seeking_venue=False,
        image_link="https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
    )
    artist2.genres.append(Jazz)

    artist3 = Artist(
        name="The Wild Sax Band",
        city="San Francisco",
        state="CA",
        phone="432-325-5432",
        seeking_venue=False,
        image_link="https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
    )
    artist3.genres.append(Jazz)
    artist3.genres.append(Classical)

    show1 = Show(
        start_time="2019-05-21T21:30:00.000Z",
        venue=venue1,
        artist=artist1,
    )

    show2 = Show(
        start_time="2019-06-15T23:00:00.000Z",
        venue=venue3,
        artist=artist2,
    )

    show3 = Show(
        start_time="2035-04-01T20:00:00.000Z",
        venue=venue3,
        artist=artist3,
    )

    show4 = Show(
        start_time="2035-04-08T20:00:00.000Z",
        venue=venue3,
        artist=artist3,
    )

    show5 = Show(
        start_time="2035-04-15T20:00:00.000Z",
        venue=venue3,
        artist=artist3,
    )

    db.session.add_all([artist1, artist2, artist3])
    db.session.add_all([venue1, venue2, venue3])
    db.session.add_all([show1, show2, show3, show4, show5])

    db.session.commit()
    db.session.close()


# feed_data(db, Venue, Artist, Genre, Show)
