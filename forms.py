from wtforms import Form, StringField, RadioField, SelectField, TextAreaField, validators
from Base import *
from datetime import datetime


class CreateFaqForm (Form):
    question = StringField('Question', [validators.Length(min=1, max=150), validators.DataRequired()])
    answer = StringField('Answer', [validators.Length(min=1, max=150), validators.DataRequired()])
    remarks = TextAreaField('Remarks', [validators.Optional()])


class CreateFeedbackForm (Form):
    name = StringField('Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    subject = StringField('Subject', [validators.Length(min=1, max=150), validators.DataRequired()])
    content = TextAreaField('Content', [validators.Length(min=1, max=5000), validators.DataRequired()])
