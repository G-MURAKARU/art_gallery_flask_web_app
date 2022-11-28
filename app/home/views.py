# app/home/views.py

import ast
from flask import render_template, abort, url_for, redirect, session, flash, request
from flask_login import login_required, current_user

from app import db, login_manager
from . import home
from ..models import Artist, Artwork, Group, Customer, load_user, artistPreferences, groupPreferences
from forms import SelectArtistPreferenceForm, SelectGroupPreferenceForm
from sqlalchemy import exc


@home.route('/')
def homepage():
    """
    Render the homepage template on the / route
    """
    # prevents admin from accessing customer homepage
    if current_user.is_authenticated:
        if current_user.is_admin:
            return redirect(url_for('home.admin_dashboard'))

    return render_template('home/home.html', title="Welcome")


@home.route('/artists')
def featured_artists():
    """
    Listing all artists
    """
    artists = Artist.query.all()

    return render_template('home/featured_artists.html', artists=artists, title='Artists')


@home.route('/admin/dashboard')
@login_required
def admin_dashboard():
    # prevent non-admins from accessing the page
    if not current_user.is_admin:
        abort(403)

    return render_template('home/admin_dashboard.html', title="Dashboard")


# Artwork Views
@home.route('/artwork', methods=['GET', 'POST'])
def featured_artwork():
    """
    List all the artwork
    """

    artwork = Artwork.query.all()

    return render_template('home/featured_artwork.html', artwork=artwork)


# Preferences View
@home.route('/preferences')
def preference():
    """
    Displays customer's preferred artists and groups
    """
    current_customer = Customer.query.get(ast.literal_eval(session['user_id']))
    artist = current_customer.artistPreference
    group = current_customer.groupPreference

    return render_template('home/preferences.html', preferred_artist=artist, preferred_group=group)


@home.route('/preferences/select_preferences', methods=['GET', 'POST'])
def select_preferences():
    """
    Allows the customer to select their preferred artists and groups
    """
    current_customer = Customer.query.get(ast.literal_eval(session['user_id']))

    form = SelectArtistPreferenceForm(obj=current_customer)
    if form.validate_on_submit:
        try:
            artist = form.artist.data
            if artist:
                artist.customerPreferArtist.append(current_customer)
                db.session.commit()
                flash('Artist preference selected.')
                return redirect(url_for('home.preference'))
        except exc.IntegrityError:
            db.session().rollback()
            flash('This preference was already selected.')
            return redirect(url_for('home.preference'))

    return render_template('home/select_preferences.html', form=form)


@home.route('/preferences/select_groupPreferences', methods=['GET', 'POST'])
def select_groupPreferences():
    """
    Allows the customer to select their preferred artists and groups
    """
    current_customer = Customer.query.get(ast.literal_eval(session['user_id']))

    form = SelectGroupPreferenceForm(obj=current_customer)
    if form.validate_on_submit:
        try:
            group = form.group.data
            if group:
                group.customerPreferGroup.append(current_customer)
                db.session.commit()
                flash('Group preference selected.')
                return redirect(url_for('home.preference'))
        except exc.IntegrityError:
            db.session().rollback()
            flash('This preference was already selected.')
            return redirect(url_for('home.preference'))

    return render_template('home/groupPreferences.html', form=form)


@home.route('/preferences/purchase/<artpiece>')
@login_required
def purchase(artpiece):
    """
    This will allow registered users to purchase art pieces
    """
    current_customer = Customer.query.get(ast.literal_eval(session['user_id']))
    spent = current_customer.expenditure
    piece = Artwork.query.get(artpiece)
    price = piece.price
    update_spent = spent + price
    current_customer.expenditure = update_spent
    piece.purchased = True
    piece.customerPurchaseArt = current_customer
    db.session.commit()
    flash('Purchase successful.')
    return redirect(url_for('home.featured_artwork'))

    return render_template(title='Purchase Artwork')


@home.route('/preferences/delete_artistPreferences/<artistName>', methods=['GET', 'POST'])
def delete_artistPreference(artistName):
    """
    This will allow the user to delete their selected preferences
    """
    current_customer = Customer.query.get(ast.literal_eval(session['user_id']))

    query_artistPrefer = Artist.query.join(artistPreferences).join(Customer).filter(
        artistPreferences.c.artistName == artistName, artistPreferences.c.customerName == current_customer.customerName).all()

    myArtist = []
    for artist in query_artistPrefer:
        myArtist.append(artist)

    myArtist[0].customerPreferArtist.remove(current_customer)
    db.session.commit()

    flash('Artist preference deleted.')
    return redirect(url_for('home.preference'))

    return render_template(title='Delete Artist Preferences')


@home.route('/preferences/delete_groupPreferences/<groupName>', methods=['GET', 'POST'])
def delete_groupPreference(groupName):
    """
    This will allow the user to delete their selected preferences
    """
    current_customer = Customer.query.get(ast.literal_eval(session['user_id']))

    query_groupPrefer = Group.query.join(groupPreferences).join(Customer).filter(
        groupPreferences.c.groupName == groupName, groupPreferences.c.customerName == current_customer.customerName).all()

    myGroup = []
    for group in query_groupPrefer:
        myGroup.append(group)

    myGroup[0].customerPreferGroup.remove(current_customer)
    db.session.commit()

    flash('Group preference deleted.')
    return redirect(url_for('home.preference'))

    return render_template(title='Delete Artist Preferences')


@home.route('/purchases')
@login_required
def my_purchases():
    """
    This will allow the customers to see their  expenditure and specific purchased artwork
    """
    current_customer = Customer.query.get(ast.literal_eval(session['user_id']))
    artwork = Artwork.query.filter_by(purchaser=current_customer.customerName).all()

    return render_template('home/purchases.html', customer=current_customer, artwork=artwork, title='My Purchases')


@home.route('/artists/artwork/<artist>')
def artist_artwork(artist):
    """
    Listing all artwork by a specific artist
    """
    name = artist.encode('utf-8')
    artistArt = Artist.query.filter_by(artistName=name).first()
    myArt = []
    for art in artistArt.artwork:
        myArt.append(art)

    return render_template('home/artist_artwork.html', artwork=myArt, title='Art')
