from flask_wtf import FlaskForm
from wtforms.fields import (BooleanField, PasswordField, StringField,
                            SubmitField)
from wtforms.validators import Email, EqualTo, InputRequired, Length
from .. import db
from ..models import Bucket, Destination
from . import main

class BucketForm(FlaskForm):
    #TODO update this class

class DestinationForm(FlaskForm):
    #TODO update this class
