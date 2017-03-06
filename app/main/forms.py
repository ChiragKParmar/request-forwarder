from flask_wtf import FlaskForm
from wtforms.fields import (BooleanField, PasswordField, StringField,
                            SubmitField)
from wtforms.validators import Email, EqualTo, InputRequired, Length
from .. import db
from ..models import ProxyUrl
from . import main

class RegistrationForm(FlaskForm):
    outgoing_url = StringField('Outgoing URL', validators=[InputRequired(), Length(1, 64)])
    submit = SubmitField('submit')
