#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import (
    Flask, 
    render_template, 
    request, 
    Response, 
    flash, 
    redirect, 
    url_for,
    session
)
from flask_moment import Moment
from configparser import ConfigParser
from sqlalchemy import func
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *

from flask_migrate import Migrate
from model import db, Venue, Artist, Show

import sys

#----------------------------------------------------------------------------#
# App Config.

#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db.init_app(app)
migrate = Migrate(app , db)
with app.app_context():
     db.create_all()

# TODO: connect to a local postgresql database

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#


#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format)

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  locals = []
  venues = Venue.query.all()

  places = Venue.query.distinct(Venue.city, Venue.state).all()

  for place in places:
    locals.append({
        'city': place.city,
        'state': place.state,
        'venues': [{
            'id': venue.id,
            'name': venue.name,
            'num_upcoming_shows': len([show for show in venue.show if show.start_time > datetime.now()])
        } for venue in venues if
            venue.city == place.city and venue.state == place.state]
    })

  return render_template('pages/venues.html', areas=locals)

@app.route('/venues/search', methods=['POST'])
def search_venues():
 search = request.form.get('search_term', '')

 venues = Venue.query.filter(Venue.name.ilike("%" + search + "%")).all()

 response = {
    "count": len(venues),
    "data": []
}

 for venue in venues:
    response["data"].append({
        'id': venue.id,
        'name': venue.name,
    })

 return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
          venue = Venue.query.filter_by(id=venue_id).first()
          shows = Show.query.filter_by(venue_id=venue_id).all()
          past_shows = []
          upcoming_shows = []
          now = str(datetime.now())
          for show in shows:
                  if  str(show.start_time) < now :
                      past_shows.append({
                      "venue_id": show.venue_id,
                      "venue_name": Venue.query.filter_by(id=show.venue_id).first().name,
                      "artist_image_link": Artist.query.filter_by(id=show.artist_id).first().image_link,
                      "start_time": str(show.start_time),
                      "artist_name": Artist.query.filter_by(id=show.artist_id).first().name,
                      "artist_id": Artist.query.filter_by(id=show.artist_id).first().id
                    })
                  elif str(show.start_time) > now :
                      upcoming_shows.append({
                      "venue_id": show.venue_id,
                      "venue_name": Venue.query.filter_by(id=show.venue_id).first().name,
                      "artist_image_link": Artist.query.filter_by(id=show.artist_id).first().image_link,
                      "start_time": str(show.start_time),
                      "artist_name": Artist.query.filter_by(id=show.artist_id).first().name,
                      "artist_id": Artist.query.filter_by(id=show.artist_id).first().id
                    })
                
          data = {
            "id": venue.id,
            "name": venue.name,
            #"genres": str(venue.genres).replace("{","").replace("}","").split(","), 
            "genres": str(venue.genres).replace("[","").replace("]","").replace("'","").split(","), 
            "city": venue.city,
            "state": venue.state,
            "address": venue.address,
            "phone": venue.phone,
            "website": venue.website,
            "facebook_link": venue.facebook_link,
            "seeking_talent": venue.seeking_talent,
            "seeking_description": venue.seeking_description,
            "image_link": venue.image_link,
            "past_shows": past_shows,
            "upcoming_shows": upcoming_shows,
            "past_shows_count": len(past_shows),
            "upcoming_shows_count": len(upcoming_shows)
          }
          return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)
  

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
 
    data = request.form
    name = data['name']
    city = data['city']
    state = data['state']
    address = data['address']
    phone = data['phone']
    genres = data.getlist('genres')
    facebook_link = data['facebook_link']
    if Venue.query.first() != None and Venue.query.filter_by(phone=phone).first() != None:
        flash('this Venue is already listed!')
    else:
        try:
            new_venue = Venue(name=name, city=city, state=state, address=address,
                              phone=phone, genres=genres, facebook_link=facebook_link)
            db.session.add(new_venue)
            db.session.commit()
            # on successful db insert, flash success
            flash('Venue ' + request.form['name'] +
                  ' was successfully listed!')
        except:
            db.session.rollback()
            # TODO: on unsuccessful db insert, flash an error instead.
            flash('Something went wrong :( Venue ' +
                  request.form['name'] + ' could not be listed')
        finally:
            db.session.close()
        
    # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
        return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['POST'])
