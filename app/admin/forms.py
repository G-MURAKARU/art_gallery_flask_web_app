# app/admin/forms.py

from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, IntegerField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired, InputRequired, ValidationError
from ..models import Artist, Artwork, Group, Style


class ArtistForm(FlaskForm):
    name = StringField('Artist Name', validators=[InputRequired(), DataRequired()])
    age = IntegerField('Age', validators=[InputRequired(), DataRequired()])
    birthplace = StringField('Birthplace', validators=[InputRequired(), DataRequired()])
    style = QuerySelectField(query_factory=lambda: Style.query.all(), allow_blank=True, get_label='styleName')
    submit = SubmitField('Add')

    def validate_name(self, name):
        artist = Artist.query.filter_by(artistName=name.data).first()
        if artist:
            raise ValidationError('This artist already exists.')


class ArtworkForm(FlaskForm):
    name = QuerySelectField(query_factory=lambda: Artist.query.all(), allow_blank=False, get_label='artistName')
    title = StringField('Artwork Title', validators=[InputRequired(), DataRequired()])
    year = IntegerField('Year of Creation', validators=[InputRequired(), DataRequired()])
    price = IntegerField('Artwork Price', validators=[InputRequired(), DataRequired()])
    type = StringField('Artwork Type', validators=[InputRequired(), DataRequired()])
    group = QuerySelectField(query_factory=lambda: Group.query.all(), allow_blank=False, get_label='groupName')
    submit = SubmitField('Add')

    def validate_title(self, title):
        artwork = Artwork.query.filter_by(title=title.data).first()
        if artwork:
            raise ValidationError('This artwork already exists.')


class ArtistEditForm(FlaskForm):
    name = StringField('Artist Name', validators=[InputRequired(), DataRequired()])
    age = IntegerField('Age', validators=[InputRequired(), DataRequired()])
    birthplace = StringField('Birthplace', validators=[InputRequired(), DataRequired()])
    style = QuerySelectField(query_factory=lambda: Style.query.all(), allow_blank=True, get_label='styleName')
    submit = SubmitField('Add')


class ArtworkEditForm(FlaskForm):
    name = QuerySelectField(query_factory=lambda: Artist.query.all(), allow_blank=False, get_label='artistName')
    title = StringField('Artwork Title', validators=[InputRequired(), DataRequired()])
    year = IntegerField('Year of Creation', validators=[InputRequired(), DataRequired()])
    price = IntegerField('Artwork Price', validators=[InputRequired(), DataRequired()])
    type = StringField('Artwork Type', validators=[InputRequired(), DataRequired()])
    group = QuerySelectField(query_factory=lambda: Group.query.all(), allow_blank=True, get_label='groupName')
    submit = SubmitField('Add')


class GroupForm(FlaskForm):
    title = StringField('Group Title', validators=[InputRequired(), DataRequired()])
    submit = SubmitField('Add')

    def validate_title(self, title):
        group = Group.query.filter_by(groupName=title.data).first()
        if group:
            raise ValidationError('This group already exists.')


class StyleForm(FlaskForm):
    title = StringField('Style of Art', validators=[InputRequired(), DataRequired()])
    submit = SubmitField('Add')

    def validate_title(self, title):
        style = Style.query.filter_by(styleName=title.data).first()
        if style:
            raise ValidationError('This style already exists.')


class ArtistStyleAssignmentForm(FlaskForm):
    style = QuerySelectField(query_factory=lambda: Style.query.all(), allow_blank=True, get_label='styleName')
    submit = SubmitField('Assign')


class ArtworkGroupAssignmentForm(FlaskForm):
    group = QuerySelectField(query_factory=lambda: Group.query.all(), allow_blank=True, get_label='groupName')
    submit = SubmitField('Assign')
