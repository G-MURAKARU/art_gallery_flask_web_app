from app import db, login_manager
from flask_login import UserMixin

db.metadata.clear()


artStyles = db.Table('artStyles',
                     db.Column('artistName', db.String(120), db.ForeignKey('artists.artistName', onupdate='cascade'), primary_key=True),
                     db.Column('styleName', db.String(40), db.ForeignKey('styles.styleName', onupdate='cascade'), primary_key=True))


class Artist(db.Model):
    """
    Create an Artists table
    """

    # Ensures table will be named in plural and not in singular
    # as is the name of the model
    __tablename__ = 'artists'
    __table_args__ = {'mysql_engine': 'InnoDB'}

    artistName = db.Column(db.String(120), primary_key=True)
    age = db.Column(db.Integer, nullable=False)
    birthplace = db.Column(db.String(120), nullable=False)
    artwork = db.relationship('Artwork', backref='artist', cascade='save-update, merge, delete, delete-orphan', lazy='dynamic')
    artStyle = db.relationship('Style', secondary=artStyles, cascade='save-update', backref=db.backref('artistStyle', lazy='dynamic'))

    def __repr__(self):
        return '{}'.format(self.artistName)


groupings = db.Table('groupings',
                     db.Column('title', db.String(120), db.ForeignKey('artwork.title', onupdate='cascade'), primary_key=True),
                     db.Column('groupName', db.String(60), db.ForeignKey('groups.groupName', onupdate='cascade'), primary_key=True))


class Style(db.Model):
    """
    Create a Styles Of Art table
    """

    __tablename__ = 'styles'

    styleName = db.Column(db.String(40), primary_key=True)

    def __repr__(self):
        return '{},'.format(self.styleName)


class Artwork(db.Model):
    """
    Create an Artwork table
    """

    __tablename__ = 'artwork'
    __table_args__ = {'mysql_engine': 'InnoDB'}

    title = db.Column(db.String(120), index=True, primary_key=True)
    year = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    typeOfArt = db.Column(db.String(60), nullable=False)
    artistName = db.Column(db.String(120), db.ForeignKey('artists.artistName', onupdate='cascade'), nullable=False)
    group = db.relationship('Group', secondary=groupings, backref=db.backref('artGroup', lazy='dynamic'))
    purchased = db.Column(db.Boolean, default=False)
    purchaser = db.Column(db.String(120), db.ForeignKey('customers.customerName', onupdate='cascade'), nullable=True)

    def __repr__(self):
        return '{} by {}, {}.'.format(self.title, self.artistName, self.year, self.price, self.typeOfArt)


class Group(db.Model):
    """
    Create a Group table
    """

    __tablename__ = 'groups'

    groupName = db.Column(db.String(60), primary_key=True)

    def __repr__(self):
        return '{},'.format(self.groupName)


artistPreferences = db.Table('artistPreferences',
                             db.Column('customerName', db.String(120), db.ForeignKey('customers.customerName', onupdate='cascade'), primary_key=True),
                             db.Column('artistName', db.String(120), db.ForeignKey('artists.artistName', onupdate='cascade'), primary_key=True))

groupPreferences = db.Table('groupPreferences',
                            db.Column('customerName', db.String(120), db.ForeignKey('customers.customerName', onupdate='cascade'), primary_key=True),
                            db.Column('groupName', db.String(60), db.ForeignKey('groups.groupName', onupdate='cascade'), primary_key=True))


class Customer(db.Model, UserMixin):
    """
    Create Customer Table
    """

    __tablename__ = 'customers'

    id = db.Column(db.Integer, primary_key=True)
    customerName = db.Column(db.String(120), nullable=False, unique=True)
    email = db.Column(db.String(60), nullable=False, unique=True)
    address = db.Column(db.String(120), nullable=False)
    expenditure = db.Column(db.Integer, nullable=False, default=0)
    password = db.Column(db.String(60), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    artistPreference = db.relationship('Artist', secondary=artistPreferences, backref=db.backref('customerPreferArtist', lazy='dynamic'))
    groupPreference = db.relationship('Group', secondary=groupPreferences, backref=db.backref('customerPreferGroup', lazy='dynamic'))
    purchase = db.relationship('Artwork', backref='customerPurchaseArt', lazy='dynamic')

    def __repr__(self):
        return '(Customer: {}, Email: {}, Address: {}, Expenditure: {})'.format(self.customerName, self.email, self.address, self.expenditure)


@login_manager.user_loader
def load_user(user_id):
    current_customer = Customer.query.get(int(user_id))
    return current_customer