def delete_venue(venue_id):
  
  # TODO: Complete this endpoint for taking a venue_id, and using
        try:
            venue = Venue.query.get(venue_id)
            db.session.delete(venue)
            db.session.commit()
            # on successful db delete, flash success
            flash('Venue ' + venue.name +
                  ' was successfully deleted!')
        except:
            db.session.rollback()
            # TODO: on unsuccessful db delete, flash an error instead.
            flash('Something went wrong :( Venue ' +
                  venue.name + ' could not be deleted')
        finally:
            db.session.close()
    
        return render_template('pages/home.html')

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database
  data = Artist.query.all()
 
  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
 search = request.form.get('search_term', '')

 artists = Artist.query.filter(Artist.name.ilike("%" + search + "%")).all()

 response = {
    "count": len(artists),
    "data": []
 }

 for artist in artists:
    response["data"].append({
        'id': artist.id,
        'name': artist.name,
    })

    return render_template('pages/search_artists.html', results=response)

# Delete Artist method
@app.route('/artists/<artist_id>', methods=['POST'])
def delete_artist(artist_id):
  
  # TODO: Complete this endpoint for taking a venue_id, and using
        try:
            artist = Artist.query.get(artist_id)
            db.session.delete(artist)
            db.session.commit()
            # on successful db delete, flash success
            flash('Artist ' + artist.name +
                  ' was successfully deleted!')
        except:
            db.session.rollback()
            # TODO: on unsuccessful db delete, flash an error instead.
            flash('Something went wrong :( Artist ' +
                  artist.name + ' could not be deleted')
        finally:
            db.session.close()
    
        return render_template('pages/home.html')

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
          artist = Artist.query.filter_by(id=artist_id).first()
          shows = Show.query.filter_by(artist_id=artist_id).all()
          past_shows = []
          upcoming_shows = []
          now = str(datetime.now())
          for show in shows:
                  if  str(show.start_time) < now :
                      past_shows.append({
                      "artist_id": show.artist_id,
                      "artist_name": Artist.query.filter_by(id=show.artist_id).first().name,
                      "venue_image_link": Venue.query.filter_by(id=show.venue_id).first().image_link,
                      "start_time": str(show.start_time),
                      "venue_name": Venue.query.filter_by(id=show.venue_id).first().name,
                      "venue_id": Venue.query.filter_by(id=show.venue_id).first().id
                    })
                  elif str(show.start_time) > now :
                      upcoming_shows.append({
                      "artist_id": show.artist_id,
                      "artist_name": Artist.query.filter_by(id=show.artist_id).first().name,
                      "venue_image_link": Venue.query.filter_by(id=show.venue_id).first().image_link,
                      "start_time": str(show.start_time),
                      "venue_name": Venue.query.filter_by(id=show.venue_id).first().name,
                      "venue_id": Venue.query.filter_by(id=show.venue_id).first().id
                    })
     
          data = {
            "id": artist.id,
            "name": artist.name,
            "genres": str(artist.genres).replace("[","").replace("]","").replace("'","").split(","), 
            "city": artist.city,
            "state": artist.state,
            "address": artist.address,
            "phone": artist.phone,
            "website": artist.website,
            "facebook_link": artist.facebook_link,
            "seeking_venue": artist.seeking_venue,
            "seeking_description": artist.seeking_description,
            "image_link": artist.image_link,
            "past_shows": past_shows,
            "upcoming_shows": upcoming_shows,
            "past_shows_count": len(past_shows),
            "upcoming_shows_count": len(upcoming_shows)

          }
          
          return render_template('pages/show_artist.html', artist=data)



