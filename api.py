from database_setup import Restaurant, MenuItem
from flask import render_template, jsonify

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base

# Connect to Database and create database session
engine = create_engine('sqlite:///restaurantmenu.db', connect_args={'check_same_thread': False}, echo=True)
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


def register(app):
    # JSON API's to view information
    @app.route('/restaurants/<int:restaurant_id>/menu/JSON')
    def restaurantMenuJSON(restaurant_id):
        restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
        items = session.query(MenuItem).filter_by(
            restaurant_id=restaurant_id).all()
        return jsonify(MenuItems=[i.serialize for i in items])

    @app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/JSON')
    def menuItemJSON(restaurant_id, menu_id):
        menuItem = session.query(MenuItem).filter_by(id=menu_id).one()
        return jsonify(MenuItem=menuItem.serialize)

    @app.route('/restaurants/JSON')
    def restaurantsJSON():
        restaurants = session.query(Restaurant).all()
        return jsonify(restaurants=[r.serialize for r in restaurants])

    # Show all restaurants
    @app.route('/')
    @app.route('/restaurants/')
    def showRestaurants():
        restaurants = session.query(Restaurant).all()
        return render_template('restaurants.html', restaurants=restaurants)
