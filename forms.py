from datetime import datetime
from flask_wtf import FlaskForm as Form
from wtforms import (
    StringField,
    SelectField,
    SelectMultipleField,
    DateTimeField,
    BooleanField,
)
from wtforms.validators import DataRequired, URL
from utils import genres_choices, state_choices, is_valid_phone


class ShowForm(Form):
    artist_id = StringField("artist_id")
    venue_id = StringField("venue_id")
    start_time = DateTimeField(
        "start_time", validators=[DataRequired()], default=datetime.today()
    )


class VenueForm(Form):
    name = StringField("name", validators=[DataRequired()])
    city = StringField("city", validators=[DataRequired()])
    state = SelectField(
        "state",
        validators=[DataRequired()],
        choices=state_choices(),
    )
    address = StringField("address", validators=[DataRequired()])
    phone = StringField("phone")
    image_link = StringField("image_link")
    genres = SelectMultipleField(
        # TODO implement enum restriction
        "genres",
        validators=[DataRequired()],
        choices=genres_choices(),
    )
    facebook_link = StringField("facebook_link", validators=[URL()])
    website_link = StringField("website_link")

    seeking_talent = BooleanField("seeking_talent")

    seeking_description = StringField("seeking_description")

    def validate(self, **kwargs):
        # `**kwargs` to match the method's signature in the `FlaskForm` class.

        """Define a custom validate method in your Form:"""
        validated = Form.validate(self)

        if not validated:
            return False

        if not is_valid_phone(self.phone.data):
            self.phone.errors.append("Invalid phone.")
            return False

        if not set(self.genres.data).issubset(
            [g[0] for g in genres_choices()]
        ):
            self.genres.errors.append("Invalid genres.")
            return False

        if self.state.data not in [s[0] for s in state_choices()]:
            self.state.errors.append("Invalid state.")
            return False

        # if pass validation
        return True


class ArtistForm(Form):
    name = StringField("name", validators=[DataRequired()])
    city = StringField("city", validators=[DataRequired()])
    state = SelectField(
        "state",
        validators=[DataRequired()],
        choices=state_choices(),
    )
    phone = StringField("phone")
    image_link = StringField("image_link")
    genres = SelectMultipleField(
        "genres",
        validators=[DataRequired()],
        choices=genres_choices(),
    )
    facebook_link = StringField(
        # TODO implement enum restriction
        "facebook_link",
        validators=[URL()],
    )

    website_link = StringField("website_link")

    seeking_venue = BooleanField("seeking_venue")

    seeking_description = StringField("seeking_description")

    def validate(self, **kwargs):
        # `**kwargs` to match the method's signature in the `FlaskForm` class.

        """Define a custom validate method in your Form:"""
        validated = Form.validate(self)

        if not validated:
            return False

        if not is_valid_phone(self.phone.data):
            self.phone.errors.append("Invalid phone.")
            return False

        if not set(self.genres.data).issubset(
            [g[0] for g in genres_choices()]
        ):
            self.genres.errors.append("Invalid genres.")
            return False

        if self.state.data not in [s[0] for s in state_choices()]:
            self.state.errors.append("Invalid state.")
            return False

        # if pass validation
        return True
