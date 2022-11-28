#app/admin/views.py


from flask import abort, flash, redirect, render_template, url_for, request
from flask_login import current_user, login_required

from . import admin
from .. import db
from forms import ArtistForm, ArtworkForm, GroupForm, StyleForm, ArtistStyleAssignmentForm, ArtworkGroupAssignmentForm, ArtistEditForm, ArtworkEditForm
from ..models import Artist, Artwork, Group, Style, Customer
from sqlalchemy import exc


def check_admin():
    """
    Prevent non-admins from accessing the page
    """
    if not current_user.is_admin:
        abort(403)


# Artists Views
@admin.route('/artists', methods=['GET', 'POST'])
@login_required
def list_artists():
    """
    Listing all artists
    """
    check_admin()

    artists = Artist.query.all()

    return render_template('admin/artists/artists.html', artists=artists, title='Artists')


@admin.route('/artists/add', methods=['GET', 'POST'])
@login_required
def add_artist():
    """
    Adding artists to the database
    """
    check_admin()

    add_artists = True

    form = ArtistForm()

    if form.validate_on_submit():
        artist = Artist(artistName=form.name.data, age=form.age.data, birthplace=form.birthplace.data)
        style = form.style.data
        if style:
            style.artistStyle.append(artist)
        db.session.add(artist)
        db.session.commit()
        flash('You have successfully added the artist.')

        return redirect(url_for('admin.list_artists'))

    return render_template('admin/artists/artist_add.html', action='Add', add_artists=add_artists, form=form, title='Add Artists')


@admin.route('/artists/edit/<artistName>', methods=['GET', 'POST'])
@login_required
def edit_artist(artistName):
    """
    Edit an existing artist
    """
    check_admin()

    add_artists = False

    form = ArtistEditForm()

    artist = Artist.query.get_or_404(artistName)

    if form.validate_on_submit():
        artist.artistName = form.name.data
        artist.age = form.age.data
        artist.birthplace = form.birthplace.data
        db.session.commit()
        flash('You have successfully edited the artist.')

        return redirect(url_for('admin.list_artists'))

    form.name.data = artist.artistName
    form.age.data = artist.age
    form.birthplace.data = artist.birthplace
    return render_template('admin/artists/artist_add.html', action='Add', add_artists=add_artists, form=form, title='Add Artists')


@admin.route('/artists/delete/<artistName>')
@login_required
def delete_artist(artistName):
    """
    Delete an existing artist
    """
    check_admin()

    artist = Artist.query.get_or_404(artistName)
    for art in artist.artStyle:
        myStyle = []
        myStyle.append(art)
        del myStyle[:]
    db.session.delete(artist)
    db.session.commit()
    flash('You have successfully deleted the artist.')

    return redirect(url_for('admin.list_artists'))

    return render_template(title='Delete Artist')


# Artwork Views
@admin.route('/artwork', methods=['GET', 'POST'])
@login_required
def list_artwork():
    """
    List all the artwork
    """
    check_admin()

    artwork = Artwork.query.all()

    return render_template('admin/artwork/artwork.html', artwork=artwork)


@admin.route('/artwork/add', methods=['GET', 'POST'])
@login_required
def add_artwork():
    """
    Add a piece of artwork
    """
    check_admin()

    add_artwork = True

    form = ArtworkForm()

    if form.validate_on_submit():
        artist = form.name.data
        artwork = Artwork(artist=artist, title=form.title.data, year=form.year.data, price=form.price.data, typeOfArt=form.type.data)
        group = form.group.data
        if group:
            group.artGroup.append(artwork)
        db.session.add(artwork)
        db.session.commit()
        flash('You have successfully added the artwork.')

        return redirect(url_for('admin.list_artwork'))

    return render_template('admin/artwork/artwork_add.html', add_artwork=add_artwork, form=form, title='Add Artwork')


@admin.route('/artwork/edit/<title>', methods=['GET', 'POST'])
@login_required
def edit_artwork(title):
    """
    Edit an existing artwork
    """
    check_admin()

    add_artwork = False

    form = ArtworkEditForm()

    artwork = Artwork.query.get_or_404(title)

    if form.validate_on_submit():
        artwork.artist = form.name.data
        if artwork.title == form.title.data:
            pass
        else:
            artwork.title = form.title.data
        artwork.year = form.year.data
        artwork.price = form.price.data
        artwork.typeOfArt = form.type.data
        group = form.group.data
        if group:
            group.artGroup.append(artwork)
        db.session.commit()

        flash('You have successfully edited the artwork.')

        # return artist
        return redirect(url_for('admin.list_artwork'))

    # artist = artist
    form.name.data = artwork.artist
    form.title.data = artwork.title
    form.year.data = artwork.year
    form.price.data = artwork.price
    form.type.data = artwork.typeOfArt
    return render_template('admin/artwork/artwork_add.html', action='Add', add_artwork=add_artwork, form=form, title='Add Artwork')


@admin.route('/artwork/delete/<title>')
@login_required
def delete_artwork(title):
    """
    Delete an existing artwork
    """
    check_admin()

    artwork = Artwork.query.get_or_404(title)
    for art in artwork.group:
        myGroup = []
        myGroup.append(art)
        del myGroup[:]
    db.session.delete(artwork)
    db.session.commit()
    flash('You have successfully deleted the artwork.')

    return redirect(url_for('admin.list_artwork'))

    return render_template(title='Delete Artwork')