#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()

  # TODO: populate form with fields from artist with ID <artist_id>
  artist = Artist.query.get(artist_id)
  form.name.data = artist.name
  form.city.data = artist.city
  form.state.data = artist.state
  form.phone.data = artist.phone
  form.genres.data = artist.genres
  form.facebook_link.data = artist.facebook_link
 
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
    data = request.form 
    artist = Artist.query.get(artist_id)
    artist.name = data['name']
    artist.city = data['city']
    artist.state = data['state']
    artist.phone = data['phone']
    artist.genres = data.getlist('genres')
    artist.facebook_link = data['facebook_link']
   
    try:
           
            db.session.commit()
            # on successful db editing, flash success
            flash('Artist ' + request.form['name'] +
                  ' was successfully updated!')
    except:
            db.session.rollback()
            # TODO: on unsuccessful db edited, flash an error instead.
            flash('Something went wrong :( Artist ' +
                  request.form['name'] + ' could not be updated')
    finally:
            db.session.close()
  # artist record with ID <artist_id> using the new attributes

    return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()

  # TODO: populate form with values from venue with ID <venue_id>
  venue = Venue.query.get(venue_id)
  form.name.data = venue.name
  form.city.data = venue.city
  form.address.data = venue.address
  form.state.data = venue.state
  form.phone.data = venue.phone
  form.genres.data = venue.genres
  form.facebook_link.data = venue.facebook_link

  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
    data = request.form 
    venue = Venue.query.get(venue_id)
    venue.name = data['name']
    venue.city = data['city']
    venue.state = data['state']
    venue.phone = data['phone']
    venue.address = data['address']
    venue.genres = data.getlist('genres')
    venue.facebook_link = data['facebook_link']
   
    try:
           
            db.session.commit()
            # on successful db editing, flash success
            flash('Venue ' + request.form['name'] +
                  ' was successfully updated!')
    except:
            db.session.rollback()
            # TODO: on unsuccessful db edited, flash an error instead.
            flash('Something went wrong :( Venue ' +
                  request.form['name'] + ' could not be updated')
    finally:
            db.session.close()

    return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
    
    data = request.form
    name = data['name']
    city = data['city']
    state = data['state']
    address = data['address']
    phone = data['phone']
    genres = data.getlist('genres')

    facebook_link = data['facebook_link']
    if Artist.query.first() != None and Artist.query.filter_by(phone=phone).first() != None:
        flash('this Artist is already listed!')
    else:
        try:
            new_artist = Artist(name=name, city=city, state=state,address=address,
                              phone=phone, genres=genres, facebook_link=facebook_link)
            db.session.add(new_artist)
            db.session.commit()
            # on successful db insert, flash success
            flash('Artist ' + request.form['name'] +
                  ' was successfully listed!')
        except:
            db.session.rollback()
            # TODO: on unsuccessful db insert, flash an error instead.
            flash('Something went wrong :( Artist ' +
                  request.form['name'] + ' could not be listed')
        finally:
            db.session.close()
    # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
        return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  #data = Show.query.all()
    data = Show.query.\
    filter_by(venue_id=Venue.id).\
    join(Venue).\
    filter_by(id=Show.venue_id).\
    join(Artist).\
    filter_by(id=Show.artist_id).\
    all()

    shows = Show.query.all()
    all_shows = []

    for show in shows:
                  
                      all_shows.append({
                      "artist_id": show.artist_id,
                      "artist_name": Artist.query.filter_by(id=show.artist_id).first().name,
                      "venue_id": show.venue_id,
                      "venue_name": Venue.query.filter_by(id=show.venue_id).first().name,
                      "venue_image_link": Venue.query.filter_by(id=show.venue_id).first().image_link,
                      "artist_image_link": Artist.query.filter_by(id=show.artist_id).first().image_link,
                      "start_time": str(show.start_time)

                    })
                
    data = all_shows  
    return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  data = request.form

  venue_id = data['venue_id']
  artist_id = data['artist_id']
  start_time = data['start_time']

  if Show.query.first() != None and Show.query.filter_by(start_time=start_time).first() != None:
        flash('this Show cannot be listed because this time is booked before!')

  else:
        try:
            new_show = Show(venue_id=venue_id, artist_id=artist_id, start_time=start_time)
            db.session.add(new_show)
            db.session.commit()
            # on successful db insert, flash success
            flash('Show was successfully listed!')
        except:
            db.session.rollback()
            # TODO: on unsuccessful db insert, flash an error instead.
            flash('Something went wrong :( Show could not be listed')
        finally:
            db.session.close()


  return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()
    app.secret_key = 'super secret key'


# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
