from flask_wtf import FlaskForm
from wtforms.fields.html5 import SearchField
from webapp.app import db
from wtforms.widgets import Select
from wtforms import StringField, TextAreaField, SubmitField, SelectField, IntegerField, validators

class Carton_add_row(FlaskForm):
  carton_name = StringField('Kunde', [validators.DataRequired(message='Field required')])
  carton_oras = StringField('Ort', [validators.DataRequired(message='Field required')])
  carton_dimens = StringField('Mass', [validators.DataRequired(message='Field required')])
  carton_stampila = StringField('Klischee')
  carton_stanta = StringField('Werkzeug')
  carton_culoare1 = StringField('Farbe 1')
  carton_culoare2 = StringField('Farbe 2')
  carton_notite = TextAreaField('Notitzen')
  submit = SubmitField ('Save')

class Result_color(FlaskForm):
  name1 = StringField("")
  embacant1 = StringField("")
  embacant2 = StringField("")
  name2 = StringField("")
  simcacant1 = StringField("")
  simcacant2 = StringField("")
  submit1 = SubmitField('Update')

class Delete_data(FlaskForm):
  name_cul = StringField('',render_kw={'readonly': True})
  delete = SubmitField('Delete')

class Color_add (FlaskForm):
  color_name = StringField('Farbe', [validators.DataRequired(message='Field required')])
  submit = SubmitField ('Save')

class Search_color(FlaskForm):
  search = StringField('Search', [validators.DataRequired(message='Field required')],render_kw={"placeholder":"Farbe"})
  submit = SubmitField ('Search')

class Search_carton(FlaskForm):
  search = StringField('Search', [validators.DataRequired(message='Field required')],render_kw={"placeholder":"Kunde"})
  search1 = StringField('', [validators.DataRequired(message='Field required')],render_kw={"placeholder":"Mass"})
  submit = SubmitField ('Search')

class Showtable(FlaskForm):
  showtable = SubmitField('Show Table')

class Result_carton(FlaskForm):
    id_cart = IntegerField("")
    client_cart = StringField("")
    oras_cart = StringField("")
    dimensiune_cart = StringField("")
    stampila_cart = StringField("")
    stanta_cart = StringField("")
    notite_cart = TextAreaField("")
    cul1_cart = StringField("")
    cul2_cart = StringField("")
    submit1 = SubmitField('Update')

class Delete_carton(FlaskForm):
    nume_cart = StringField("",render_kw={'readonly': True})
    delete1 = SubmitField('Delete')
