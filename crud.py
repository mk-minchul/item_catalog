from flask import render_template, request, redirect, url_for, flash
from flask import session as login_session
from database_setup import Restaurant, MenuItem

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base

# Connect to Database and create database session
engine = create_engine('sqlite:///restaurantmenu.db', connect_args={'check_same_thread': False}, echo=True)
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


def register(app):
    # Create new restaurant
    @app.route('/restaurants/new/', methods=['GET', 'POST'])
    def newRestaurant():
        if 'username' not in login_session:
            return redirect('/login')
        if request.method == 'POST':
            newRestaurant = Restaurant(name=request.form['name'], user_id=login_session["user_id"])
            session.add(newRestaurant)
            session.commit()
            return redirect(url_for('showRestaurants'))
        else:
            return render_template('newRestaurant.html')

    # Edit restaurant
    @app.route('/restaurants/<int:restaurant_id>/edit/', methods=['GET', 'POST'])
    def editRestaurant(restaurant_id):
        editedRestaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
        if 'username' not in login_session:
            return redirect('/login')
        if editedRestaurant.user_id != login_session['user_id']:
            return "<script>{alert('Unauthorized');}</script>"
        if request.method == 'POST':
            if request.form['name']:
                if request.form['name'] is not None:
                    editedRestaurant.name = request.form['name']
                    session.add(editedRestaurant)
                    session.commit()

                flash('Restaurant Successfully Edited %s' % editedRestaurant.name)
                return redirect(url_for('showRestaurants'))
            else:
                return redirect(url_for('showRestaurants'))
        else:
            return render_template('editRestaurant.html', restaurant=editedRestaurant)

    # Delete restaurant
    @app.route('/restaurants/<int:restaurant_id>/delete/', methods=['GET', 'POST'])
    def deleteRestaurant(restaurant_id):
        restaurantToDelete = session.query(
            Restaurant).filter_by(id=restaurant_id).one()
        if 'username' not in login_session:
            return redirect('/login')
        if restaurantToDelete.user_id != login_session['user_id']:
            return "<script>{alert('Unauthorized');}</script>"
        if request.method == 'POST':
            session.delete(restaurantToDelete)
            flash('%s Successfully Deleted' % restaurantToDelete.name)
            session.commit()
            return redirect(url_for('showRestaurants'))
        else:
            return render_template('deleteRestaurant.html',
                                   restaurant=restaurantToDelete)

    # Show restaurant menu
    @app.route('/restaurants/<int:restaurant_id>/')
    @app.route('/restaurants/<int:restaurant_id>/menu/')
    def restaurantMenu(restaurant_id):
        restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
        items = session.query(
            MenuItem).filter_by(restaurant_id=restaurant_id).all()
        return render_template('menu.html', restaurant=restaurant, items=items)

    # Create new menu item
    @app.route(
        '/restaurants/<int:restaurant_id>/menu/new/', methods=['GET', 'POST'])
    def newMenuItem(restaurant_id):
        if 'username' not in login_session:
            return redirect('/login')

        if request.method == 'POST':
            newItem = MenuItem(name=request.form['name'],
                               description=request.form['description'],
                               price=request.form['price'],
                               restaurant_id=restaurant_id,
                               user_id=login_session["user_id"])
            session.add(newItem)
            session.commit()
            flash("Menu Item has been added")
            return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
        else:
            return render_template('newmenuitem.html', restaurant_id=restaurant_id)

    # Edit menu item
    @app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/edit/',
               methods=['GET', 'POST'])
    def editMenuItem(restaurant_id, menu_id):
        if 'username' not in login_session:
            return redirect('/login')
        editedItem = session.query(MenuItem).filter_by(id=menu_id).one()
        if request.method == 'POST':
            if request.form['name']:
                editedItem.name = request.form['name']
            if request.form['description']:
                editedItem.description = request.form['description']
            if request.form['price']:
                editedItem.price = request.form['price']
            session.add(editedItem)
            session.commit()
            flash("Menu Item has been edited")

            return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
        else:
            return render_template(
                'editmenuitem.html', restaurant_id=restaurant_id,
                menu_id=menu_id, item=editedItem)

    # Delete menu item
    @app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/delete/',
               methods=['GET', 'POST'])
    def deleteMenuItem(restaurant_id, menu_id):
        if 'username' not in login_session:
            return redirect('/login')
        itemToDelete = session.query(MenuItem).filter_by(id=menu_id).one()
        if request.method == 'POST':
            session.delete(itemToDelete)
            session.commit()
            flash("Menu Item has been deleted")
            return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
        else:
            return render_template('deleteMenuItem.html', item=itemToDelete)
