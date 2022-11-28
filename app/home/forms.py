# app/home/forms.py

from flask_wtf import FlaskForm
from wtforms import SubmitField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from ..models import Artist, Group


class SelectArtistPreferenceForm(FlaskForm):
    artist = QuerySelectField('Preferred Artist', query_factory=lambda: Artist.query.all(), allow_blank=True, get_label='artistName')
    submit = SubmitField('Select')


class SelectGroupPreferenceForm(FlaskForm):
    group = QuerySelectField('Preferred Group', query_factory=lambda: Group.query.all(), allow_blank=True, get_label='groupName')
    submit = SubmitField('Select')
