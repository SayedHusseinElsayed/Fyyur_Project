from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class Venue(db.Model):

    __tablename__        = 'Venue'
    id                   = db.Column(db.Integer, primary_key=True)
    name                 = db.Column(db.String)
    city                 = db.Column(db.String(120))
    state                = db.Column(db.String(120))
    address              = db.Column(db.String(120))
    phone                = db.Column(db.String(120))
    image_link           = db.Column(db.String(500))
    facebook_link        = db.Column(db.String(120))
    website              = db.Column(db.String(120))
    seeking_talent       = db.Column(db.Boolean,nullable=True)
    seeking_description  = db.Column(db.String(2000), nullable=True)
    upcoming_shows_count = db.Column(db.Integer, nullable=True)
    past_shows_count     = db.Column(db.Integer, nullable=True)
    genres               = db.Column(db.ARRAY(db.String), nullable=True) 
    show                 = db.relationship('Show',  backref='Venue.show', lazy=True)

class Artist(db.Model):
    __tablename__        = 'Artist'
    id                   = db.Column(db.Integer, primary_key=True)
    name                 = db.Column(db.String)
    city                 = db.Column(db.String(120))
    state                = db.Column(db.String(120))
    address              = db.Column(db.String(120))
    phone                = db.Column(db.String(120))
    genres               = db.Column(db.ARRAY(db.String), nullable=True)
    image_link           = db.Column(db.String(500))
    facebook_link        = db.Column(db.String(120))
    website              = db.Column(db.String(120))
    seeking_venue        = db.Column(db.Boolean())
    seeking_description  = db.Column(db.String(2000))
    upcoming_shows_count = db.Column(db.Integer, nullable=True)
    past_shows_count     = db.Column(db.Integer, nullable=True)
    show                 = db.relationship('Show',  backref='Artist.show', lazy=True)

class Show(db.Model):
    __tablename__        = 'Show'
    id                   = db.Column(db.Integer, primary_key=True)
    venue_id             = db.Column(db.Integer, db.ForeignKey('Venue.id'))
    artist_id            = db.Column(db.Integer, db.ForeignKey('Artist.id'))
    start_time           = db.Column(db.DateTime)
    artist_image_link    = db.Column(db.String(2000))

    