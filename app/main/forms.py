from flask_wtf import FlaskForm
from wtforms.fields import (BooleanField, PasswordField, StringField,
                            SubmitField)
from wtforms.validators import Email, EqualTo, InputRequired, Length
from .. import db
from ..models import Bucket, Destination
from . import main

class BucketForm(FlaskForm):
    bucket_name = StringField('Enter bucket name', validators=[Required(), Length(1,128)])
    submit = SubmitField('Submit')

class DestinationForm(FlaskForm):
    destination_endpoint = StringField('Enter desination end point', validators=[Required(), Length(1, 128)])
    submit = SubmitField('Submit')
