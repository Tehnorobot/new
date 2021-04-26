from wtforms.fields.html5 import EmailField
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, IntegerField
from wtforms.validators import DataRequired

class JobAddForm(FlaskForm):
    title = StringField('Job Title', validators=[DataRequired()])
    teamLeader = IntegerField('Team Leader id', validators=[DataRequired()])
    workSize = IntegerField('Work Size', validators=[DataRequired()])
    collaborators = StringField('Collaborators', validators=[DataRequired()])
    complete = BooleanField('Is job finished?')
    submit = SubmitField('Submit')