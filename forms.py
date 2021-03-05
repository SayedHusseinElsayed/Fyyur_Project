from datetime import datetime
from flask_wtf import FlaskForm as Form
from enums import Genre, State
from wtforms import StringField, SelectField, SelectMultipleField, DateTimeField
from wtforms.validators import DataRequired, AnyOf, URL, Regexp, Length, regexp

class ShowForm(Form):
    artist_id = StringField(
        'artist_id'
    )
    venue_id = StringField(
        'venue_id'
    )
    start_time = DateTimeField(
        'start_time',
        validators=[DataRequired()],
        default= datetime.today()
    )

class VenueForm(Form):
    name = StringField(
        'name', validators=[DataRequired()]
    )
    city = StringField(
        'city', validators=[DataRequired()]
    )
    state = SelectField(
        'state', validators=[DataRequired()],
        choices=State.choices()
    )
    address = StringField(
        'address', validators=[DataRequired()]
    )
    phone = StringField(
        'phone' ,
        validators=[DataRequired(),
        Length(min=10, max=11)
       
         ]
      
        )
  
    image_link = StringField(
        'image_link'
    )
    genres = SelectMultipleField(
        # TODO implement enum restriction
        'genres',
        choices=Genre.choices()
    )
    facebook_link = StringField(
        'facebook_link', validators=[URL()]
    )
    website = StringField(
        'website', validators=[URL()]
    )
    seeking_talent = SelectField('seeking_talent', choices=[(False, 'No'), (True, 'Yes')])
    seeking_description = StringField(
        'seeking_description', validators=[DataRequired()]
    )

class ArtistForm(Form):
    name = StringField(
        'name', validators=[DataRequired()]
    )
    city = StringField(
        'city', validators=[DataRequired()]
    )
    state = SelectField(
        'state', validators=[DataRequired()],
        choices=State.choices()
    )
    phone = StringField(
        # TODO implement validation logic for state
      'phone' ,
        validators=[DataRequired(),
        Length(min=10, max=11)
       
         ]
      
    )
    address = StringField(
        # TODO implement validation logic for state
      'address' ,
        validators=[DataRequired(),

         ]
      
    )
    image_link = StringField(
        'image_link'
    )
    genres = SelectMultipleField(
        # TODO implement enum restriction
        'genres', validators=[DataRequired()],
        choices=Genre.choices()
    )
    facebook_link = StringField(
        # TODO implement enum restriction
        'facebook_link', validators=[URL()]
    )
    website = StringField(
        'website', validators=[URL()]
    )
    seeking_venue = SelectField('seeking_venue', choices=[(False, 'No'), (True, 'Yes')])
    seeking_description = StringField(
        'seeking_description', validators=[DataRequired()]
    )

# TODO IMPLEMENT NEW ARTIST FORM AND NEW SHOW FORM