#Group Views
@admin.route('/groups', methods=['GET', 'POST'])
@login_required
def list_groups():
    """
    List all groups
    """
    check_admin()

    groups = Group.query.all()

    return render_template('admin/groups/groups.html', groups=groups)


@admin.route('/groups/add', methods=['GET', 'POST'])
@login_required
def add_groups():
    """
    Add group to database
    """
    check_admin()

    add_groups = True

    form = GroupForm()

    if form.validate_on_submit():
        group = Group(groupName=form.title.data)
        db.session.add(group)
        db.session.commit()

        return redirect(url_for('admin.list_groups'))

    return render_template('admin/groups/group_add.html', action='Add', add_groups=add_groups, form=form, title='Add Groups')


@admin.route('/groups/add/<groupName>', methods=['GET', 'POST'])
@login_required
def edit_groups(groupName):
    """
    Edit existing groups
    """
    check_admin()

    add_groups = False

    form = GroupForm()

    group = Group.query.get_or_404(groupName)

    if form.validate_on_submit():
        group.groupName = form.title.data
        db.session.commit()
        flash('You have successfully edited the group.')

        return redirect(url_for('admin.list_groups'))

    form.title.data = group.groupName

    return render_template('admin/groups/group_add.html', action='Add', add_groups=add_groups, form=form, title='Edit Groups')


@admin.route('/groups/delete/<groupName>')
@login_required
def delete_groups(groupName):
    """
    Delete an existing group
    """
    check_admin()

    group = Group.query.get_or_404(groupName)
    for art in group.artGroup:
        myGroup = []
        myGroup.append(art)
        del myGroup[:]
    db.session.delete(group)
    db.session.commit()
    flash('You have successfully deleted the group.')

    return redirect(url_for('admin.list_groups'))

    return render_template(title='Delete Group')


# Style Routes
@admin.route('/styles', methods=['GET', 'POST'])
@login_required
def list_styles():
    """
    List all styles
    """
    check_admin()

    styles = Style.query.all()

    return render_template('admin/styles/styles.html', styles=styles)


@admin.route('/styles/add', methods=['GET', 'POST'])
@login_required
def add_styles():
    """
    Add style to database
    """
    check_admin()

    add_styles = True

    form = StyleForm()

    if form.validate_on_submit():
        style = Style(styleName=form.title.data)
        db.session.add(style)
        db.session.commit()

        return redirect(url_for('admin.list_styles'))

    return render_template('admin/styles/style_add.html', action='Add', add_styles=add_styles, form=form, title='Add Styles')


@admin.route('/styles/add/<styleName>', methods=['GET', 'POST'])
@login_required
def edit_styles(styleName):
    """
    Edit existing styles
    """
    check_admin()

    add_styles = False

    form = StyleForm()

    style = Style.query.get_or_404(styleName)

    if form.validate_on_submit():
        style.styleName = form.title.data
        db.session.commit()
        flash('You have successfully edited the style of art.')

        return redirect(url_for('admin.list_styles'))

    form.title.data = style.styleName
    return render_template('admin/styles/style_add.html', action='Add', add_styles=add_styles, form=form, title='Edit Styles')


@admin.route('/styles/delete/<styleName>')
@login_required
def delete_styles(styleName):
    """
    Delete an existing group
    """
    check_admin()

    style = Style.query.get_or_404(styleName)
    for art in style.artistStyle:
        myStyle = []
        myStyle.append(art)
        del myStyle[:]
    db.session.delete(style)
    db.session.commit()
    flash('You have successfully deleted the style of art.')

    return redirect(url_for('admin.list_styles'))

    return render_template(title='Delete Style')


@admin.route('/artists/assign/<artistName>', methods=['GET', 'POST'])
@login_required
def assign_styles(artistName):
    """
    Assign styles to artists
    """
    check_admin()

    artist = Artist.query.get_or_404(artistName)

    form = ArtistStyleAssignmentForm(obj=artist)

    if form.validate_on_submit():
        try:
            style = form.style.data
            if style:
                style.artistStyle.append(artist)
                db.session.commit()
                flash('Style assignment successful.')
                return redirect(url_for('admin.list_artists'))
            else:
                return redirect(url_for('admin.list_artists'))
        except exc.IntegrityError:
            db.session().rollback()
            flash("The style has already been assigned to that artist.")
            return redirect(url_for('admin.list_artists'))

    return render_template('/admin/artists/style_add.html', artist=artist, form=form, title='Assign Style')


@admin.route('/artwork/assign/<title>', methods=['GET', 'POST'])
@login_required
def assign_groups(title):
    """
    Assign groups to artwork
    """
    check_admin()

    artwork = Artwork.query.get_or_404(title)

    form = ArtworkGroupAssignmentForm(obj=artwork)

    if form.validate_on_submit():
        try:
            group = form.group.data
            if group:
                group.artGroup.append(artwork)
                db.session.commit()
                flash('Group assignment successful.')
                return redirect(url_for('admin.list_artwork'))
            else:
                return redirect(url_for('admin.list_artwork'))
        except exc.IntegrityError:
            db.session().rollback()
            flash("The art piece has already been assigned to that group.")
            return redirect(url_for('admin.list_artwork'))

    return render_template('/admin/artwork/group_add.html', artwork=artwork, form=form, title='Assign Group')


@admin.route('/customers')
@login_required
def list_customers():
    """
    Admin can view information about customers
    """
    check_admin()

    customers = Customer.query.all()

    return render_template('admin/customers/customers.html', customers=customers, title='Our Customers')
