from flask import Flask, render_template, request, redirect, url_for
from wtforms import StringField, validators, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email
import email_validator

app = Flask(__name__)
Bootstrap(app)
app.secret_key = "any-string-you-want-just-keep-it-secret"


class contactForm(FlaskForm):
    name = StringField(label='Name', validators=[DataRequired()])
    email = StringField(label='Email', validators=[DataRequired(), Email(granular_message=True)])
    message = StringField(label='Message')
    submit = SubmitField(label="Log In")